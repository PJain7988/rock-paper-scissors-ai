from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add the parent directory to sys.path so we can import our RPS game logic
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from RPS import player
except ImportError:
    pass # Will handle gracefully if path issues exist in vercel

# We store game state in memory. Note that Vercel Serverless functions 
# are stateless across cold starts, but this state WILL persist while 
# the function is "warm", allowing for short game sessions to have memory!
game_history = []
play_order = {}

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            user_move = data.get('move', '')
            
            # Call our Markov Chain AI from RPS.py
            ai_move = player(user_move, game_history, play_order)
            
            response = {
                "ai_move": ai_move,
                "history_length": len(game_history)
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "Rock Paper Scissors AI is running. Send a POST request with {'move': 'R/P/S'} to play!"}).encode('utf-8'))

    def do_OPTIONS(self):
        # Handle CORS preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
