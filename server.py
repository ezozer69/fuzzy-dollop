#!/usr/bin/env python3
"""
Simple HTTP Server for Agent Test Dashboard
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

def start_server(port=8000):
    """Start a simple HTTP server."""
    try:
        # Change to the directory containing our files
        os.chdir(Path(__file__).parent)
        
        # Create server
        with socketserver.TCPServer(("", port), CustomHTTPRequestHandler) as httpd:
            print(f"🌐 Starting server at http://localhost:{port}")
            print(f"📁 Serving files from: {os.getcwd()}")
            print(f"🎯 Dashboard: http://localhost:{port}/dashboard.html")
            print("Press Ctrl+C to stop the server")
            print("-" * 50)
            
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n🛑 Server stopped by user")
                
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Port {port} is already in use. Trying port {port + 1}")
            start_server(port + 1)
        else:
            print(f"❌ Error starting server: {e}")
            sys.exit(1)

if __name__ == "__main__":
    start_server()