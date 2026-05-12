"""
LRLRE Security Module - API Keys, Rate Limiting, Request Validation
"""
import secrets
import time
from fastapi import Request, HTTPException
from typing import Dict, Optional
from collections import defaultdict
import hashlib

# Generate secure API key (in production, use environment variable)
API_KEY = secrets.token_urlsafe(32)
print(f"🔑 Generated API Key: {API_KEY}")

class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = defaultdict(list)
    
    def is_allowed(self, client_id: str) -> bool:
        """Check if request is allowed"""
        now = time.time()
        minute_ago = now - 60
        
        # Clean old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if req_time > minute_ago
        ]
        
        # Check rate limit
        if len(self.requests[client_id]) >= self.requests_per_minute:
            return False
        
        # Add current request
        self.requests[client_id].append(now)
        return True
    
    def get_remaining(self, client_id: str) -> int:
        """Get remaining requests"""
        now = time.time()
        minute_ago = now - 60
        recent = sum(1 for t in self.requests[client_id] if t > minute_ago)
        return max(0, self.requests_per_minute - recent)

# Global rate limiter
rate_limiter = RateLimiter()

class RequestValidator:
    """Validate incoming requests"""
    
    MAX_TEXT_LENGTH = 10000  # 10k chars max
    MAX_LINE_LENGTH = 1000    # 1k chars per line
    
    @classmethod
    def validate_text(cls, text: str) -> Optional[str]:
        """Validate text input, return error message if invalid"""
        if not text or not text.strip():
            return "Empty text provided"
        
        if len(text) > cls.MAX_TEXT_LENGTH:
            return f"Text too long: {len(text)} chars (max {cls.MAX_TEXT_LENGTH})"
        
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if len(line) > cls.MAX_LINE_LENGTH:
                return f"Line {i+1} too long: {len(line)} chars (max {cls.MAX_LINE_LENGTH})"
        
        # Check for null bytes
        if '\x00' in text:
            return "Text contains null bytes"
        
        return None
    
    @classmethod
    def sanitize_text(cls, text: str) -> str:
        """Sanitize text input"""
        # Remove control characters (except newlines/tabs)
        sanitized = ''.join(char for char in text 
                          if char == '\n' or char == '\t' or ord(char) >= 32)
        return sanitized.strip()

async def verify_api_key(request: Request):
    """Verify API key middleware"""
    # Skip for public endpoints
    if request.url.path in ["/", "/docs", "/openapi.json"]:
        return True
    
    # Get API key from header
    api_key = request.headers.get("x-api-key")
    
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="Missing API key. Include x-api-key header"
        )
    
    # In production, validate against stored keys
    # For now, compare with generated key
    if api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    
    # Rate limiting based on API key hash
    client_id = hashlib.sha256(api_key.encode()).hexdigest()
    if not rate_limiter.is_allowed(client_id):
        remaining = rate_limiter.get_remaining(client_id)
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. {remaining} requests remaining this minute"
        )
    
    return True

async def add_security_headers(request: Request, call_next):
    """Add security headers to all responses"""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response
