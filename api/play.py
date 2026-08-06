import sys
import os
import json
from http.server import BaseHTTPRequestHandler

# Add parent directory to sys.path to import RPS
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from RPS import RPSAgent

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            history = data.get('history', [])
            
            # Spin up a fresh agent (Stateless Architecture)
            agent = RPSAgent()
            
            # Train the agent instantly on the entire session history
            for move in history:
                agent.record_and_train(move)
                
            # Predict the counter move for the NEXT round
            ai_move = agent.predict_next_move()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {"ai_move": ai_move}
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

    def do_OPTIONS(self):
        # Handle CORS preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
