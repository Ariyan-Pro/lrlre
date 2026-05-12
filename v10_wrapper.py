"""
LRLRE v10.0 Ultimate Grid - Docker Wrapper
Exports the FastAPI app properly for uvicorn
"""
import sys
import os
from pathlib import Path
import importlib.util

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import the original module
import ultimate_v10_fixed

# Check what's available
if hasattr(ultimate_v10_fixed, 'app'):
    app = ultimate_v10_fixed.app
    print("Using existing app")
elif hasattr(ultimate_v10_fixed, 'application'):
    app = ultimate_v10_fixed.application
    print("Using application")
else:
    # Create a simple app
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse
    
    app = FastAPI(title="LRLRE v10.0 Ultimate Grid")
    
    # Try to get HTML content
    html_content = None
    if hasattr(ultimate_v10_fixed, 'HTML_TEMPLATE'):
        html_content = ultimate_v10_fixed.HTML_TEMPLATE
    else:
        # Search for HTML in file
        import inspect
        source = inspect.getsource(ultimate_v10_fixed)
        if 'HTML_TEMPLATE = """' in source:
            start = source.find('HTML_TEMPLATE = """') + 18
            end = source.find('"""', start)
            html_content = source[start:end]
    
    if html_content:
        @app.get("/")
        async def root():
            return HTMLResponse(content=html_content)
        print("Using extracted HTML template")
    else:
        @app.get("/")
        async def root():
            return HTMLResponse(content="<h1>LRLRE v10.0 Ultimate Grid</h1><p>System Ready</p>")
        print("Using fallback HTML")

print("v10.0 Ultimate Grid ready on port 8013")
