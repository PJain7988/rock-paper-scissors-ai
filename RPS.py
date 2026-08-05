import numpy as np
from typing import List, Dict

class RPSPredictorNumPy:
    """Deep Learning MLP Model for sequence prediction using NumPy."""
    def __init__(self, input_size=15, hidden_size=16, output_size=3, lr=0.05):
        # Weights and biases
        self.W1 = np.random.randn(input_size, hidden_size) * 0.1
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * 0.1
        self.b2 = np.zeros((1, output_size))
        
        self.lr = lr
        
        # Cache for backprop
        self.X = None
        self.Z1 = None
        self.A1 = None
        self.Z2 = None
        self.A2 = None

    def relu(self, Z):
        return np.maximum(0, Z)
        
    def relu_deriv(self, Z):
        return Z > 0
        
    def softmax(self, Z):
        expZ = np.exp(Z - np.max(Z, axis=1, keepdims=True))
        return expZ / np.sum(expZ, axis=1, keepdims=True)
        
    def forward(self, X):
        self.X = X
        self.Z1 = np.dot(X, self.W1) + self.b1
        self.A1 = self.relu(self.Z1)
        self.Z2 = np.dot(self.A1, self.W2) + self.b2
        self.A2 = self.softmax(self.Z2)
        return self.A2
        
    def backward(self, Y_true_onehot):
        m = self.X.shape[0]
        
        # dZ2 is A2 - Y for cross-entropy with softmax
        dZ2 = self.A2 - Y_true_onehot
        dW2 = np.dot(self.A1.T, dZ2) / m
        db2 = np.sum(dZ2, axis=0, keepdims=True) / m
        
        dA1 = np.dot(dZ2, self.W2.T)
        dZ1 = dA1 * self.relu_deriv(self.Z1)
        dW1 = np.dot(self.X.T, dZ1) / m
        db1 = np.sum(dZ1, axis=0, keepdims=True) / m
        
        # Update parameters (gradient descent, similar to SGD)
        self.W1 -= self.lr * dW1
        self.b1 -= self.lr * db1
        self.W2 -= self.lr * dW2
        self.b2 -= self.lr * db2

# Global dictionary to persist the model across function calls
dl_state = {
    'model': None,
    'history_idx': []
}

move_to_idx = {'R': 0, 'P': 1, 'S': 2}
idx_to_move = {0: 'R', 1: 'P', 2: 'S'}

def one_hot(idx: int):
    t = np.zeros(3)
    t[idx] = 1.0
    return t

def player(prev_play: str, opponent_history: List[str] = [], play_order: Dict = {}) -> str:
    """
    Rock-Paper-Scissors AI powered by a NumPy MLP Network.
    
    The neural network trains 'online' (after every single move) to continuously
    adapt its weights based on the opponent's changing strategy.
    """
    # Initialize the Neural Network on first run
    if dl_state['model'] is None:
        dl_state['model'] = RPSPredictorNumPy(input_size=15, hidden_size=16, output_size=3, lr=0.1)
        
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
        
        # Prepare arrays
        X_train = np.array([one_hot(i) for i in X_train_indices]).flatten().reshape(1, -1)
        y_train = one_hot(y_train_idx).reshape(1, -1)
        
        # Forward pass & Backpropagation
        dl_state['model'].forward(X_train)
        dl_state['model'].backward(y_train)
        
    # --- INFERENCE (PREDICTION) PHASE ---
    if len(dl_state['history_idx']) >= seq_len:
        X_test_indices = dl_state['history_idx'][-seq_len:]
        X_test = np.array([one_hot(i) for i in X_test_indices]).flatten().reshape(1, -1)
        
        out = dl_state['model'].forward(X_test)
        predicted_idx = np.argmax(out, axis=1)[0]
        predicted_move = idx_to_move[predicted_idx]
            
        return counter_move(predicted_move)
    else:
        # Fallback for the first few games before sequence length is reached
        return "P"

def counter_move(move: str) -> str:
    """Return the winning move."""
    counters = {"R": "P", "P": "S", "S": "R"}
    return counters.get(move, "R")