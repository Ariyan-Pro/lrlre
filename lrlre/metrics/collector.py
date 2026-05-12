"""
LRLRE Metrics System - Real performance measurements
"""
import time
import statistics
from datetime import datetime
from typing import Dict, List, Optional
from collections import deque
import threading

class MetricsCollector:
    """Collect real performance metrics"""
    
    def __init__(self, window_size: int = 1000):
        self.window_size = window_size
        self.latencies = deque(maxlen=window_size)
        self.inference_times = deque(maxlen=window_size)
        self.db_times = deque(maxlen=window_size)
        self.request_count = 0
        self.error_count = 0
        self.start_time = time.time()
        self.lock = threading.Lock()
    
    def record_request(self, 
                      latency_ms: float,
                      inference_ms: Optional[float] = None,
                      db_ms: Optional[float] = None,
                      success: bool = True):
        """Record a request with real measurements"""
        with self.lock:
            self.latencies.append(latency_ms)
            if inference_ms:
                self.inference_times.append(inference_ms)
            if db_ms:
                self.db_times.append(db_ms)
            self.request_count += 1
            if not success:
                self.error_count += 1
    
    def get_stats(self) -> Dict:
        """Get current statistics"""
        with self.lock:
            latencies = list(self.latencies)
            
            stats = {
                "requests_total": self.request_count,
                "errors_total": self.error_count,
                "error_rate": round(self.error_count / max(1, self.request_count), 4),
                "uptime_seconds": round(time.time() - self.start_time, 2),
                "latency_ms": {
                    "avg": round(statistics.mean(latencies), 2) if latencies else 0,
                    "min": round(min(latencies), 2) if latencies else 0,
                    "max": round(max(latencies), 2) if latencies else 0,
                    "p95": round(self._percentile(latencies, 95), 2) if latencies else 0,
                    "p99": round(self._percentile(latencies, 99), 2) if latencies else 0
                }
            }
            
            if self.inference_times:
                stats["inference_ms"] = {
                    "avg": round(statistics.mean(self.inference_times), 2),
                    "p95": round(self._percentile(list(self.inference_times), 95), 2)
                }
            
            if self.db_times:
                stats["db_ms"] = {
                    "avg": round(statistics.mean(self.db_times), 2),
                    "p95": round(self._percentile(list(self.db_times), 95), 2)
                }
            
            return stats
    
    def _percentile(self, data: List[float], percentile: float) -> float:
        """Calculate percentile"""
        if not data:
            return 0
        sorted_data = sorted(data)
        k = (len(sorted_data) - 1) * percentile / 100
        f = int(k)
        c = int(k) + 1 if f < len(sorted_data) - 1 else f
        return sorted_data[f] + (sorted_data[c] - sorted_data[f]) * (k - f)

# Global metrics instance
metrics = MetricsCollector()

def get_timing_context() -> Dict:
    """Get timing context for request processing"""
    return {
        "request_start": time.perf_counter(),
        "db_start": None,
        "inference_start": None
    }
