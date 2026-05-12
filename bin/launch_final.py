"""
LRLRE ENTERPRISE GRID LAUNCHER v2.0
Launch any of the 3 enterprise modes:
- v7.0: Analysis Grid (port 8007)
- v8.2: Visual Grid (port 8009) 
- v10.0: Ultimate Grid (port 8013)
"""
import subprocess
import sys
import os
import time

def print_header():
    print("=" * 80)
    print("🚀 LRLRE ENTERPRISE GRID - PRODUCTION LAUNCHER v2.0")
    print("=" * 80)
    print("📡 Symbolic NLP Engine | 5 Languages | <100MB Memory")
    print("=" * 80)

def check_port(port):
    """Check if port is available"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result != 0

def kill_port(port):
    """Kill process using port"""
    import subprocess
    import os
    
    if os.name == 'nt':  # Windows
        result = subprocess.run(f'netstat -ano | findstr :{port}', 
                               shell=True, capture_output=True, text=True)
        if result.stdout:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                parts = line.split()
                if len(parts) > 4:
                    pid = parts[4]
                    try:
                        subprocess.run(f'taskkill /F /PID {pid}', shell=True)
                        print(f"   Killed process {pid} on port {port}")
                    except:
                        pass

def main():
    print_header()
    
    print("\n🎯 ENTERPRISE GRID DEPLOYMENT OPTIONS:")
    print("-" * 60)
    print("1. 🧠 Launch v7.0 - Enterprise Analysis Grid")
    print("   (Deep text analysis, logical inference, entity detection)")
    print("   Port: 8007")
    print()
    print("2. ✨ Launch v8.2 - Enterprise Visual Grid")
    print("   (Bento Grid animations, flip cards, interactive UI)")
    print("   Port: 8009")
    print()
    print("3. 💎 Launch v10.0 - Enterprise Ultimate Grid")
    print("   (Complete package - Analysis + Visuals + Enterprise)")
    print("   Port: 8013")
    print()
    print("4. 🚪 Exit")
    print("-" * 60)
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == "1":
        port = 8007
        print(f"\n🔧 Preparing v7.0 Analysis Grid on port {port}...")
        
        # Kill existing process
        if not check_port(port):
            kill_port(port)
            time.sleep(1)
        
        # Run v7.0
        print(f"\n🚀 Starting v7.0 Analysis Grid...")
        print(f"   Access at: http://localhost:{port}")
        print("\n" + "=" * 60)
        subprocess.run([sys.executable, "start_analytics_v7.py"])
        
    elif choice == "2":
        port = 8009
        print(f"\n🔧 Preparing v8.2 Visual Grid on port {port}...")
        
        # Kill existing process
        if not check_port(port):
            kill_port(port)
            time.sleep(1)
        
        # Run v8.2
        print(f"\n🚀 Starting v8.2 Visual Grid...")
        print(f"   Access at: http://localhost:{port}")
        print("\n" + "=" * 60)
        subprocess.run([sys.executable, "start_analytics_v8_bento_grid.py"])
        
    elif choice == "3":
        port = 8013
        print(f"\n🔧 Preparing v10.0 Ultimate Grid on port {port}...")
        
        # Kill existing process
        if not check_port(port):
            kill_port(port)
            time.sleep(1)
        
        # Run v10.0
        print(f"\n🚀 Starting v10.0 Ultimate Grid...")
        print(f"   Access at: http://localhost:{port}")
        print("\n" + "=" * 60)
        subprocess.run([sys.executable, "ultimate_v10_fixed.py"])
        
    elif choice == "4":
        print("\n👋 Shutting down Enterprise Grid...")
        print("Thank you for using LRLRE!")
        return
        
    else:
        print("\n❌ Invalid option. Please select 1-4.")
        time.sleep(2)
        main()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Shutdown complete.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("\nPress Enter to exit...")
