import torch
import torch.nn as nn
import torch.optim as optim
from typing import List, Dict

class RPSPredictor(nn.Module):
    """Deep Learning LSTM Model for sequence prediction."""
    def __init__(self):
        super().__init__()
        # Input size is 3 (one-hot encoded R, P, S)
        self.lstm = nn.LSTM(input_size=3, hidden_size=16, batch_first=True)
        self.fc = nn.Linear(16, 3)
        
    def forward(self, x):
        # x shape: (batch, seq_len, 3)
        out, _ = self.lstm(x)
        # We only care about the last output in the sequence
        out = out[:, -1, :] 
        out = self.fc(out)  
        return out

# Global dictionary to persist the PyTorch model and optimizer across function calls
dl_state = {
    'model': None,
    'optimizer': None,
    'criterion': None,
    'history_idx': []
}

move_to_idx = {'R': 0, 'P': 1, 'S': 2}
idx_to_move = {0: 'R', 1: 'P', 2: 'S'}

def one_hot(idx: int) -> torch.Tensor:
    t = torch.zeros(3)
    t[idx] = 1.0
    return t

def player(prev_play: str, opponent_history: List[str] = [], play_order: Dict = {}) -> str:
    """
    Rock-Paper-Scissors AI powered by a Deep Learning LSTM Network.
    
    The neural network trains 'online' (after every single move) to continuously
    adapt its weights based on the opponent's changing strategy.
    """
    # Initialize the Neural Network on first run
    if dl_state['model'] is None:
        dl_state['model'] = RPSPredictor()
        # High learning rate because we only have ~1000 games to learn
        dl_state['optimizer'] = optim.Adam(dl_state['model'].parameters(), lr=0.05)
        dl_state['criterion'] = nn.CrossEntropyLoss()
        
    # Reset for a new opponent
    if not prev_play:
        opponent_history.clear()
        dl_state['history_idx'].clear()
        return "R"
        
    # Record opponent's move
    idx = move_to_idx[prev_play]
    opponent_history.append(prev_play)
    dl_state['history_idx'].append(idx)
    
    # We will look at the last 5 moves to predict the 6th
    seq_len = 5
    
    # --- ONLINE TRAINING PHASE ---
    if len(dl_state['history_idx']) > seq_len:
        # The input X was the `seq_len` moves before the current move
        X_train_indices = dl_state['history_idx'][-(seq_len+1):-1]
        y_train_idx = idx # The true label is what the opponent just played
        
        # Prepare Tensors
        X_train = torch.stack([one_hot(i) for i in X_train_indices]).unsqueeze(0)
        y_train = torch.tensor([y_train_idx], dtype=torch.long)
        
        # Backpropagation
        dl_state['model'].train()
        dl_state['optimizer'].zero_grad()
        out = dl_state['model'](X_train)
        loss = dl_state['criterion'](out, y_train)
        loss.backward()
        dl_state['optimizer'].step()
        
    # --- INFERENCE (PREDICTION) PHASE ---
    if len(dl_state['history_idx']) >= seq_len:
        X_test_indices = dl_state['history_idx'][-seq_len:]
        X_test = torch.stack([one_hot(i) for i in X_test_indices]).unsqueeze(0)
        
        dl_state['model'].eval()
        with torch.no_grad():
            out = dl_state['model'](X_test)
            predicted_idx = torch.argmax(out, dim=1).item()
            predicted_move = idx_to_move[predicted_idx]
            
        return counter_move(predicted_move)
    else:
        # Fallback for the first few games before sequence length is reached
        return "P"

def counter_move(move: str) -> str:
    """Return the winning move."""
    counters = {"R": "P", "P": "S", "S": "R"}
    return counters.get(move, "R")