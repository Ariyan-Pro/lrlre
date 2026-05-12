"""
LRLRE COMPLETE TEST SUITE - WebSocket Edition
Tests all 5 languages with real WebSocket communication
"""
import asyncio
import json
import time
import websockets
import statistics
from datetime import datetime
from typing import Dict, List

class LRLRETester:
    def __init__(self, port: int):
        self.ws_url = f"ws://localhost:{port}/ws"
        self.results = []
    
    async def test_connection(self):
        """Test WebSocket connection"""
        try:
            async with websockets.connect(self.ws_url) as websocket:
                return True
        except Exception as e:
            print(f"  ❌ Connection failed: {e}")
            return False
    
    async def analyze_text(self, text: str) -> Dict:
        """Send text to WebSocket and get response"""
        start_time = time.perf_counter()
        
        try:
            async with websockets.connect(self.ws_url) as websocket:
                # Send the text
                await websocket.send(json.dumps({"text": text}))
                
                # Wait for response
                response = await asyncio.wait_for(websocket.recv(), timeout=10)
                
                latency = (time.perf_counter() - start_time) * 1000
                
                data = json.loads(response)
                return {
                    "success": True,
                    "data": data,
                    "latency_ms": latency
                }
        except asyncio.TimeoutError:
            return {
                "success": False,
                "error": "Timeout",
                "latency_ms": (time.perf_counter() - start_time) * 1000
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "latency_ms": (time.perf_counter() - start_time) * 1000
            }
    
    async def run_tests(self):
        """Run complete test suite"""
        print("=" * 70)
        print(f"🧪 LRLRE TEST SUITE - Port {self.ws_url.split(':')[-1]}")
        print("=" * 70)
        
        # Test connection first
        print("\n🔌 Testing WebSocket connection...")
        if not await self.test_connection():
            print("❌ Cannot connect. Make sure server is running.")
            return
        
        print("✅ WebSocket connected")
        
        # Test cases with expected languages
        test_cases = [
            # English
            ("The cat is on the mat. The cat likes fish.", "en", "English - Simple"),
            ("I would like to order a pizza please.", "en", "English - Request"),
            ("What time does the train depart from the station?", "en", "English - Question"),
            
            # French
            ("Le chat est sur le tapis. Le chat aime le poisson.", "fr", "French - Simple"),
            ("Je voudrais commander une pizza s'il vous plaît.", "fr", "French - Request"),
            ("À quelle heure le train part-il de la gare?", "fr", "French - Question"),
            
            # Japanese
            ("猫はマットの上にいます。猫は魚が好きです。", "ja", "Japanese - Simple"),
            ("ピザを注文したいです。", "ja", "Japanese - Request"),
            ("電車は何時に駅を出発しますか？", "ja", "Japanese - Question"),
            
            # Korean
            ("고양이가 매트 위에 있어요. 고양이는 생선을 좋아해요.", "ko", "Korean - Simple"),
            ("피자를 주문하고 싶습니다.", "ko", "Korean - Request"),
            ("기차는 몇 시에 역에서 출발하나요?", "ko", "Korean - Question"),
            
            # Chinese
            ("猫在垫子上。猫喜欢鱼。", "zh", "Chinese - Simple"),
            ("我想点一份披萨。", "zh", "Chinese - Request"),
            ("火车什么时候从车站出发？", "zh", "Chinese - Question"),
        ]
        
        results = []
        latencies = []
        languages_detected = {"en": 0, "fr": 0, "ja": 0, "ko": 0, "zh": 0}
        languages_correct = {"en": 0, "fr": 0, "ja": 0, "ko": 0, "zh": 0}
        
        print("\n📊 Running tests...")
        print("-" * 70)
        
        for text, expected, description in test_cases:
            result = await self.analyze_text(text)
            
            if result["success"]:
                data = result["data"]
                detected = data.get("language", "unknown").lower()
                confidence = data.get("confidence", 0)
                latency = result["latency_ms"]
                latencies.append(latency)
                
                is_correct = (detected == expected)
                
                # Update stats
                languages_detected[expected] += 1
                if is_correct:
                    languages_correct[expected] += 1
                
                status = "✅" if is_correct else "❌"
                print(f"{status} {description:30} → {detected.upper():3} ({confidence:.0f}%) in {latency:.1f}ms")
                
                results.append({
                    "text": text[:50],
                    "expected": expected,
                    "detected": detected,
                    "confidence": confidence,
                    "latency": latency,
                    "correct": is_correct
                })
            else:
                print(f"❌ {description:30} → ERROR: {result['error']}")
                results.append({
                    "text": text[:50],
                    "expected": expected,
                    "error": result['error'],
                    "correct": False
                })
            
            await asyncio.sleep(0.5)  # Small delay between requests
        
        # Calculate accuracy per language
        print("\n" + "=" * 70)
        print("📈 ACCURACY BY LANGUAGE")
        print("-" * 70)
        
        total_correct = 0
        total_tests = 0
        
        for lang, detected in languages_detected.items():
            correct = languages_correct[lang]
            accuracy = (correct / detected * 100) if detected > 0 else 0
            total_correct += correct
            total_tests += detected
            
            lang_names = {"en": "English", "fr": "French", "ja": "Japanese", "ko": "Korean", "zh": "Chinese"}
            print(f"  {lang_names.get(lang, lang).ljust(10)}: {correct}/{detected} ({accuracy:.1f}%)")
        
        overall_accuracy = (total_correct / total_tests * 100) if total_tests > 0 else 0
        
        print("\n" + "=" * 70)
        print("📊 PERFORMANCE METRICS")
        print("-" * 70)
        
        if latencies:
            print(f"  Total tests:        {len(results)}")
            print(f"  Successful:         {sum(1 for r in results if r.get('correct', False))}")
            print(f"  Failed:             {sum(1 for r in results if not r.get('correct', False))}")
            print(f"  Overall accuracy:   {overall_accuracy:.1f}%")
            print(f"\n  Latency (ms):")
            print(f"    Avg:              {statistics.mean(latencies):.1f}")
            print(f"    Min:              {min(latencies):.1f}")
            print(f"    Max:              {max(latencies):.1f}")
            print(f"    P95:              {statistics.quantiles(latencies, n=20)[18]:.1f}")
        
        print("\n" + "=" * 70)
        print("✅ TEST SUITE COMPLETE")
        print("=" * 70)
        
        return results

async def test_all_ports():
    """Test all three services"""
    ports = [8007, 8009, 8013]
    
    for port in ports:
        print(f"\n{'='*70}")
        print(f"🎯 TESTING LRLRE SERVICE ON PORT {port}")
        print(f"{'='*70}")
        
        tester = LRLRETester(port)
        await tester.run_tests()
        
        print("\n" + " " * 70)
        await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(test_all_ports())
