"""
System resilience module for TRILOGY Brain
Provides error recovery, circuit breakers, and self-healing
"""
import logging
import time
import threading
from typing import Dict, Any, Callable, List
import os
import json

class CircuitBreaker:
    """Prevent system overload by breaking problematic circuits"""
    
    def __init__(self, name: str, failure_threshold: int = 5, 
                 reset_timeout: int = 30):
        self.name = name
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.failure_count = 0
        self.last_failure_time = 0
        self.open = False
        self.logger = logging.getLogger(f"trilogy.circuit_breaker.{name}")
        
    def execute(self, func: Callable, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        if self.open:
            if time.time() - self.last_failure_time > self.reset_timeout:
                self.logger.info(f"Circuit {self.name} reset after timeout")
                self.open = False
                self.failure_count = 0
            else:
                raise CircuitOpenError(f"Circuit {self.name} is open")
                
        try:
            result = func(*args, **kwargs)
            self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.open = True
                self.logger.warning(f"Circuit {self.name} opened after {self.failure_count} failures")
                
            raise 