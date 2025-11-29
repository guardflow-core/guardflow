"""
GuardFlow - Simple HTTP Server for Demo
Servidor HTTP simples para demonstração
"""
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import time

class GuardFlowHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # CORS headers
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        if path == '/health':
            response = {
                "status": "healthy",
                "service": "GuardFlow API",
                "version": "0.1.0"
            }
        elif path == '/api/v1/scanner/stats':
            response = {
                "success": True,
                "data": {
                    "total_scans": 1250,
                    "successful_scans": 1180,
                    "success_rate": 94.4,
                    "avg_scan_time_ms": 850
                }
            }
        elif path == '/api/v1/esg/dashboard':
            response = {
                "success": True,
                "data": {
                    "total_score": 87,
                    "total_points": 2450,
                    "total_tokens": 125
                }
            }
        elif path == '/api/v1/products':
            response = {
                "success": True,
                "data": {
                    "total": 150,
                    "products": [
                        {"id": 1, "name": "Produto 1", "price": 10.50},
                        {"id": 2, "name": "Produto 2", "price": 15.75}
                    ]
                }
            }
        else:
            response = {
                "message": "GuardFlow API - Sistema de Checkout Inteligente",
                "version": "0.1.0",
                "status": "active"
            }
        
        self.wfile.write(json.dumps(response).encode())
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run_server():
    """Run the HTTP server"""
    server = HTTPServer(('127.0.0.1', 8002), GuardFlowHandler)
    print("🚀 GuardFlow Backend rodando em http://127.0.0.1:8002")
    print("📊 Health check: http://127.0.0.1:8002/health")
    print("📚 API Docs: http://127.0.0.1:8002/")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
