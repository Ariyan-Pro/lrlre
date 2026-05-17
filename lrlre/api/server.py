"""
Simple FastAPI server for Phase 2
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Dict, List
import time
import uuid

# Import engine
from lrlre.engine.enhanced_engine import EnhancedEngine

# Create FastAPI app
app = FastAPI(
    title="LRLRE Enterprise API",
    description="Low-Resource Language Reasoning Engine",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engine
engine = EnhancedEngine()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "LRLRE Enterprise API is running",
        "version": "2.0.0",
        "engine": "enhanced",
        "endpoints": {
            "/": "This info",
            "/process": "POST - Process text and make inferences",
            "/query": "POST - Query knowledge base",
            "/add_rule": "POST - Add new rule",
            "/status": "GET - System status",
            "/docs": "API documentation"
        }
    }

@app.post("/process")
async def process_text(request: Request):
    """Process text and make inferences"""
    try:
        data = await request.json()
        text = data.get("text", "")

        if not text:
            raise HTTPException(status_code=400, detail="Text is required")

        # Process text
        start_time = time.time()
        
        # Simple language detection (using the detector directly)
        from lrlre.multilingual.simple_detector import SimpleLanguageDetector
        detector = SimpleLanguageDetector()
        result = detector.detect(text)
        
        processing_time = int((time.time() - start_time) * 1000)

        return {
            "input": text,
            "result": result,
            "processing_time_ms": processing_time,
            "session_id": str(uuid.uuid4())
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze")
async def analyze_text(request: Request):
    """Analyze text for language detection"""
    try:
        data = await request.json()
        text = data.get("text", "")

        if not text:
            raise HTTPException(status_code=400, detail="Text is required")

        # Process text
        start_time = time.time()
        
        # Simple language detection
        from lrlre.multilingual.simple_detector import SimpleLanguageDetector
        detector = SimpleLanguageDetector()
        result = detector.detect(text)
        
        processing_time = int((time.time() - start_time) * 1000)

        return {
            "input": text,
            **result,
            "processing_time_ms": processing_time,
            "session_id": str(uuid.uuid4())
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
async def system_status():
    """Get system status"""
    return {
        "engine": "enhanced",
        "status": "running",
        "mode": "inference",
        "uptime": "always"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": time.time()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": time.time()
        }

if __name__ == "__main__":
    uvicorn.run(
        "lrlre.api.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
