"""
Model Analytics Module

Provides visualization and tracking of model performance metrics.
"""
import logging
import time
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sqlite3
import os
import json

logger = logging.getLogger(__name__)

class ModelAnalytics:
    """
    Tracks and visualizes model performance metrics
    
    Features:
    - Performance tracking by domain and model
    - Response time visualization
    - Success rate metrics
    - Domain effectiveness comparison
    """
    
    def __init__(self, db_path: str = "data/analytics.db"):
        """
        Initialize the analytics system
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._initialize_db()
        logger.info(f"Model analytics initialized with database at {db_path}")
        
    def _initialize_db(self):
        """Initialize the SQLite database"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Create tables if they don't exist
        c.execute('''
        CREATE TABLE IF NOT EXISTS model_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            model TEXT,
            domain TEXT,
            query TEXT,
            execution_time REAL,
            token_count INTEGER,
            success BOOLEAN
        )
        ''')
        
        c.execute('''
        CREATE TABLE IF NOT EXISTS model_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usage_id INTEGER,
            rating INTEGER,
            feedback TEXT,
            FOREIGN KEY (usage_id) REFERENCES model_usage (id)
        )
        ''')
        
        conn.commit()
        conn.close()
        
    def track_model_usage(self, 
                          model: str, 
                          domain: str, 
                          query: str, 
                          execution_time: float,
                          token_count: int = 0, 
                          success: bool = True) -> int:
        """
        Track model usage for analytics
        
        Args:
            model: Name of the model used
            domain: Domain category (general, coding, math, etc.)
            query: User query text
            execution_time: Execution time in seconds
            token_count: Number of tokens used
            success: Whether the query was successful
            
        Returns:
            ID of the inserted record
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        timestamp = datetime.now().isoformat()
        
        c.execute('''
        INSERT INTO model_usage 
        (timestamp, model, domain, query, execution_time, token_count, success)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, model, domain, query, execution_time, token_count, success))
        
        usage_id = c.lastrowid
        conn.commit()
        conn.close()
        
        return usage_id
    
    def record_feedback(self, usage_id: int, rating: int, feedback: Optional[str] = None):
        """
        Record user feedback for a model interaction
        
        Args:
            usage_id: ID of the usage record
            rating: Rating from 1-5
            feedback: Optional feedback text
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
        INSERT INTO model_feedback 
        (usage_id, rating, feedback)
        VALUES (?, ?, ?)
        ''', (usage_id, rating, feedback))
        
        conn.commit()
        conn.close()
    
    def get_model_performance(self, 
                             days: int = 7,
                             model: Optional[str] = None) -> Dict[str, Any]:
        """
        Get performance metrics for models
        
        Args:
            days: Number of days to include
            model: Optional filter by model name
            
        Returns:
            Dictionary of performance metrics
        """
        conn = sqlite3.connect(self.db_path)
        
        # Calculate the date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Create query with parameters
        query = '''
        SELECT model, domain, AVG(execution_time) as avg_time, 
               COUNT(*) as count, SUM(CASE WHEN success THEN 1 ELSE 0 END) as success_count,
               AVG(token_count) as avg_tokens
        FROM model_usage
        WHERE timestamp >= ?
        '''
        params = [start_date.isoformat()]
        
        # Add model filter if specified
        if model:
            query += " AND model = ?"
            params.append(model)
            
        # Group by model and domain
        query += " GROUP BY model, domain"
        
        # Load into DataFrame
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        
        # Calculate success rate
        if not df.empty:
            df['success_rate'] = df['success_count'] / df['count'] * 100
        
        return {
            "performance_data": df.to_dict(orient='records'),
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "total_queries": df['count'].sum() if not df.empty else 0,
            "overall_success_rate": (df['success_count'].sum() / df['count'].sum() * 100) if not df.empty else 0
        }
    
    def create_performance_chart(self, days: int = 7) -> Dict[str, Any]:
        """
        Create performance comparison chart
        
        Args:
            days: Number of days to include
            
        Returns:
            Chart data
        """
        # Get performance data
        performance_data = self.get_performance_data(days)
        
        # Create performance chart
        fig_performance = px.line(
            performance_data,
            x="date",
            y="avg_time",
            color="model",
            title="Response Time by Model",
            labels={"avg_time": "Average Response Time (s)", "date": "Date", "model": "Model"}
        )
        
        # For domain effectiveness, use grouped bar chart instead of heatmap
        # (more compatible across plotly versions)
        fig_domains = px.bar(
            performance_data,
            x="domain",
            y="success_rate",
            color="model",
            barmode="group",
            title="Success Rate by Domain and Model",
            labels={"success_rate": "Success Rate (%)", "domain": "Domain", "model": "Model"}
        )
        
        return {
            "fig_performance": fig_performance,
            "fig_domains": fig_domains,
            "data": {
                "performance_data": performance_data
            }
        }
    
    def get_usage_trends(self, days: int = 30) -> Dict[str, Any]:
        """
        Get trends in model usage over time
        
        Args:
            days: Number of days to include
            
        Returns:
            Dictionary with trend data and figure
        """
        conn = sqlite3.connect(self.db_path)
        
        # Calculate the date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Query for daily counts by model
        query = '''
        SELECT date(timestamp) as date, model, COUNT(*) as count
        FROM model_usage
        WHERE timestamp >= ?
        GROUP BY date(timestamp), model
        ORDER BY date
        '''
        
        df = pd.read_sql_query(query, conn, params=[start_date.isoformat()])
        conn.close()
        
        if df.empty:
            return {
                "fig": go.Figure(),
                "data": []
            }
        
        # Create line chart of usage trends
        fig = px.line(
            df, 
            x='date', 
            y='count', 
            color='model',
            labels={'count': 'Number of Queries', 'date': 'Date', 'model': 'Model'},
            title='Model Usage Trends'
        )
        
        # Improve layout
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Number of Queries",
            legend_title="Model"
        )
        
        return {
            "fig": fig,
            "data": df.to_dict(orient='records')
        }
    
    def get_performance_data(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get performance data for the specified number of days
        
        Args:
            days: Number of days to include
            
        Returns:
            List of performance data dictionaries
        """
        # Calculate the date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Query for model usage
        query = """
        SELECT model, domain, AVG(execution_time) as avg_time, COUNT(*) as count,
               SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as success_rate,
               date(timestamp) as date
        FROM model_usage
        WHERE timestamp >= ?
        GROUP BY model, domain, date(timestamp)
        ORDER BY date
        """
        
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query(query, conn, params=[start_date.isoformat()])
            conn.close()
            
            if df.empty:
                # Return empty data if no records
                return []
            
            # Convert to list of dictionaries
            return df.to_dict('records')
        except Exception as e:
            logger.error(f"Error fetching performance data: {e}")
            return [] 