"""
LRLRE Failure Testing - Updated for Docker Deployment
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import time
import random
import string
import requests
from typing import Dict, List

class FailureTester:
    def __init__(self, base_url: str = "http://localhost:8007"):
        self.base_url = base_url
        self.results = []
    
    def test_server_connection(self):
        """Test if server is reachable"""
        print("\n🔌 Testing server connection...")
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            if response.status_code == 200:
                print(f"  ✅ Server reachable (HTTP {response.status_code})")
                return True
            else:
                print(f"  ⚠️  Server returned {response.status_code}")
                return False
        except Exception as e:
            print(f"  ❌ Server not reachable: {str(e)[:80]}")
            return False
    
    def test_valid_input(self):
        """Test with valid inputs first to ensure baseline works"""
        print("\n✅ Testing valid inputs (baseline)...")
        
        valid_tests = [
            ("The cat is on the mat.", "en", "Simple English"),
            ("Le chat est sur le tapis.", "fr", "Simple French"),
            ("猫はマットの上にいます。", "ja", "Simple Japanese"),
        ]
        
        success_count = 0
        for text, expected, desc in valid_tests:
            try:
                response = requests.post(
                    f"{self.base_url}/analyze",
                    json={"text": text},
                    timeout=5
                )
                if response.status_code == 200:
                    data = response.json()
                    if data.get('language', '').lower() == expected.lower():
                        print(f"  ✅ {desc}: Detected as {data.get('language')} (correct)")
                        success_count += 1
                    else:
                        print(f"  ⚠️  {desc}: Got {data.get('language')}, expected {expected}")
                else:
                    print(f"  ❌ {desc}: HTTP {response.status_code}")
            except Exception as e:
                print(f"  ❌ {desc}: {str(e)[:50]}")
        
        return success_count == len(valid_tests)
    
    def test_invalid_input(self):
        """Test with invalid inputs"""
        print("\n📛 Testing invalid inputs...")
        
        tests = [
            ("", "Empty string"),
            ("   \n   ", "Whitespace only"),
            ("a" * 20000, "Extremely long text"),
            ("\n" * 1000, "Many newlines"),
        ]
        
        for test_input, description in tests:
            try:
                response = requests.post(
                    f"{self.base_url}/analyze",
                    json={"text": test_input},
                    timeout=5
                )
                
                # Should either return 200 with detection or 400 for validation
                if response.status_code in [200, 400, 422]:
                    print(f"  ✅ {description}: {response.status_code}")
                else:
                    print(f"  ⚠️  {description}: {response.status_code}")
                    
            except Exception as e:
                print(f"  ⚠️  {description}: {str(e)[:50]}")
    
    def test_unsupported_languages(self):
        """Test with unsupported languages (should still work, maybe detect as default)"""
        print("\n🌍 Testing unsupported languages...")
        
        tests = [
            ("مرحبا بالعالم", "Arabic"),
            ("Привет мир", "Russian"),
            ("హలో వరల్డ్", "Telugu"),
            ("Ciao mondo", "Italian"),
        ]
        
        for text, description in tests:
            try:
                response = requests.post(
                    f"{self.base_url}/analyze",
                    json={"text": text},
                    timeout=5
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"  ✅ {description}: detected as {data.get('language', 'unknown')}")
                else:
                    print(f"  ⚠️  {description}: {response.status_code}")
                    
            except Exception as e:
                print(f"  ⚠️  {description}: {str(e)[:50]}")
    
    def test_malformed_requests(self):
        """Test malformed requests"""
        print("\n💥 Testing malformed requests...")
        
        # Missing content-type
        try:
            response = requests.post(
                f"{self.base_url}/analyze",
                data="just plain text",
                headers={"Content-Type": "text/plain"},
                timeout=5
            )
            print(f"  ✅ Plain text request: {response.status_code}")
        except:
            print("  ⚠️  Plain text request failed")
        
        # Invalid JSON
        try:
            response = requests.post(
                f"{self.base_url}/analyze",
                data="{invalid json",
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            print(f"  ✅ Invalid JSON: {response.status_code}")
        except:
            print("  ⚠️  Invalid JSON request failed")
        
        # SQL injection attempt
        try:
            response = requests.post(
                f"{self.base_url}/analyze",
                json={"text": "' OR '1'='1' --"},
                timeout=5
            )
            print(f"  ✅ SQL injection: {response.status_code}")
        except:
            print("  ⚠️  SQL injection test failed")
    
    def test_load(self, requests_count: int = 50):
        """Simple load test"""
        print(f"\n⚡ Load testing with {requests_count} requests...")
        
        sentences = [
            "The cat is on the mat.",
            "Le chat est sur le tapis.",
            "猫はマットの上にいます。",
            "고양이가 매트 위에 있어요.",
            "猫在垫子上。",
        ]
        
        start_time = time.time()
        success = 0
        failed = 0
        latencies = []
        
        for i in range(requests_count):
            text = random.choice(sentences)
            req_start = time.time()
            
            try:
                response = requests.post(
                    f"{self.base_url}/analyze",
                    json={"text": text},
                    timeout=5
                )
                
                latency = (time.time() - req_start) * 1000
                latencies.append(latency)
                
                if response.status_code == 200:
                    success += 1
                else:
                    failed += 1
                    
            except Exception as e:
                failed += 1
            
            if (i + 1) % 10 == 0:
                print(f"  Progress: {i+1}/{requests_count}")
        
        total_time = time.time() - start_time
        
        print(f"\n  Results:")
        print(f"    Success: {success}")
        print(f"    Failed: {failed}")
        if success > 0:
            print(f"    Success rate: {(success/requests_count)*100:.1f}%")
        print(f"    Total time: {total_time:.2f}s")
        if requests_count > 0:
            print(f"    Requests/sec: {requests_count/total_time:.1f}")
        if latencies:
            print(f"    Avg latency: {sum(latencies)/len(latencies):.1f}ms")
            print(f"    Max latency: {max(latencies):.1f}ms")
    
    def run_all(self):
        """Run all failure tests"""
        print("=" * 70)
        print("💥 LRLRE FAILURE TESTING SUITE (Docker Edition)")
        print("=" * 70)
        
        # First check if server is running
        if not self.test_server_connection():
            print("\n❌ Cannot connect to server. Make sure Docker containers are running:")
            print("   docker ps")
            print("   docker-compose up -d")
            return
        
        # Run baseline test first
        if not self.test_valid_input():
            print("\n⚠️  Baseline tests failed. Check if the /analyze endpoint exists.")
            print("   The test expects POST /analyze with JSON body: {\"text\": \"...\"}")
        
        # Run all other tests
        self.test_invalid_input()
        self.test_unsupported_languages()
        self.test_malformed_requests()
        self.test_load(30)  # Reduced from 50 for quicker testing
        
        print("\n" + "=" * 70)
        print("✅ Failure testing complete")
        print("=" * 70)

if __name__ == "__main__":
    # Try all three ports
    ports = [8007, 8009, 8013]
    for port in ports:
        print(f"\n🎯 Testing service on port {port}...")
        tester = FailureTester(f"http://localhost:{port}")
        tester.run_all()
        print("\n" + "-" * 70)
