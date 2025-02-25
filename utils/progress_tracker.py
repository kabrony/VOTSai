import time
import threading
from typing import Dict, Any, Optional, Callable, List
import logging
import uuid

logger = logging.getLogger(__name__)

class ProgressTracker:
    """Track progress of long-running operations."""
    
    _instance = None
    _lock = threading.Lock()
    _operations = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProgressTracker, cls).__new__(cls)
        return cls._instance
        
    def start_operation(self, operation_type: str, description: str, client_id: str = "default") -> str:
        """Start tracking a new operation."""
        with self._lock:
            operation_id = str(uuid.uuid4())
            self._operations[operation_id] = {
                "id": operation_id,
                "type": operation_type,
                "description": description,
                "status": "running",
                "progress": 0.0,
                "message": "Operation started",
                "start_time": time.time(),
                "end_time": None,
                "eta": None,
                "client_id": client_id,
                "result": None,
                "error": None
            }
            logger.debug(f"Started operation {operation_id} ({operation_type}): {description}")
            return operation_id
            
    def update_progress(self, operation_id: str, progress: float, message: str = None) -> bool:
        """Update the progress of an operation."""
        with self._lock:
            if operation_id not in self._operations:
                logger.warning(f"Attempted to update non-existent operation: {operation_id}")
                return False
                
            operation = self._operations[operation_id]
            if operation["status"] != "running":
                logger.warning(f"Attempted to update non-running operation: {operation_id}")
                return False
                
            old_progress = operation["progress"]
            operation["progress"] = min(max(0.0, progress), 1.0)  # Clamp to [0, 1]
            
            if message:
                operation["message"] = message
                
            # Calculate ETA if we have progress
            if old_progress < progress and progress > 0:
                elapsed = time.time() - operation["start_time"]
                estimated_total = elapsed / progress
                eta = operation["start_time"] + estimated_total
                operation["eta"] = eta
                
            logger.debug(f"Updated operation {operation_id}: {progress:.1%} - {message or ''}")
            return True
            
    def complete_operation(self, operation_id: str, result: Any = None) -> bool:
        """Mark an operation as completed."""
        with self._lock:
            if operation_id not in self._operations:
                logger.warning(f"Attempted to complete non-existent operation: {operation_id}")
                return False
                
            operation = self._operations[operation_id]
            operation["status"] = "completed"
            operation["progress"] = 1.0
            operation["end_time"] = time.time()
            operation["result"] = result
            
            logger.debug(f"Completed operation {operation_id}")
            return True
            
    def fail_operation(self, operation_id: str, error: str) -> bool:
        """Mark an operation as failed."""
        with self._lock:
            if operation_id not in self._operations:
                logger.warning(f"Attempted to fail non-existent operation: {operation_id}")
                return False
                
            operation = self._operations[operation_id]
            operation["status"] = "failed"
            operation["end_time"] = time.time()
            operation["error"] = error
            
            logger.debug(f"Failed operation {operation_id}: {error}")
            return True
            
    def get_operation(self, operation_id: str) -> Optional[Dict[str, Any]]:
        """Get information about an operation."""
        with self._lock:
            if operation_id not in self._operations:
                return None
            return dict(self._operations[operation_id])  # Return a copy
            
    def clean_old_operations(self, max_age: int = 3600) -> int:
        """Remove operations older than max_age seconds."""
        with self._lock:
            now = time.time()
            to_remove = []
            
            for op_id, op in self._operations.items():
                if op["status"] in ["completed", "failed"]:
                    end_time = op["end_time"] or now  # Use now if end_time is None
                    age = now - end_time
                    if age > max_age:
                        to_remove.append(op_id)
                        
            for op_id in to_remove:
                del self._operations[op_id]
                
            return len(to_remove)
            
    def get_active_operations(self, client_id: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
        """Get all active operations, optionally filtered by client."""
        with self._lock:
            result = {}
            for op_id, op in self._operations.items():
                if op["status"] == "running" and (client_id is None or op["client_id"] == client_id):
                    result[op_id] = dict(op)
            return result
