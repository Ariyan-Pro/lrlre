"""
🚀 LRLRE ENTERPRISE GRID - SYSTEM VERIFICATION SCRIPT
Run this to verify the entire system is production-ready.
"""
import os
import sys
import subprocess
import time
from datetime import datetime

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f"🔍 {text}")
    print("=" * 80)

def run_test(test_name, test_func):
    """Run a test and report results."""
    print(f"\n🧪 {test_name}...")
    try:
        result = test_func()
        if result:
            print(f"✅ {test_name}: PASSED")
            return True
        else:
            print(f"❌ {test_name}: FAILED")
            return False
    except Exception as e:
        print(f"💥 {test_name}: ERROR - {e}")
        return False

def test_imports():
    """Test that all critical imports work."""
    try:
        from lrlre.multilingual.simple_detector import SimpleLanguageDetector
        from lrlre.symbols.persistence import init_db, check_database_health
        from lrlre.symbols.graph import SymbolGraph
        from lrlre.inference.pattern_engine import PatternEngine
        return True
    except Exception as e:
        print(f"   Import error: {e}")
        return False

def test_language_detection():
    """Test language detection with all 5 languages."""
    try:
        from lrlre.multilingual.simple_detector import SimpleLanguageDetector
        detector = SimpleLanguageDetector()
        
        tests = [
            ("Hello world", "en"),
            ("こんにちは", "ja"),
            ("안녕하세요", "ko"),
            ("你好", "zh"),
            ("Bonjour", "fr")
        ]
        
        all_pass = True
        for text, expected in tests:
            result = detector.detect(text)
            if result['language'] != expected:
                print(f"   Failed: '{text}' -> {result['language']} (expected {expected})")
                all_pass = False
        
        return all_pass
    except Exception as e:
        print(f"   Language detection error: {e}")
        return False

def test_database():
    """Test database connectivity and operations."""
    try:
        from lrlre.symbols.persistence import init_db, add_fact, get_all_facts, check_database_health
        
        # Initialize database
        engine = init_db()
        
        # Add a test fact
        fact_id = add_fact("test", "is", "working", confidence=1.0)
        
        # Check database health
        health = check_database_health()
        
        return fact_id is not None and health['status'] == 'healthy'
    except Exception as e:
        print(f"   Database error: {e}")
        return False

def test_ports():
    """Test that required ports are available."""
    import socket
    
    ports = [8007, 8009, 8013]
    all_available = True
    
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            
            if result == 0:
                print(f"   Port {port} is in use")
                all_available = False
        except:
            pass
    
    return all_available

def test_file_integrity():
    """Check that all critical files exist and are readable."""
    critical_files = [
        "launch_final.py",
        "start_analytics_v7.py",
        "start_analytics_v8_bento_grid.py",
        "ultimate_v10_fixed.py",
        "requirements.txt",
        "lrlre/__init__.py",
        "lrlre/multilingual/simple_detector.py",
        "lrlre/symbols/persistence.py",
        "lrlre/symbols/graph.py",
        "lrlre/inference/__init__.py"
    ]
    
    all_exist = True
    for file in critical_files:
        if not os.path.exists(file):
            print(f"   Missing: {file}")
            all_exist = False
        elif not os.access(file, os.R_OK):
            print(f"   Not readable: {file}")
            all_exist = False
    
    return all_exist

def test_requirements():
    """Check that requirements can be installed."""
    try:
        # Try to import key dependencies
        import fastapi
        import uvicorn
        import sqlalchemy
        import networkx
        import pydantic
        import yaml
        return True
    except ImportError as e:
        print(f"   Missing dependency: {e}")
        return False

def main():
    """Run all verification tests."""
    print("🚀 LRLRE ENTERPRISE GRID - PRODUCTION VERIFICATION")
    print("=" * 80)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python: {sys.version}")
    print(f"Working Directory: {os.getcwd()}")
    print("=" * 80)
    
    tests = [
        ("File Integrity Check", test_file_integrity),
        ("Import Test", test_imports),
        ("Language Detection", test_language_detection),
        ("Database System", test_database),
        ("Port Availability", test_ports),
        ("Dependencies", test_requirements)
    ]
    
    results = []
    for test_name, test_func in tests:
        passed = run_test(test_name, test_func)
        results.append((test_name, passed))
        time.sleep(0.5)  # Small delay for readability
    
    # Summary
    print_header("VERIFICATION SUMMARY")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    print(f"\n📊 Results: {passed_count}/{total_count} tests passed")
    print("-" * 40)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print("-" * 40)
    
    if passed_count == total_count:
        print("\n🎉 ENTERPRISE GRID VERIFICATION: COMPLETE SUCCESS")
        print("   System is PRODUCTION READY for deployment.")
        print("\nNext steps:")
        print("   1. Run: python launch_final.py")
        print("   2. Choose deployment option")
        print("   3. Access dashboard at http://localhost:[port]")
    else:
        print(f"\n⚠️  ENTERPRISE GRID VERIFICATION: {total_count - passed_count} ISSUES FOUND")
        print("   Please fix the failed tests before deployment.")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    try:
        main()
        input("\nPress Enter to exit...")
    except KeyboardInterrupt:
        print("\n\n⚠️  Verification interrupted by user")
    except Exception as e:
        print(f"\n💥 Critical error during verification: {e}")
        input("\nPress Enter to exit...")


