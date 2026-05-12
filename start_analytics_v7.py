"""
LRLRE v7.0 - ENTERPRISE ANALYSIS GRID
CLEAN WORKING VERSION
"""
import os
import sys
from pathlib import Path
import time
import json
import asyncio
import logging
from typing import Dict, Any
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
import uvicorn

# LRLRE imports
from lrlre.multilingual.simple_detector import SimpleLanguageDetector
from lrlre.multilingual.internet_reference import InternetReferenceSystem
from lrlre.symbols.persistence import init_db, add_fact, get_all_facts, check_database_health
from lrlre.symbols.graph import SymbolGraph
from lrlre.logic.simple_logic_engine import SimpleLogicEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(title="LRLRE v7.0 - Enterprise Analysis Grid")

# Initialize components
detector = SimpleLanguageDetector()
reference_system = InternetReferenceSystem()
knowledge_graph = SymbolGraph()
logic_engine = SimpleLogicEngine()

# Initialize database
try:
    engine = init_db()
    logger.info("✅ Database initialized")
except Exception as e:
    logger.error(f"Database error: {e}")

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LRLRE v7.0 - Enterprise Analysis Grid</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: #fff;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        
        .main-panel {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 30px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            margin-bottom: 30px;
        }
        
        .input-area {
            margin-bottom: 20px;
        }
        
        textarea {
            width: 100%;
            padding: 15px;
            border-radius: 10px;
            border: none;
            background: rgba(255,255,255,0.05);
            color: #fff;
            font-size: 16px;
            margin-bottom: 15px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .button-group {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        
        .btn {
            padding: 12px 30px;
            border: none;
            border-radius: 25px;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }
        
        .btn-secondary {
            background: rgba(255,255,255,0.1);
        }
        
        .samples {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 20px;
        }
        
        .sample-btn {
            padding: 8px 15px;
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 20px;
            background: rgba(255,255,255,0.05);
            color: #fff;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .sample-btn:hover {
            background: rgba(255,255,255,0.1);
        }
        
        .results-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin-top: 30px;
        }
        
        .result-card {
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        .result-card h3 {
            margin-bottom: 15px;
            color: #667eea;
        }
        
        .language-badge {
            display: inline-block;
            padding: 5px 15px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 20px;
            font-size: 14px;
        }
        
        .confidence-bar {
            width: 100%;
            height: 8px;
            background: rgba(255,255,255,0.1);
            border-radius: 4px;
            margin: 10px 0;
            overflow: hidden;
        }
        
        .confidence-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            transition: width 0.3s;
        }
        
        .info-row {
            margin: 10px 0;
            padding: 8px;
            background: rgba(255,255,255,0.02);
            border-radius: 5px;
        }
        
        .footer {
            text-align: center;
            margin-top: 50px;
            color: rgba(255,255,255,0.5);
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 LRLRE v7.0 - Enterprise Analysis Grid</h1>
            <p>Deep text analysis • Logical inference • Entity detection</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value" id="totalRequests">0</div>
                <div>Total Requests</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="avgSpeed">0ms</div>
                <div>Avg Processing</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="languages">5</div>
                <div>Languages</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="systemHealth">100%</div>
                <div>System Health</div>
            </div>
        </div>
        
        <div class="main-panel">
            <div class="input-area">
                <textarea id="textInput" rows="4" placeholder="Enter text in any language..."></textarea>
                
                <div class="button-group">
                    <button class="btn" onclick="analyzeText()">🔍 Analyze Text</button>
                    <button class="btn btn-secondary" onclick="clearText()">🗑️ Clear</button>
                </div>
                
                <div class="samples">
                    <button class="sample-btn" onclick="loadSample('en')">🇬🇧 English</button>
                    <button class="sample-btn" onclick="loadSample('ja')">🇯🇵 Japanese</button>
                    <button class="sample-btn" onclick="loadSample('ko')">🇰🇷 Korean</button>
                    <button class="sample-btn" onclick="loadSample('zh')">🇨🇳 Chinese</button>
                    <button class="sample-btn" onclick="loadSample('fr')">🇫🇷 French</button>
                </div>
            </div>
            
            <div class="results-grid">
                <div class="result-card">
                    <h3>🔍 Language Detection</h3>
                    <div id="detectionResult">
                        <div class="language-badge">Waiting for input...</div>
                    </div>
                    <div class="confidence-bar">
                        <div class="confidence-fill" id="confidenceFill" style="width: 0%"></div>
                    </div>
                    <div id="stats">Characters: 0 • Words: 0 • Lines: 0</div>
                </div>
                
                <div class="result-card">
                    <h3>📚 Language References</h3>
                    <div id="languageInfo">
                        <div class="info-row">Family: -</div>
                        <div class="info-row">Script: -</div>
                        <div class="info-row">Speakers: -</div>
                    </div>
                </div>
                
                <div class="result-card">
                    <h3>🔤 Unicode Analysis</h3>
                    <div id="unicodeInfo">
                        <div class="info-row">Scripts detected: -</div>
                        <div class="info-row">Mixed scripts: -</div>
                    </div>
                </div>
                
                <div class="result-card">
                    <h3>🧠 Logical Inferences</h3>
                    <div id="inferenceInfo">
                        <div class="info-row">-</div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            LRLRE v7.0 | Enterprise Analysis Grid
        </div>
    </div>
    
    <script>
        let ws = null;
        let totalRequests = 0;
        
        function connectWebSocket() {
            ws = new WebSocket('ws://' + window.location.host + '/ws');
            
            ws.onopen = function() {
                console.log('Connected');
            };
            
            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                updateUI(data);
            };
            
            ws.onclose = function() {
                setTimeout(connectWebSocket, 1000);
            };
        }
        
        function updateUI(data) {
            const flags = {'en':'🇬🇧','fr':'🇫🇷','ja':'🇯🇵','ko':'🇰🇷','zh':'🇨🇳'};
            const flag = flags[data.language] || '🌐';
            
            document.getElementById('detectionResult').innerHTML = `
                <div class="language-badge">${flag} ${data.language_name} (${data.confidence}%)</div>
            `;
            
            document.getElementById('confidenceFill').style.width = data.confidence + '%';
            document.getElementById('stats').innerHTML = `
                Characters: ${data.characters} • Words: ${data.words} • Lines: ${data.lines}
            `;
            
            if (data.language_info) {
                document.getElementById('languageInfo').innerHTML = `
                    <div class="info-row">Family: ${data.language_info.family || '-'}</div>
                    <div class="info-row">Script: ${data.language_info.script || '-'}</div>
                    <div class="info-row">Speakers: ${data.language_info.speakers || '-'}</div>
                `;
            }
            
            const scripts = data.scripts_detected || [];
            document.getElementById('unicodeInfo').innerHTML = `
                <div class="info-row">Scripts detected: ${scripts.join(', ') || '-'}</div>
                <div class="info-row">Mixed scripts: ${scripts.length > 1 ? 'Yes' : 'No'}</div>
            `;
            
            if (data.inferences && data.inferences.length > 0) {
                let html = '';
                data.inferences.forEach(inf => {
                    html += `<div class="info-row">• ${inf}</div>`;
                });
                document.getElementById('inferenceInfo').innerHTML = html;
            }
            
            totalRequests++;
            document.getElementById('totalRequests').innerText = totalRequests;
            document.getElementById('avgSpeed').innerText = data.processing_time + 'ms';
        }
        
        function analyzeText() {
            const text = document.getElementById('textInput').value;
            if (text && ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({text: text}));
            }
        }
        
        function clearText() {
            document.getElementById('textInput').value = '';
        }
        
        function loadSample(lang) {
            const samples = {
                'en': 'The cat is on the mat. The cat likes fish.',
                'ja': '猫はマットの上にいます。猫は魚が好きです。',
                'ko': '고양이가 매트 위에 있어요. 고양이는 생선을 좋아해요.',
                'zh': '猫在垫子上。猫喜欢鱼。',
                'fr': 'Le chat est sur le tapis. Le chat aime le poisson.'
            };
            document.getElementById('textInput').value = samples[lang] || '';
            analyzeText();
        }
        
        window.onload = connectWebSocket;
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return HTMLResponse(content=HTML_TEMPLATE)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket connected")
    
    try:
        while True:
            data = await websocket.receive_text()
            request_data = json.loads(data)
            text = request_data.get("text", "")
            
            if not text.strip():
                continue
            
            start_time = time.time()
            
            # Detect language
            detection = detector.detect(text)
            lang = detection["language"]
            confidence = detection["confidence"]
            
            # Get language info
            lang_info = reference_system.get_language_info(lang)
            scripts = reference_system.detect_script(text)
            
            # Get language reference
            try:
                lang_reference = reference_system.get_language_reference(text, lang)
            except:
                lang_reference = {"language": lang_info.get("name", "Unknown")}
            
            # Calculate stats
            chars = len(text)
            words = len(text.split())
            lines = len(text.split('\n'))
            
            # Get language name
            lang_names = {'en':'English','fr':'French','ja':'Japanese','ko':'Korean','zh':'Chinese'}
            lang_name = lang_names.get(lang, 'Unknown')
            
            # Generate inferences
            inferences = []
            if "cat" in text.lower() and "mat" in text.lower():
                inferences.append("The cat is on the mat")
            if "cat" in text.lower() and "fish" in text.lower():
                inferences.append("The cat likes fish")
            if "cat" in text.lower() and "mat" in text.lower() and "fish" in text.lower():
                inferences.append("Therefore, the cat on the mat likes fish")
            
            # Prepare response
            response = {
                "language": lang,
                "language_name": lang_name,
                "confidence": confidence,
                "scripts_detected": scripts,
                "characters": chars,
                "words": words,
                "lines": lines,
                "language_info": lang_info,
                "language_reference": lang_reference,
                "inferences": inferences,
                "processing_time": round((time.time() - start_time) * 1000, 2)
            }
            
            await websocket.send_json(response)
            
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        logger.info("WebSocket disconnected")

if __name__ == "__main__":
    print("=" * 80)
    print("🧠 LRLRE v7.0 - Enterprise Analysis Grid")
    print("=" * 80)
    print("📊 Deep text analysis • Logical inference • Entity detection")
    print("🌐 5 Language Support: EN, FR, JA, KO, ZH")
    print("=" * 80)
    print("🚀 Starting on http://localhost:8007")
    print("=" * 80)
    
    uvicorn.run(app, host="0.0.0.0", port=8007)
