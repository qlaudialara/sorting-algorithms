#!/usr/bin/env python3
"""Simple HTTP server for downloading result files."""

import os
import sys
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import unquote

class DownloadHandler(SimpleHTTPRequestHandler):
    """Custom handler with better file serving."""
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/':
            # Serve download directory listing
            self.path = '/downloads/'
        
        # Add content-disposition header for downloads
        if self.path.startswith('/downloads/') and not self.path.endswith('/'):
            self.send_response(200)
            filename = Path(self.path).name
            self.send_header('Content-type', self.guess_type(self.path)[0] or 'application/octet-stream')
            self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
            
            # Send file
            filepath = Path(self.path.lstrip('/'))
            if filepath.exists() and filepath.is_file():
                self.send_header('Content-Length', filepath.stat().st_size)
                self.end_headers()
                with open(filepath, 'rb') as f:
                    self.wfile.write(f.read())
            return
        
        return super().do_GET()
    
    def end_headers(self):
        """Add custom headers."""
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()
    
    def log_message(self, format, *args):
        """Custom log format."""
        print(f"[{self.log_date_time_string()}] {format % args}")

def run_server(port=8000):
    """Run download server."""
    os.chdir(Path(__file__).parent)
    
    server_address = ('', port)
    httpd = HTTPServer(server_address, DownloadHandler)
    
    print("=" * 80)
    print("📥 DOWNLOAD SERVER STARTED")
    print("=" * 80)
    print(f"\n🌐 Server running at: http://localhost:{port}")
    print(f"📂 Downloads directory: {Path('downloads').absolute()}")
    print(f"\nAvailable files:")
    
    downloads_dir = Path('downloads')
    if downloads_dir.exists():
        for i, file in enumerate(sorted(downloads_dir.glob('*')), 1):
            if file.is_file():
                size_kb = file.stat().st_size / 1024
                url = f"http://localhost:{port}/downloads/{file.name}"
                print(f"  {i}. {file.name:<50} ({size_kb:>6.1f} KB)")
                print(f"     → {url}")
    
    print("\n" + "=" * 80)
    print("Press Ctrl+C to stop the server")
    print("=" * 80 + "\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n✓ Server stopped")
        sys.exit(0)

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run_server(port)
