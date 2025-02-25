"""
Self-improvement learning system for TRILOGY Brain
Continuously learns from interactions to improve performance
"""
import pandas as pd
import numpy as np
import joblib
import os
import json
import logging
from typing import Dict, List, Any, Optional
import threading
import time
import re
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

class FeatureExtractor:
    """Extracts features from queries for machine learning"""
    
    def __init__(self):
        """Initialize the feature extractor"""
        self.logger = logging.getLogger("trilogy.features")
        # Load dictionaries for domain-specific terms if available
        self.domain_terms = self._load_domain_terms()
        
    def _load_domain_terms(self) -> Dict[str, List[str]]:
        """Load domain-specific term dictionaries"""
        domains = {
            "coding": ["function", "class", "code", "programming", "algorithm", "variable", "bug", "debug"],
            "math": ["equation", "calculate", "solve", "math", "formula", "number", "sum", "difference"],
            "science": ["theory", "experiment", "hypothesis", "scientific", "research", "data"],
            "general": ["what", "who", "how", "why", "when", "explain", "describe"]
        }
        return domains
        
    def extract_features(self, query: str) -> Dict[str, float]:
        """
        Extract features from a query
        
        Args:
            query: The query text
            
        Returns:
            Dictionary of features
        """
        # Initialize features
        features = {}
        
        # Basic text features
        features["length"] = len(query)
        features["word_count"] = len(query.split())
        features["avg_word_length"] = sum(len(w) for w in query.split()) / max(1, len(query.split()))
        
        # Special character features
        features["has_code"] = 1.0 if any(c in query for c in "{}()[]<>;:") else 0.0
        features["has_math"] = 1.0 if any(c in query for c in "+-*/^=<>") else 0.0
        features["has_question"] = 1.0 if "?" in query else 0.0
        
        # Domain detection
        for domain, terms in self.domain_terms.items():
            query_lower = query.lower()
            term_count = sum(1 for term in terms if term in query_lower)
            features[f"domain_{domain}"] = term_count / len(terms)
            
        # Complexity features
        features["complexity"] = min(1.0, features["length"] / 500)
        
        self.logger.debug(f"Extracted features: {features}")
        return features

class PerformanceLearner:
    """
    Learns to predict the best model for different query types
    based on historical performance
    """
    
    def __init__(self, data_path: str = "data/performance"):
        self.data_path = data_path
        self.logger = logging.getLogger("trilogy.learner")
        os.makedirs(data_path, exist_ok=True)
        self.model_path = f"{data_path}/router_model.joblib"
        self.feature_extractor = FeatureExtractor()
        self.model = self._load_model()
        self.min_samples = 100
        self.training_thread = None
        
    def _load_model(self):
        """Load or create router model"""
        if os.path.exists(self.model_path):
            self.logger.info(f"Loading existing router model from {self.model_path}")
            return joblib.load(self.model_path)
        else:
            self.logger.info("Creating new router model")
            return RandomForestClassifier(n_estimators=100, class_weight='balanced')
    
    def record_performance(self, query: str, model_used: str, 
                         execution_time: float, success: bool):
        """Record model performance for a query"""
        # Extract features from query
        features = self.feature_extractor.extract_features(query)
        
        # Add performance data
        performance_data = {
            "query": query,
            "model": model_used,
            "execution_time": execution_time,
            "success": 1 if success else 0,
            "timestamp": time.time(),
            **features
        }
        
        # Save performance data
        self._save_performance_data(performance_data)
        
        # Check if we should train in background
        self._check_training_needed()
    
    def recommend_model(self, query: str) -> str:
        """Recommend the best model for a query"""
        # Extract features
        features = self.feature_extractor.extract_features(query)
        
        # Convert to array for prediction
        feature_array = np.array([list(features.values())])
        
        # Make prediction
        try:
            prediction = self.model.predict(feature_array)[0]
            confidence = max(self.model.predict_proba(feature_array)[0])
            
            self.logger.info(f"Model recommendation: {prediction} with confidence {confidence:.2f}")
            
            # Fall back to default if confidence is low
            if confidence < 0.6:
                self.logger.info("Low confidence, falling back to default model")
                return "default_model"
                
            return prediction
        except:
            self.logger.warning("Error making model prediction, using default")
            return "default_model"

    def _save_performance_data(self, data: Dict[str, Any]):
        """Save performance data to file"""
        # Create data file if it doesn't exist
        data_file = os.path.join(self.data_path, "performance_data.jsonl")
        
        # Append data to file
        with open(data_file, "a") as f:
            f.write(json.dumps(data) + "\n")
        
    def _check_training_needed(self):
        """Check if we should train the model"""
        # Count data samples
        data_file = os.path.join(self.data_path, "performance_data.jsonl")
        if not os.path.exists(data_file):
            return
        
        # Count lines in file
        sample_count = 0
        with open(data_file, "r") as f:
            for line in f:
                sample_count += 1
            
        # Check if we have enough data
        if sample_count >= self.min_samples and (self.training_thread is None or not self.training_thread.is_alive()):
            self.logger.info(f"Starting training with {sample_count} samples")
            self.training_thread = threading.Thread(target=self._train_model)
            self.training_thread.daemon = True
            self.training_thread.start()
        
    def _train_model(self):
        """Train the model in background"""
        # Load data
        data_file = os.path.join(self.data_path, "performance_data.jsonl")
        data = []
        with open(data_file, "r") as f:
            for line in f:
                try:
                    data.append(json.loads(line))
                except:
                    continue
                
        if not data:
            self.logger.warning("No data to train on")
            return
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Extract features and targets
        feature_cols = [col for col in df.columns if col.startswith("domain_") 
                       or col in ["length", "word_count", "complexity", "has_code", "has_math"]]
        X = df[feature_cols].values
        y = df["model"].values
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        try:
            # Train model
            self.model.fit(X_train, y_train)
            
            # Evaluate model
            accuracy = self.model.score(X_test, y_test)
            self.logger.info(f"Model trained with accuracy: {accuracy:.2f}")
            
            # Save model
            joblib.dump(self.model, self.model_path)
            self.logger.info(f"Model saved to {self.model_path}")
        except Exception as e:
            self.logger.error(f"Error training model: {e}") 