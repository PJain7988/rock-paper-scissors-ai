from http.server import BaseHTTPRequestHandler

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Rock Paper Scissors</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --primary: #8b5cf6;
            --secondary: #ec4899;
            --dark: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.6);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Outfit', sans-serif; }
        body {
            background: var(--dark);
            background-image: 
                radial-gradient(at 0% 0%, rgba(139, 92, 246, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(236, 72, 153, 0.15) 0px, transparent 50%);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            padding: 20px;
        }
        .container { display: flex; gap: 30px; width: 100%; max-width: 1200px; z-index: 10; }
        .glass-panel {
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 24px;
            padding: 40px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            text-align: center;
            flex: 1;
        }
        h1 {
            font-weight: 800; font-size: 2.5rem; margin-bottom: 10px;
            background: linear-gradient(to right, var(--primary), var(--secondary));
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        p.subtitle { color: var(--text-muted); font-size: 1.1rem; margin-bottom: 30px; }
        .score-board {
            display: flex; justify-content: space-around;
            background: rgba(0,0,0,0.3); border-radius: 16px; padding: 20px; margin-bottom: 30px;
        }
        .score-box { display: flex; flex-direction: column; }
        .score-box span.label { font-size: 0.9rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }
        .score-box span.score { font-size: 2.5rem; font-weight: 800; color: var(--text-main); }
        .battle-arena { display: flex; align-items: center; justify-content: center; gap: 20px; margin-bottom: 30px; min-height: 120px; }
        .move-display {
            font-size: 4rem; width: 100px; height: 100px; display: flex; align-items: center; justify-content: center;
            background: rgba(255,255,255,0.05); border-radius: 50%; border: 1px dashed rgba(255,255,255,0.2); transition: all 0.3s ease;
        }
        .vs { font-weight: 800; font-size: 1.5rem; color: var(--text-muted); }
        .result-text { font-size: 1.5rem; font-weight: 600; height: 35px; margin-bottom: 30px; letter-spacing: 1px; }
        .win { color: #4ade80; text-shadow: 0 0 10px rgba(74, 222, 128, 0.5); }
        .lose { color: #f87171; text-shadow: 0 0 10px rgba(248, 113, 113, 0.5); }
        .tie { color: #fbbf24; }
        .controls { display: flex; justify-content: center; gap: 20px; }
        button.move-btn {
            background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); color: white; font-size: 2.5rem;
            width: 80px; height: 80px; border-radius: 20px; cursor: pointer; transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
            display: flex; align-items: center; justify-content: center;
        }
        button.move-btn:hover:not(:disabled) {
            transform: translateY(-5px) scale(1.1); background: rgba(255, 255, 255, 0.1); border-color: rgba(255, 255, 255, 0.3); box-shadow: 0 10px 25px -5px rgba(139, 92, 246, 0.4);
        }
        button.move-btn:active:not(:disabled) { transform: scale(0.95); }
        button.move-btn:disabled { opacity: 0.5; cursor: not-allowed; }
        .chart-container { position: relative; height: 300px; width: 100%; margin-top: 20px; }
        .bg-blob { position: absolute; filter: blur(100px); z-index: 1; opacity: 0.4; animation: float 10s infinite ease-in-out alternate; }
        .blob-1 { background: var(--primary); width: 400px; height: 400px; border-radius: 50%; top: -100px; left: -100px; }
        .blob-2 { background: var(--secondary); width: 500px; height: 500px; border-radius: 50%; bottom: -150px; right: -100px; animation-delay: -5s; }
        @keyframes float { 0% { transform: translate(0, 0) rotate(0deg); } 100% { transform: translate(50px, 80px) rotate(20deg); } }
        @media (max-width: 900px) { .container { flex-direction: column; } }
    </style>
</head>
<body>
    <div class="bg-blob blob-1"></div>
    <div class="bg-blob blob-2"></div>
    <div class="container">
        <!-- Play Arena -->
        <div class="glass-panel">
            <h1>AI Showdown</h1>
            <p class="subtitle">Can you outsmart the Deep Learning Network?</p>
            <div class="score-board">
                <div class="score-box"><span class="label">You</span><span class="score" id="score-you">0</span></div>
                <div class="score-box"><span class="label">Ties</span><span class="score" id="score-ties" style="font-size: 1.5rem; color: var(--text-muted); margin-top:10px;">0</span></div>
                <div class="score-box"><span class="label">AI</span><span class="score" id="score-ai">0</span></div>
            </div>
            <div class="battle-arena">
                <div class="move-display" id="display-you">?</div>
                <div class="vs">VS</div>
                <div class="move-display" id="display-ai">🤖</div>
            </div>
            <div class="result-text" id="result-text">Initializing AI...</div>
            <div class="controls">
                <button class="move-btn" id="btn-R" onclick="playMove('R')" title="Rock" disabled>🪨</button>
                <button class="move-btn" id="btn-P" onclick="playMove('P')" title="Paper" disabled>📄</button>
                <button class="move-btn" id="btn-S" onclick="playMove('S')" title="Scissors" disabled>✂️</button>
            </div>
        </div>
        <!-- Analytics Dashboard -->
        <div class="glass-panel">
            <h2 style="margin-bottom: 20px;">Live AI Analytics</h2>
            <p class="subtitle" style="margin-bottom: 10px;">The AI trains on your move history in real-time.</p>
            <div class="chart-container">
                <canvas id="winRateChart"></canvas>
            </div>
        </div>
    </div>
    <script>
        const emojiMap = { 'R': '🪨', 'P': '📄', 'S': '✂️', '': '?' };
        let history = [];
        let scoreYou = 0; let scoreAI = 0; let scoreTies = 0;
        let nextAIMove = null;
        
        // Initialize Chart
        Chart.defaults.color = '#94a3b8';
        Chart.defaults.font.family = 'Outfit';
        const ctx = document.getElementById('winRateChart').getContext('2d');
        const winRateChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'AI Win Rate (%)',
                    data: [],
                    borderColor: '#8b5cf6',
                    backgroundColor: 'rgba(139, 92, 246, 0.2)',
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true,
                    pointBackgroundColor: '#ec4899',
                    pointRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { beginAtZero: true, max: 100, grid: { color: 'rgba(255,255,255,0.05)' } },
                    x: { grid: { color: 'rgba(255,255,255,0.05)' } }
                },
                plugins: { legend: { display: false } }
            }
        });

        function setButtonsEnabled(enabled) {
            document.getElementById('btn-R').disabled = !enabled;
            document.getElementById('btn-P').disabled = !enabled;
            document.getElementById('btn-S').disabled = !enabled;
        }

        async function fetchNextAIMove() {
            setButtonsEnabled(false);
            const resultText = document.getElementById('result-text');
            if (history.length === 0) resultText.innerHTML = 'AI is connecting...';
            else resultText.innerHTML = 'AI is predicting your next move...';
            
            try {
                const response = await fetch('/api/play', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ history: history })
                });
                if (!response.ok) throw new Error("API Error");
                const data = await response.json();
                nextAIMove = data.ai_move;
                
                resultText.innerHTML = 'AI is ready! Make your move.';
                resultText.className = 'result-text';
                setButtonsEnabled(true);
            } catch (error) {
                console.error(error);
                resultText.innerHTML = 'Error connecting to API';
                resultText.className = 'result-text lose';
            }
        }

        function playMove(userMove) {
            if (!nextAIMove) return;
            const aiMove = nextAIMove;
            document.getElementById('display-you').innerHTML = emojiMap[userMove];
            document.getElementById('display-ai').innerHTML = emojiMap[aiMove];
            const resultText = document.getElementById('result-text');
            
            if (userMove === aiMove) {
                scoreTies++; document.getElementById('score-ties').innerText = scoreTies;
                resultText.innerHTML = "It's a Tie! 🤝"; resultText.className = 'result-text tie';
            } else if ( (userMove === 'R' && aiMove === 'S') || (userMove === 'P' && aiMove === 'R') || (userMove === 'S' && aiMove === 'P') ) {
                scoreYou++; document.getElementById('score-you').innerText = scoreYou;
                resultText.innerHTML = 'You Win! 🎉'; resultText.className = 'result-text win';
            } else {
                scoreAI++; document.getElementById('score-ai').innerText = scoreAI;
                resultText.innerHTML = 'AI Wins! 🤖'; resultText.className = 'result-text lose';
            }

            history.push(userMove);
            const totalGames = scoreYou + scoreAI + scoreTies;
            const currentWinRate = (scoreAI / totalGames) * 100;
            
            winRateChart.data.labels.push(totalGames);
            winRateChart.data.datasets[0].data.push(currentWinRate);
            winRateChart.update();

            nextAIMove = null;
            setTimeout(fetchNextAIMove, 1000);
        }
        fetchNextAIMove();
    </script>
</body>
</html>
"""

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(HTML_CONTENT.encode('utf-8'))
