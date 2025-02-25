"""
Telemetry Module

Tracks system usage, performance metrics, and provides reporting
for the TRILOGY Brain system.
"""
import logging
import time
from typing import Dict, Any, List, Optional
import os
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class Telemetry:
    """
    Telemetry system for tracking usage and performance metrics
    
    This class tracks:
    - Queries and their execution
    - Model performance
    - System events
    - Usage statistics
    """
    
    def __init__(self, data_path: Optional[str] = None):
        """
        Initialize the telemetry system
        
        Args:
            data_path: Path to save telemetry data (or None for in-memory only)
        """
        self.events = []
        self.query_counter = 0
        self.data_path = data_path
        
        # Try to load previous telemetry if path is provided
        if data_path and os.path.exists(data_path):
            try:
                with open(data_path, 'r') as f:
                    self.events = json.load(f)
                logger.info(f"Loaded {len(self.events)} telemetry events from {data_path}")
            except Exception as e:
                logger.error(f"Error loading telemetry data: {e}")
                
        logger.info("Telemetry system initialized")
        
    def track_query(self, query: str) -> str:
        """
        Track a new query
        
        Args:
            query: The query text
            
        Returns:
            query_id: Unique identifier for the query
        """
        self.query_counter += 1
        query_id = f"q-{int(time.time())}-{self.query_counter}"
        
        event = {
            "event_type": "query",
            "query_id": query_id,
            "query": query[:100] + "..." if len(query) > 100 else query,  # Truncate long queries
            "timestamp": time.time()
        }
        
        self.events.append(event)
        self._save_telemetry()
        
        return query_id
        
    def track_response(self, 
                       query_id: str, 
                       model: str, 
                       execution_time: float,
                       token_count: int = 0) -> None:
        """
        Track a response to a query
        
        Args:
            query_id: The ID of the query being responded to
            model: The model used for the response
            execution_time: Time taken to generate the response
            token_count: Number of tokens used (if available)
        """
        event = {
            "event_type": "response",
            "query_id": query_id,
            "model": model,
            "execution_time": execution_time,
            "token_count": token_count,
            "timestamp": time.time()
        }
        
        self.events.append(event)
        self._save_telemetry()
        
    def track_error(self, query_id: str, error_message: str) -> None:
        """
        Track an error that occurred during processing
        
        Args:
            query_id: The ID of the query that caused the error
            error_message: Description of the error
        """
        event = {
            "event_type": "error",
            "query_id": query_id,
            "error_message": error_message,
            "timestamp": time.time()
        }
        
        self.events.append(event)
        self._save_telemetry()
        
    def track_system_event(self, event_type: str, details: Dict[str, Any]) -> None:
        """
        Track a system event (e.g., startup, shutdown, config change)
        
        Args:
            event_type: Type of system event
            details: Additional event details
        """
        event = {
            "event_type": f"system_{event_type}",
            "details": details,
            "timestamp": time.time()
        }
        
        self.events.append(event)
        self._save_telemetry()
        
    def get_recent_activity(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent activity events
        
        Args:
            limit: Maximum number of events to return
            
        Returns:
            List of recent events with formatted timestamps
        """
        recent_events = sorted(
            self.events[-limit:] if len(self.events) > 0 else [],
            key=lambda x: x.get("timestamp", 0),
            reverse=True
        )
        
        # Format events for display
        formatted_events = []
        for event in recent_events:
            formatted_event = event.copy()
            # Convert timestamp to readable format
            timestamp = event.get("timestamp", 0)
            formatted_event["time"] = datetime.fromtimestamp(timestamp).strftime("%H:%M:%S")
            formatted_events.append(formatted_event)
            
        return formatted_events
        
    def get_model_usage_stats(self) -> Dict[str, Any]:
        """
        Get statistics on model usage
        
        Returns:
            Dictionary with model usage statistics
        """
        model_stats = {}
        model_counts = {}
        model_times = {}
        model_tokens = {}
        
        # Collect data
        for event in self.events:
            if event.get("event_type") == "response" and "model" in event:
                model = event.get("model", "unknown")
                if model not in model_counts:
                    model_counts[model] = 0
                    model_times[model] = []
                    model_tokens[model] = 0
                    
                model_counts[model] += 1
                model_times[model].append(event.get("execution_time", 0))
                model_tokens[model] += event.get("token_count", 0)
                
        # Calculate statistics
        for model in model_counts.keys():
            times = model_times[model]
            model_stats[model] = {
                "count": model_counts[model],
                "avg_time": sum(times) / len(times) if times else 0,
                "total_tokens": model_tokens[model]
            }
            
        return model_stats
        
    def _save_telemetry(self) -> None:
        """Save telemetry data to disk if a path is provided"""
        if not self.data_path:
            return
            
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
            
            # Save the most recent 1000 events to avoid file growth
            with open(self.data_path, 'w') as f:
                json.dump(self.events[-1000:], f)
        except Exception as e:
            logger.error(f"Error saving telemetry data: {e}")

    def get_system_metrics(self) -> Dict[str, Any]:
        """
        Get overall system metrics
        
        Returns:
            Dictionary with system-wide metrics
        """
        # Count events by type
        event_counts = {}
        for event in self.events:
            event_type = event.get("event_type", "unknown")
            if event_type not in event_counts:
                event_counts[event_type] = 0
            event_counts[event_type] += 1
            
        # Count errors
        error_count = event_counts.get("error", 0)
        
        # Calculate success rate
        query_count = event_counts.get("query", 0)
        response_count = event_counts.get("response", 0)
        success_rate = response_count / max(1, query_count)
        
        # Calculate average response time
        response_times = [
            event.get("execution_time", 0) 
            for event in self.events 
            if event.get("event_type") == "response"
        ]
        avg_response_time = sum(response_times) / max(1, len(response_times))
        
        return {
            "total_queries": query_count,
            "error_count": error_count,
            "success_rate": success_rate,
            "avg_response_time": avg_response_time,
            "event_counts": event_counts
        } 