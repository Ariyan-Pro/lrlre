"""
LRLRE v8.2 - ENTERPRISE VISUAL GRID
COMPLETE VERSION - Bento Grid, Animations, Interactive UI
"""
import os
import sys
from pathlib import Path
import time
import json
import asyncio
import logging
from typing import Dict, Any

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
import uvicorn

# LRLRE imports
from lrlre.multilingual.simple_detector import SimpleLanguageDetector
from lrlre.multilingual.internet_reference import InternetReferenceSystem

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(title="LRLRE v8.2 - Enterprise Visual Grid")

# Initialize components
detector = SimpleLanguageDetector()
reference_system = InternetReferenceSystem()

# HTML Template - Complete Visual Grid
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LRLRE v8.2 - Enterprise Visual Grid</title>
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
            animation: fadeIn 1s ease;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 40px;
        }
        
        .stat-card {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            animation: slideUp 0.5s ease;
            transition: transform 0.3s;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
        }
        
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }
        
        .bento-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-bottom: 40px;
        }
        
        .bento-item {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            animation: scaleIn 0.5s ease;
            transition: all 0.3s;
            cursor: pointer;
        }
        
        .bento-item:hover {
            transform: scale(1.02);
            background: rgba(255,255,255,0.15);
        }
        
        @keyframes scaleIn {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }
        
        .bento-item.large {
            grid-column: span 2;
        }
        
        .input-area {
            grid-column: span 2;
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
        
        .btn {
            padding: 12px 30px;
            border: none;
            border-radius: 25px;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            margin-right: 10px;
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
            margin: 20px 0;
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
            transform: translateY(-2px);
        }
        
        .flag-container {
            display: flex;
            gap: 15px;
            margin: 20px 0;
            flex-wrap: wrap;
        }
        
        .flag {
            font-size: 32px;
            cursor: pointer;
            transition: transform 0.3s;
            filter: drop-shadow(0 5px 10px rgba(0,0,0,0.3));
        }
        
        .flag:hover {
            transform: scale(1.2);
        }
        
        .result-card {
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
            padding: 15px;
            margin-top: 15px;
        }
        
        .language-badge {
            display: inline-block;
            padding: 8px 20px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 25px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .confidence-bar {
            width: 100%;
            height: 10px;
            background: rgba(255,255,255,0.1);
            border-radius: 5px;
            margin: 10px 0;
            overflow: hidden;
        }
        
        .confidence-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            transition: width 0.5s;
        }
        
        .chart-container {
            height: 200px;
            margin-top: 20px;
        }
        
        .theme-selector {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(255,255,255,0.1);
            border-radius: 30px;
            padding: 10px;
            backdrop-filter: blur(10px);
            display: flex;
            gap: 10px;
            z-index: 1000;
        }
        
        .theme-btn {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            border: none;
            cursor: pointer;
            transition: transform 0.3s;
        }
        
        .theme-btn:hover {
            transform: scale(1.2);
        }
        
        .theme-purple { background: linear-gradient(135deg, #667eea, #764ba2); }
        .theme-blue { background: linear-gradient(135deg, #2193b0, #6dd5ed); }
        .theme-green { background: linear-gradient(135deg, #11998e, #38ef7d); }
        
        .mouse-effect {
            position: fixed;
            width: 20px;
            height: 20px;
            background: rgba(255,255,255,0.3);
            border-radius: 50%;
            pointer-events: none;
            transition: transform 0.1s;
            z-index: 9999;
        }
        
        .footer {
            text-align: center;
            margin-top: 50px;
            color: rgba(255,255,255,0.5);
            animation: fadeIn 1s ease;
        }
    </style>
</head>
<body>
    <div class="mouse-effect" id="mouseEffect"></div>
    
    <div class="container">
        <div class="header">
            <h1>🎯 LRLRE v8.2 - Enterprise Visual Grid</h1>
            <p>Bento Grid Animations • Flip Cards • Interactive UI</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value" id="totalRequests">0</div>
                <div>Total Requests</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="avgSpeed">0ms</div>
                <div>Avg Speed</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="activeUsers">1</div>
                <div>Active Users</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="languages">5</div>
                <div>Languages</div>
            </div>
        </div>
        
        <div class="bento-grid">
            <!-- Input Area -->
            <div class="bento-item input-area">
                <h3>📝 Text Analysis Input</h3>
                <textarea id="textInput" rows="4" placeholder="Enter text to analyze..."></textarea>
                
                <div>
                    <button class="btn" onclick="analyzeText()">Complete Analysis</button>
                    <button class="btn btn-secondary" onclick="clearText()">Clear</button>
                </div>
                
                <div class="samples">
                    <button class="sample-btn" onclick="loadSample('en')">🇬🇧 English</button>
                    <button class="sample-btn" onclick="loadSample('ja')">🇯🇵 Japanese</button>
                    <button class="sample-btn" onclick="loadSample('ko')">🇰🇷 Korean</button>
                    <button class="sample-btn" onclick="loadSample('zh')">🇨🇳 Chinese</button>
                    <button class="sample-btn" onclick="loadSample('fr')">🇫🇷 French</button>
                </div>
                
                <div class="flag-container">
                    <span class="flag" onclick="loadSample('en')">🇬🇧</span>
                    <span class="flag" onclick="loadSample('ja')">🇯🇵</span>
                    <span class="flag" onclick="loadSample('ko')">🇰🇷</span>
                    <span class="flag" onclick="loadSample('zh')">🇨🇳</span>
                    <span class="flag" onclick="loadSample('fr')">🇫🇷</span>
                </div>
            </div>
            
            <!-- Detection Results -->
            <div class="bento-item">
                <h3>🔍 Detection Results</h3>
                <div id="detectionResults">
                    <div class="language-badge">Waiting for input...</div>
                </div>
            </div>
            
            <!-- Confidence Card -->
            <div class="bento-item">
                <h3>📊 Confidence Level</h3>
                <div class="confidence-bar">
                    <div class="confidence-fill" id="confidenceFill" style="width: 0%"></div>
                </div>
                <div id="confidenceValue">0%</div>
            </div>
            
            <!-- Stats Card -->
            <div class="bento-item">
                <h3>📈 Statistics</h3>
                <div id="stats">Characters: 0<br>Words: 0<br>Lines: 0</div>
            </div>
            
            <!-- Scripts Card -->
            <div class="bento-item">
                <h3>📜 Scripts Detected</h3>
                <div id="scriptsList">-</div>
            </div>
            
            <!-- Language Info Card -->
            <div class="bento-item">
                <h3>🌍 Language Info</h3>
                <div id="languageInfo">
                    Family: -<br>
                    Speakers: -<br>
                    Script: -
                </div>
            </div>
            
            <!-- Chart Card -->
            <div class="bento-item large">
                <h3>📊 Language Distribution</h3>
                <canvas id="langChart" class="chart-container"></canvas>
            </div>
        </div>
    </div>
    
    <div class="theme-selector">
        <button class="theme-btn theme-purple" onclick="setTheme('purple')"></button>
        <button class="theme-btn theme-blue" onclick="setTheme('blue')"></button>
        <button class="theme-btn theme-green" onclick="setTheme('green')"></button>
    </div>
    
    <div class="footer">
        LRLRE v8.2 | Enterprise Visual Grid | Bento Animations
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        let ws = null;
        let totalRequests = 0;
        let chart = null;
        
        // Mouse effect
        document.addEventListener('mousemove', function(e) {
            const effect = document.getElementById('mouseEffect');
            effect.style.transform = `translate(${e.clientX - 10}px, ${e.clientY - 10}px)`;
        });
        
        function connectWebSocket() {
            ws = new WebSocket('ws://' + window.location.host + '/ws');
            
            ws.onopen = function() {
                console.log('WebSocket connected');
            };
            
            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                updateUI(data);
            };
            
            ws.onclose = function() {
                console.log('WebSocket disconnected, reconnecting...');
                setTimeout(connectWebSocket, 1000);
            };
        }
        
        function updateUI(data) {
            const flags = {'en':'🇬🇧','fr':'🇫🇷','ja':'🇯🇵','ko':'🇰🇷','zh':'🇨🇳'};
            const flag = flags[data.language] || '🌐';
            
            // Update detection
            document.getElementById('detectionResults').innerHTML = `
                <div class="language-badge">${flag} ${data.language_name} (${data.confidence}%)</div>
                <div>${data.characters} chars • ${data.words} words • ${data.lines} lines</div>
            `;
            
            // Update confidence
            document.getElementById('confidenceFill').style.width = data.confidence + '%';
            document.getElementById('confidenceValue').innerText = data.confidence + '%';
            
            // Update stats
            document.getElementById('stats').innerHTML = `
                Characters: ${data.characters}<br>
                Words: ${data.words}<br>
                Lines: ${data.lines}
            `;
            
            // Update scripts
            const scripts = data.scripts_detected || [];
            document.getElementById('scriptsList').innerText = scripts.join(', ') || '-';
            
            // Update language info
            if (data.language_info) {
                document.getElementById('languageInfo').innerHTML = `
                    Family: ${data.language_info.family || '-'}<br>
                    Speakers: ${data.language_info.speakers || '-'}<br>
                    Script: ${data.language_info.script || '-'}
                `;
            }
            
            // Update chart
            if (chart) {
                chart.data.datasets[0].data = [data.confidence, 100 - data.confidence];
                chart.update();
            }
            
            // Update counters
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
        
        function setTheme(theme) {
            const gradients = {
                'purple': 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)',
                'blue': 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)',
                'green': 'linear-gradient(135deg, #134e5e 0%, #71b280 100%)'
            };
            document.body.style.background = gradients[theme];
        }
        
        window.onload = function() {
            connectWebSocket();
            
            const ctx = document.getElementById('langChart').getContext('2d');
            chart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Confidence', 'Uncertainty'],
                    datasets: [{
                        data: [0, 100],
                        backgroundColor: ['#667eea', 'rgba(255,255,255,0.1)'],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            labels: {
                                color: '#fff'
                            }
                        }
                    }
                }
            });
        };
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
            
            # Calculate stats
            chars = len(text)
            words = len(text.split())
            lines = len(text.split('\n'))
            
            # Get language name
            lang_names = {'en':'English','fr':'French','ja':'Japanese','ko':'Korean','zh':'Chinese'}
            lang_name = lang_names.get(lang, 'Unknown')
            
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
                "processing_time": round((time.time() - start_time) * 1000, 2)
            }
            
            await websocket.send_json(response)
            
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        logger.info("WebSocket disconnected")

if __name__ == "__main__":
    print("=" * 80)
    print("🎯 LRLRE v8.2 - Enterprise Visual Grid")
    print("=" * 80)
    print("✨ Bento Grid Animations • Flip Cards • Interactive UI")
    print("🌐 5 Language Support: EN, FR, JA, KO, ZH")
    print("📊 Real-time WebSocket Updates")
    print("=" * 80)
    print("🚀 Starting on http://localhost:8009")
    print("=" * 80)
    
    uvicorn.run(app, host="0.0.0.0", port=8009)
