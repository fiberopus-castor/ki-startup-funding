#!/usr/bin/env python3
"""Simple HTTP server with basic auth for the funding presentation."""
import http.server
import base64
import os

PORT = 8888
USER = "1234"
PASS = "1234"
DIR = os.path.dirname(os.path.abspath(__file__))

class AuthHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="Praesentation"')
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        auth = self.headers.get("Authorization")
        if auth is None:
            self.do_AUTHHEAD()
            self.wfile.write(b"Login required")
            return
        elif auth == "Basic " + base64.b64encode(f"{USER}:{PASS}".encode()).decode():
            # Redirect / to /index.html
            if self.path == "/":
                self.path = "/index.html"
            super().do_GET()
        else:
            self.do_AUTHHEAD()
            self.wfile.write(b"Wrong credentials")

if __name__ == "__main__":
    with http.server.HTTPServer(("0.0.0.0", PORT), AuthHandler) as httpd:
        print(f"Serving on http://0.0.0.0:{PORT} (user: {USER}, pass: {PASS})")
        httpd.serve_forever()
