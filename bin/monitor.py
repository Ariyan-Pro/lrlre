"""
LRLRE Enterprise Monitor - Check all 3 services
"""
import requests
import time
from datetime import datetime

def check_service(name, url):
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            return "✅ ONLINE"
        else:
            return f"⚠️  RESPONDING ({response.status_code})"
    except:
        return "❌ OFFLINE"

print("=" * 60)
print("📊 LRLRE ENTERPRISE GRID - SERVICE MONITOR")
print("=" * 60)
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("-" * 60)

services = [
    ("v7.0 Analysis Grid", "http://localhost:8007"),
    ("v8.2 Visual Grid", "http://localhost:8009"),
    ("v10.0 Ultimate Grid", "http://localhost:8013")
]

all_online = True
for name, url in services:
    status = check_service(name, url)
    if "❌" in status:
        all_online = False
    print(f"{name:20} : {status}")

print("-" * 60)

if all_online:
    print("🎉 ALL SERVICES OPERATIONAL - READY FOR PRODUCTION!")
    print("\n📌 Quick Access:")
    print("   • Analysis:  http://localhost:8007")
    print("   • Visual:    http://localhost:8009")
    print("   • Ultimate:  http://localhost:8013")
else:
    print("⚠️  Some services are offline - check individual terminals")
print("=" * 60)
