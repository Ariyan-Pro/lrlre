"""
LRLRE ENTERPRISE GRID - FINAL LAUNCHER
No Unicode emoji - pure ASCII for Windows compatibility
"""
import subprocess
import sys
import os
import time

def print_header():
    print("=" * 80)
    print("LRLRE ENTERPRISE GRID - PRODUCTION LAUNCHER")
    print("=" * 80)
    print("Symbolic NLP Engine | 5 Languages | <100MB Memory")
    print("=" * 80)

def kill_port(port):
    """Kill process using port"""
    if os.name == 'nt':
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
                        print(f"   Killed process on port {port}")
                    except:
                        pass

def main():
    print_header()
    
    print("\nENTERPRISE GRID DEPLOYMENT OPTIONS:")
    print("-" * 60)
    print("1. Launch v7.0 - Enterprise Analysis Grid (port 8007)")
    print("2. Launch v8.2 - Enterprise Visual Grid (port 8009)")
    print("3. Launch v10.0 - Enterprise Ultimate Grid (port 8013)")
    print("4. Exit")
    print("-" * 60)
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == "1":
        print("\n=== Starting v7.0 Analysis Grid on port 8007 ===")
        kill_port(8007)
        time.sleep(1)
        subprocess.run([sys.executable, "start_analytics_v7.py"])
        
    elif choice == "2":
        print("\n=== Starting v8.2 Visual Grid on port 8009 ===")
        kill_port(8009)
        time.sleep(1)
        subprocess.run([sys.executable, "start_analytics_v8_bento_grid.py"])
        
    elif choice == "3":
        print("\n=== Starting v10.0 Ultimate Grid on port 8013 ===")
        kill_port(8013)
        time.sleep(1)
        subprocess.run([sys.executable, "ultimate_v10_fixed.py"])
        
    elif choice == "4":
        print("\nShutting down...")
        return
        
    else:
        print("\nInvalid option.")
        time.sleep(2)
        main()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nShutdown complete.")
