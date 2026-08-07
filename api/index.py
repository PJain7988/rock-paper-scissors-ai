from http.server import BaseHTTPRequestHandler

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RPS AI</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #0f0a1c;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(139, 92, 246, 0.4) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(236, 72, 153, 0.4) 0%, transparent 40%);
            color: white;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }

        .app-container {
            background: rgba(18, 14, 28, 0.85);
            backdrop-filter: blur(40px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 24px;
            width: 1100px;
            height: 700px;
            box-shadow: 0 30px 60px rgba(0,0,0,0.6);
            display: flex;
            flex-direction: column;
            padding: 20px 40px;
            position: relative;
        }

        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 20px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            margin-bottom: 30px;
        }

        .nav-links a {
            color: #94a3b8;
            margin: 0 15px;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.2s;
        }
        .nav-links a:hover, .nav-links a.active {
            color: white;
        }
        .nav-links a.active {
            border-bottom: 2px solid #a855f7;
            padding-bottom: 25px;
        }

        .main-content {
            display: flex;
            gap: 30px;
            height: 100%;
        }

        .glass-card {
            background: linear-gradient(145deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.01) 100%);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 20px;
            padding: 30px;
        }

        .play-area {
            flex: 1.5;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
        }

        .analytics-area {
            flex: 1;
            display: flex;
            flex-direction: column;
        }

        .title { font-size: 2.2rem; font-weight: 800; letter-spacing: 1px; margin-bottom: 20px; }
        .subtitle { font-size: 1.2rem; font-weight: 600; margin-bottom: 5px; }
        .status-text { color: #94a3b8; margin-bottom: 15px; }
        
        .score-display {
            font-size: 0.9rem;
            color: #94a3b8;
            margin-bottom: 40px;
        }
        .score-display span { color: white; font-weight: 700; }
        .score-display .ai-score { color: #ec4899; }

        .moves-container {
            display: flex;
            gap: 20px;
            width: 100%;
            justify-content: center;
        }

        .move-card {
            background: rgba(0,0,0,0.3);
            border: 2px solid;
            border-radius: 16px;
            width: 130px;
            height: 180px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }

        .move-card::before {
            content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
            opacity: 0.2; z-index: 0; transition: opacity 0.3s;
        }

        .move-card:hover { transform: translateY(-5px) scale(1.05); }
        .move-card:active { transform: scale(0.95); }
        .move-card:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }

        .move-card > * { z-index: 1; }
        .move-icon { font-size: 4rem; margin-bottom: 15px; filter: drop-shadow(0 0 10px rgba(255,255,255,0.3)); }
        .move-name { font-weight: 700; font-size: 1.1rem; }

        .move-rock { border-color: #8b5cf6; }
        .move-rock::before { background: linear-gradient(to bottom, transparent, #8b5cf6); }
        .move-paper { border-color: #ec4899; }
        .move-paper::before { background: linear-gradient(to bottom, transparent, #ec4899); }
        .move-scissors { border-color: #a855f7; }
        .move-scissors::before { background: linear-gradient(to bottom, transparent, #a855f7); }

        .stats-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }

        .chart-wrapper {
            flex: 1;
            position: relative;
            width: 100%;
        }
        
        .result-overlay {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 3rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 2px;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.3s;
            text-shadow: 0 10px 30px rgba(0,0,0,0.8);
            z-index: 50;
        }

        .show-result { opacity: 1; animation: popIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; }
        
        @keyframes popIn {
            0% { transform: translate(-50%, -50%) scale(0.5); opacity: 0; }
            100% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
        }

        .win-text { color: #4ade80; }
        .lose-text { color: #f87171; }
        .tie-text { color: #fbbf24; }
    </style>
</head>
<body>

    <div class="app-container">
        
        <!-- Navbar -->
        <div class="navbar">
            <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-full border-2 border-purple-500 flex items-center justify-center">
                    <span class="text-purple-500 text-xs">⚛</span>
                </div>
                <span class="font-bold text-xl tracking-wide">RPS AI</span>
            </div>
            <div class="nav-links flex items-center">
                <a href="#" class="active">Play</a>
                <span id="nav-score" class="font-bold text-purple-400 ml-4 tracking-wide">Score: 0 - 0</span>
            </div>
        </div>

        <div class="main-content">
            
            <!-- Left Area: Play -->
            <div class="glass-card play-area relative">
                <h1 class="title">AI ROCK-PAPER-SCISSORS</h1>
                <h2 class="subtitle">YOUR MOVE</h2>
                <p class="status-text" id="status-text">AI is ready</p>
                <div class="score-display">
                    Player: <span id="score-player">0</span> &nbsp;|&nbsp; AI: <span class="ai-score" id="score-ai">0</span>
                </div>

                <div class="moves-container">
                    <button class="move-card move-rock" id="btn-R" onclick="playMove('R')">
                        <div class="move-icon">✊</div>
                        <div class="move-name">Rock</div>
                    </button>
                    <button class="move-card move-paper" id="btn-P" onclick="playMove('P')">
                        <div class="move-icon">✋</div>
                        <div class="move-name">Paper</div>
                    </button>
                    <button class="move-card move-scissors" id="btn-S" onclick="playMove('S')">
                        <div class="move-icon">✌️</div>
                        <div class="move-name">Scissors</div>
                    </button>
                </div>
                
                <div id="result-overlay" class="result-overlay">WIN!</div>
            </div>

            <!-- Right Area: Analytics -->
            <div class="flex flex-col gap-4" style="flex: 1;">
                
                <!-- Match Stats -->
                <div class="flex justify-between items-center px-4 py-2 bg-gray-900 bg-opacity-50 rounded-lg text-sm border border-gray-700">
                    <div><span class="text-green-400">Wins:</span> <span id="stat-wins" class="font-bold">0</span></div>
                    <div><span class="text-red-400">Losses:</span> <span id="stat-losses" class="font-bold">0</span></div>
                    <div><span class="text-gray-400">Draws:</span> <span id="stat-draws" class="font-bold">0</span></div>
                    <div class="text-gray-500">Match <span id="stat-match" class="text-white">#1</span></div>
                </div>

                <div class="glass-card analytics-area">
                    <div class="stats-header">
                        <div>
                            <h3 class="font-bold text-lg leading-tight">AI PERFORMANCE</h3>
                            <h3 class="font-bold text-lg leading-tight">ANALYTICS</h3>
                        </div>
                        <select class="bg-gray-800 border border-gray-700 text-xs rounded px-2 py-1 outline-none">
                            <option>Last 30 Days</option>
                        </select>
                    </div>

                    <div class="chart-wrapper">
                        <canvas id="winRateChart"></canvas>
                    </div>

                    <div class="flex justify-center gap-6 mt-4 text-xs font-semibold text-gray-400">
                        <div class="flex items-center gap-2"><div class="w-3 h-3 rounded bg-purple-500"></div> AI WIN RATE (%)</div>
                        <div class="flex items-center gap-2"><div class="w-3 h-3 rounded bg-pink-500"></div> GAMES PLAYED</div>
                    </div>
                </div>
            </div>

        </div>
    </div>

    <script>
        let history = [];
        let scorePlayer = 0; let scoreAI = 0; let scoreDraws = 0; let matches = 1;
        let nextAIMove = null;
        
        // Setup Chart
        Chart.defaults.color = '#64748b';
        Chart.defaults.font.family = 'Inter';
        const ctx = document.getElementById('winRateChart').getContext('2d');
        
        // Gradient for line
        const gradient = ctx.createLinearGradient(0, 0, 0, 300);
        gradient.addColorStop(0, 'rgba(168, 85, 247, 0.5)');
        gradient.addColorStop(1, 'rgba(168, 85, 247, 0)');

        const winRateChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Start'],
                datasets: [{
                    data: [50],
                    borderColor: '#a855f7',
                    borderWidth: 3,
                    backgroundColor: gradient,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#ec4899',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { 
                        beginAtZero: true, max: 100, 
                        grid: { color: 'rgba(255,255,255,0.05)', drawBorder: false },
                        ticks: { callback: function(value) { return value + '%'; } }
                    },
                    x: { 
                        grid: { color: 'rgba(255,255,255,0.05)', drawBorder: false },
                        display: false 
                    }
                },
                plugins: { 
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: 'rgba(15, 23, 42, 0.9)',
                        titleFont: { size: 13 },
                        bodyFont: { size: 14, weight: 'bold' },
                        padding: 10,
                        displayColors: false,
                        callbacks: {
                            label: function(context) { return 'AI Win Rate: ' + context.parsed.y.toFixed(1) + '%'; }
                        }
                    }
                }
            }
        });

        function setButtonsEnabled(enabled) {
            document.getElementById('btn-R').disabled = !enabled;
            document.getElementById('btn-P').disabled = !enabled;
            document.getElementById('btn-S').disabled = !enabled;
        }

        async function fetchNextAIMove() {
            setButtonsEnabled(false);
            const statusText = document.getElementById('status-text');
            statusText.innerHTML = 'AI is calculating...';
            
            try {
                const response = await fetch('/api/play', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ history: history })
                });
                if (!response.ok) throw new Error("API Error");
                const data = await response.json();
                nextAIMove = data.ai_move;
                
                statusText.innerHTML = 'AI is ready. Your move.';
                setButtonsEnabled(true);
            } catch (error) {
                console.error(error);
                statusText.innerHTML = 'Connection Error';
            }
        }

        function playMove(userMove) {
            if (!nextAIMove) return;
            const aiMove = nextAIMove;
            
            const overlay = document.getElementById('result-overlay');
            overlay.className = 'result-overlay'; // reset
            
            // Calculate winner
            if (userMove === aiMove) {
                scoreDraws++; 
                document.getElementById('stat-draws').innerText = scoreDraws;
                overlay.innerHTML = 'DRAW';
                overlay.classList.add('tie-text');
            } else if ( (userMove === 'R' && aiMove === 'S') || (userMove === 'P' && aiMove === 'R') || (userMove === 'S' && aiMove === 'P') ) {
                scorePlayer++; 
                document.getElementById('score-player').innerText = scorePlayer;
                document.getElementById('stat-wins').innerText = scorePlayer;
                overlay.innerHTML = 'YOU WIN!';
                overlay.classList.add('win-text');
            } else {
                scoreAI++; 
                document.getElementById('score-ai').innerText = scoreAI;
                document.getElementById('stat-losses').innerText = scoreAI;
                overlay.innerHTML = 'AI WINS!';
                overlay.classList.add('lose-text');
            }

            // Show animation
            void overlay.offsetWidth; // trigger reflow
            overlay.classList.add('show-result');
            
            // Hide animation after 1s
            setTimeout(() => { overlay.classList.remove('show-result'); }, 1000);

            // Update Analytics
            document.getElementById('nav-score').innerText = `Score: ${scorePlayer} - ${scoreAI}`;
            history.push(userMove);
            matches++;
            document.getElementById('stat-match').innerText = '#' + matches;
            
            const totalGames = scorePlayer + scoreAI + scoreDraws;
            const currentWinRate = (scoreAI / totalGames) * 100;
            
            winRateChart.data.labels.push('Match ' + matches);
            winRateChart.data.datasets[0].data.push(currentWinRate);
            
            // Keep only last 10 points for clean chart
            if (winRateChart.data.labels.length > 10) {
                winRateChart.data.labels.shift();
                winRateChart.data.datasets[0].data.shift();
            }
            
            winRateChart.update();
            nextAIMove = null;
            setTimeout(fetchNextAIMove, 500);
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
