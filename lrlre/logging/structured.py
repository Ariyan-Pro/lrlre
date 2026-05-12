"""
LRLRE Logging System - Structured logging for enterprise
"""
import logging
import logging.handlers
import json
import time
from datetime import datetime
from pathlib import Path
import traceback
from typing import Dict, Any, Optional

# Create logs directory
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

class StructuredLogger:
    """Structured JSON logger for enterprise"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers
        self.logger.handlers.clear()
        
        # Create formatters
        json_formatter = logging.Formatter(
            '{"time": "%(asctime)s", "level": "%(levelname)s", "name": "%(name)s", "message": %(message)s}'
        )
        text_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # File handlers
        app_handler = logging.handlers.RotatingFileHandler(
            log_dir / "app.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        app_handler.setLevel(logging.INFO)
        app_handler.setFormatter(json_formatter)
        
        error_handler = logging.handlers.RotatingFileHandler(
            log_dir / "error.log",
            maxBytes=10*1024*1024,
            backupCount=5
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(json_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(text_formatter)
        
        # Add handlers
        self.logger.addHandler(app_handler)
        self.logger.addHandler(error_handler)
        self.logger.addHandler(console_handler)
    
    def _log_json(self, level: str, message: str, extra: Optional[Dict] = None):
        """Log structured JSON"""
        log_entry = {
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
            "level": level
        }
        if extra:
            log_entry.update(extra)
        
        # Convert to JSON string for logging
        log_json = json.dumps(log_entry)
        
        if level == "ERROR":
            self.logger.error(log_json)
        elif level == "WARNING":
            self.logger.warning(log_json)
        else:
            self.logger.info(log_json)
    
    def info(self, message: str, **kwargs):
        self._log_json("INFO", message, kwargs)
    
    def warning(self, message: str, **kwargs):
        self._log_json("WARNING", message, kwargs)
    
    def error(self, message: str, exc_info: bool = False, **kwargs):
        if exc_info:
            kwargs["traceback"] = traceback.format_exc()
        self._log_json("ERROR", message, kwargs)
    
    def request(self, method: str, path: str, status: int, duration_ms: float, **kwargs):
        """Log API request"""
        self.info(
            f"{method} {path} - {status}",
            type="request",
            method=method,
            path=path,
            status=status,
            duration_ms=round(duration_ms, 2),
            **kwargs
        )

# Create global logger
logger = StructuredLogger("lrlre")

class RequestLogger:
    """Middleware for logging requests"""
    
    async def __call__(self, request, call_next):
        start_time = time.perf_counter()
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = (time.perf_counter() - start_time) * 1000
        
        # Log request
        logger.request(
            method=request.method,
            path=request.url.path,
            status=response.status_code,
            duration_ms=duration,
            client_host=request.client.host if request.client else None
        )
        
        return response
