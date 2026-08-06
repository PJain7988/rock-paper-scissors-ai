import gradio as gr
import matplotlib.pyplot as plt
import pandas as pd
from RPS import RPSAgent

def init_state():
    # Return fresh state for a new user session
    return {
        "agent": RPSAgent(),
        "score_you": 0,
        "score_ai": 0,
        "score_ties": 0,
        "prev_play": "",
        "user_move_history": [],
        "ai_win_history": []
    }

def play_game(user_move, state):
    if not user_move:
        return "Waiting...", "Make a move!", state["score_you"], state["score_ai"], state["score_ties"], None, state
        
    agent = state["agent"]
    prev_play = state["prev_play"]
    
    # AI predicts its move based on what the user played last round
    ai_move = agent.predict_next_move()
    
    # Calculate winner
    if user_move == ai_move:
        state["score_ties"] += 1
        result = "It's a Tie! 🤝"
    elif (user_move == "R" and ai_move == "S") or \
         (user_move == "P" and ai_move == "R") or \
         (user_move == "S" and ai_move == "P"):
        state["score_you"] += 1
        result = "You Win! 🎉"
    else:
        state["score_ai"] += 1
        result = "AI Wins! 🤖"
        
    # Record and Train the AI online!
    agent.record_and_train(user_move)
    state["prev_play"] = user_move
    
    # Analytics data tracking
    state["user_move_history"].append(user_move)
    total_games = state["score_you"] + state["score_ai"] + state["score_ties"]
    ai_win_rate = (state["score_ai"] / total_games) * 100
    state["ai_win_history"].append(ai_win_rate)
    
    emoji_map = {'R': '🪨 Rock', 'P': '📄 Paper', 'S': '✂️ Scissors'}
    
    # Generate Analytics Plot
    fig = generate_analytics_plot(state)
    
    return emoji_map[ai_move], result, state["score_you"], state["score_ai"], state["score_ties"], fig, state

def generate_analytics_plot(state):
    import matplotlib
    matplotlib.use('Agg')
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    # Plot 1: User Move Frequencies
    moves = state["user_move_history"]
    if moves:
        counts = {'R': moves.count('R'), 'P': moves.count('P'), 'S': moves.count('S')}
        ax1.bar(['Rock', 'Paper', 'Scissors'], [counts['R'], counts['P'], counts['S']], color=['#ef4444', '#3b82f6', '#10b981'])
        ax1.set_title("Your Move Frequencies")
        ax1.set_ylabel("Count")
    
    # Plot 2: AI Win Rate Over Time
    win_rates = state["ai_win_history"]
    if win_rates:
        ax2.plot(range(1, len(win_rates) + 1), win_rates, color='#8b5cf6', marker='o', markersize=4)
        ax2.set_title("AI Win Rate Progression")
        ax2.set_xlabel("Games Played")
        ax2.set_ylabel("Win Rate (%)")
        ax2.set_ylim(0, 100)
        
    plt.tight_layout()
    return fig

# Build Premium Gradio UI
with gr.Blocks(theme=gr.themes.Soft(primary_hue="indigo", secondary_hue="pink")) as demo:
    gr.Markdown("# 🤖 Advanced AI Rock-Paper-Scissors")
    gr.Markdown("Play against a sophisticated Deep Learning MLP model. This app uses thread-safe object-oriented architecture and visual analytics.")
    
    session_state = gr.State(init_state)
    
    with gr.Tabs():
        with gr.TabItem("🎮 Play Arena"):
            with gr.Row():
                with gr.Column(scale=1, variant="panel"):
                    user_input = gr.Radio(choices=["R", "P", "S"], label="Make Your Move (R=Rock, P=Paper, S=Scissors)")
                    btn = gr.Button("Play Move", variant="primary", size="lg")
                    
                with gr.Column(scale=1, variant="panel"):
                    ai_output = gr.Textbox(label="AI Move", text_align="center")
                    result_output = gr.Textbox(label="Result", text_align="center")
                    
            with gr.Row():
                score_you_out = gr.Number(label="Your Score", value=0, interactive=False)
                score_ai_out = gr.Number(label="AI Score", value=0, interactive=False)
                score_ties_out = gr.Number(label="Ties", value=0, interactive=False)
                
        with gr.TabItem("📊 AI Analytics"):
            gr.Markdown("### Real-Time Learning Insights\nWatch how the AI analyzes your behavior and adapts its win rate over time!")
            plot_output = gr.Plot()

    btn.click(fn=play_game, 
              inputs=[user_input, session_state], 
              outputs=[ai_output, result_output, score_you_out, score_ai_out, score_ties_out, plot_output, session_state])

if __name__ == "__main__":
    demo.launch()
