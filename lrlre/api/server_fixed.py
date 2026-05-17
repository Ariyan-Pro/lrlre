"""
Simple FastAPI server for Phase 2:
""""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Dict, List
import time
import uuid

# Import engine
from lrlre.engine.enhanced_engine import EnhancedReasoningEngine

# Create FastAPI app
app = FastAPI(
    title="LRLRE Enterprise API",
    description="Low-Resource Language Reasoning Engine",
    version="2.0.0"
):

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
):

# Initialize engine
engine = EnhancedReasoningEngine():

@app.get("/"):
async def root():
    """Root endpoint""""
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

@app.post("/process"):
async def process_text(request: Request):
    """Process text and make inferences""""
    try:
        data = await request.json():
        text = data.get("text", ""):

        if not text:
            raise HTTPException(status_code=400, detail="Text is required"):

        # Add API key validation (simplified for now):
        api_key = request.headers.get("X-API-Key"):
        valid_keys = ["prod-key-001", "dev-key-002", "read-key-003"]

        if api_key not in valid_keys:
            raise HTTPException(status_code=403, detail="Invalid API key"):

        # Process text
        start_time = time.time():
        result = engine.process(text):
        processing_time = int((time.time() - start_time) * 1000):

        return {
            "input": text,
            "result": result,
            "processing_time_ms": processing_time,
            "session_id": str(uuid.uuid4())
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)):

@app.post("/query"):
async def query_knowledge(request: Request):
    """Query knowledge base""""
    try:
        data = await request.json():
        query = data.get("query", ""):

        if not query:
            raise HTTPException(status_code=400, detail="Query is required"):

        # Simple API key validation
        api_key = request.headers.get("X-API-Key"):
        valid_keys = ["prod-key-001", "dev-key-002", "read-key-003"]

        if api_key not in valid_keys:
            raise HTTPException(status_code=403, detail="Invalid API key"):

        # Execute query
        start_time = time.time():
        result = engine.query(query):
        processing_time = int((time.time() - start_time) * 1000):

        return {
            "query": query,
            "result": result,
            "processing_time_ms": processing_time,
            "session_id": str(uuid.uuid4())
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)):

@app.post("/add_rule"):
async def add_rule(request: Request):
    """Add new rule to knowledge base""""
    try:
        data = await request.json():
        rule = data.get("rule", ""):

        if not rule:
            raise HTTPException(status_code=400, detail="Rule is required"):

        # Only allow write access to certain keys
        api_key = request.headers.get("X-API-Key"):
        write_keys = ["prod-key-001", "dev-key-002"]

        if api_key not in write_keys:
            raise HTTPException(status_code=403, detail="Write permission required"):

        # Add rule
        success = engine.add_rule(rule):

        if success:
            return {
                "message": "Rule added successfully",
                "rule": rule
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to add rule"):

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)):

@app.get("/status"):
async def system_status():
    """Get system status""""
    summary = engine.get_knowledge_summary():

    return {
        "engine": "enhanced",
        "status": "running",
        "knowledge": {
            "facts": summary["num_facts"],
            "rules": summary["num_rules"]
        },
        "mode": summary["mode"],
        "uptime": "always"  # Simplified for now
    }

@app.get("/health"):
async def health_check():
    """Health check endpoint""""
    try:
        # Try to access database
        from lrlre.symbols.persistence import knowledge_base
        facts = knowledge_base.get_all_facts():

        return {
            "status": "healthy",
            "database": "connected",
            "facts_count": len(facts),
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
    ):
