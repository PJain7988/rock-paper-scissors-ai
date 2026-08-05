import gradio as gr
from RPS import player

# Global Game State
score_you = 0
score_ai = 0
score_ties = 0

# Note: RPS.py relies on mutable default arguments for opponent_history.
# We explicitly pass these lists here to avoid side effects if the module is reloaded.
game_history = []
play_order = {}
prev_play = ""

def play_game(user_move):
    global score_you, score_ai, score_ties, prev_play
    
    if not user_move:
        return "Waiting...", "Make a move!", score_you, score_ai, score_ties
        
    # The AI predicts its move for THIS round based on what the user played LAST round
    ai_move = player(prev_play, game_history, play_order)
    
    # Now we save the user's current move to be passed to the AI next round
    prev_play = user_move
    
    # Calculate winner (User's move vs AI's move)
    if user_move == ai_move:
        score_ties += 1
        result = "It's a Tie! 🤝"
    elif (user_move == "R" and ai_move == "S") or \
         (user_move == "P" and ai_move == "R") or \
         (user_move == "S" and ai_move == "P"):
        score_you += 1
        result = "You Win! 🎉"
    else:
        score_ai += 1
        result = "AI Wins! 🤖"
        
    emoji_map = {'R': '🪨 Rock', 'P': '📄 Paper', 'S': '✂️ Scissors'}
    
    return emoji_map[ai_move], result, score_you, score_ai, score_ties

# Build Gradio UI
with gr.Blocks(theme=gr.themes.Monochrome()) as demo:
    gr.Markdown("# 🤖 AI Rock-Paper-Scissors")
    gr.Markdown("Play against an Artificial Intelligence powered by a Neural Network (MLP) that learns your patterns in real-time using NumPy!")
    
    with gr.Row():
        with gr.Column(scale=1):
            user_input = gr.Radio(choices=["R", "P", "S"], label="Make Your Move (R=Rock, P=Paper, S=Scissors)")
            btn = gr.Button("Play Move", variant="primary")
            
        with gr.Column(scale=1):
            ai_output = gr.Textbox(label="AI Move")
            result_output = gr.Textbox(label="Result")
            
    with gr.Row():
        score_you_out = gr.Number(label="Your Score", value=0, interactive=False)
        score_ai_out = gr.Number(label="AI Score", value=0, interactive=False)
        score_ties_out = gr.Number(label="Ties", value=0, interactive=False)

    btn.click(fn=play_game, 
              inputs=user_input, 
              outputs=[ai_output, result_output, score_you_out, score_ai_out, score_ties_out])

if __name__ == "__main__":
    demo.launch()
