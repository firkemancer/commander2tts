#!/usr/bin/env python3
"""
COMMANDER2TTS Server Launcher
Simple HTTP server to run the COMMANDER2TTS deck builder
"""

import http.server
import socketserver
import os
import sys
import signal
import webbrowser
from pathlib import Path

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers to allow external API requests
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()

    def log_message(self, format, *args):
        # Cleaner logging
        sys.stdout.write(f"[{self.log_date_time_string()}] {format % args}\n")

def kill_existing_server():
    """Kill any process using our port"""
    import subprocess
    import platform
    
    print("\n🔍 Checking for existing server on port {}...".format(PORT))
    
    system = platform.system()
    
    # Windows
    if system == "Windows":
        try:
            # Use netstat to find the PID
            result = subprocess.run(
                ['netstat', '-ano'],
                capture_output=True,
                text=True
            )
            
            for line in result.stdout.split('\n'):
                if f':{PORT}' in line and 'LISTENING' in line:
                    parts = line.split()
                    if len(parts) >= 5:
                        pid = parts[-1]
                        print(f"🔨 Killing existing server (PID: {pid})...")
                        try:
                            subprocess.run(['taskkill', '/PID', pid, '/F'], capture_output=True)
                            import time
                            time.sleep(1)
                            print("✅ Old server stopped")
                        except:
                            print("⚠️  Could not kill old server")
                        break
            else:
                print("✅ No existing server found")
        except:
            print("⚠️  Cannot detect existing server on Windows")
            print(f"   If port {PORT} is in use, you may see an error below")
    
    # Linux/Mac
    else:
        try:
            # Try using lsof (most common on Linux/Mac)
            result = subprocess.run(
                ['lsof', '-ti', f':{PORT}'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0 and result.stdout.strip():
                pid = result.stdout.strip()
                print(f"🔨 Killing existing server (PID: {pid})...")
                try:
                    os.kill(int(pid), signal.SIGKILL)
                    import time
                    time.sleep(1)
                    print("✅ Old server stopped")
                except:
                    print("⚠️  Could not kill old server, it may have already stopped")
            else:
                print("✅ No existing server found")
                
        except FileNotFoundError:
            # lsof not available, try alternative methods
            try:
                # Try netstat
                result = subprocess.run(
                    ['netstat', '-tulpn'],
                    capture_output=True,
                    text=True
                )
                
                for line in result.stdout.split('\n'):
                    if f':{PORT}' in line and 'LISTEN' in line:
                        # Extract PID
                        parts = line.split()
                        for part in parts:
                            if '/' in part:
                                pid = part.split('/')[0]
                                print(f"🔨 Killing existing server (PID: {pid})...")
                                try:
                                    os.kill(int(pid), signal.SIGKILL)
                                    import time
                                    time.sleep(1)
                                    print("✅ Old server stopped")
                                except:
                                    pass
                                break
                        break
                else:
                    print("✅ No existing server found")
                    
            except:
                print("⚠️  Cannot detect existing server (requires lsof or netstat)")
                print(f"   If port {PORT} is in use, you may see an error below")

def main():
    # Get the directory where the script is located
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    
    # Check if commander2tts.html exists
    html_file = script_dir / "commander2tts.html"
    if not html_file.exists():
        print(f"❌ Error: commander2tts.html not found in {script_dir}")
        print("   Please make sure commander2tts.html is in the same folder as this script.")
        sys.exit(1)
    
    # Kill any existing server on the port
    kill_existing_server()
    
    # Create server
    handler = MyHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            print("=" * 60)
            print("⚔️  COMMANDER2TTS Server Started!")
            print("=" * 60)
            print(f"\n📂 Serving from: {script_dir}")
            print(f"🌐 Server running at: http://localhost:{PORT}")
            print(f"🎮 Open this URL: http://localhost:{PORT}/commander2tts.html")
            print("\n💡 Press Ctrl+C to stop the server")
            print("=" * 60)
            print()
            
            # Try to open browser automatically
            try:
                webbrowser.open(f"http://localhost:{PORT}/commander2tts.html")
                print("✅ Opening browser automatically...\n")
            except:
                print("⚠️  Could not open browser automatically. Please open the URL manually.\n")
            
            # Start serving
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        sys.exit(0)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"\n❌ Error: Port {PORT} is still in use!")
            print("   The old server may not have been killed. Try again or change the PORT.")
        else:
            print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
