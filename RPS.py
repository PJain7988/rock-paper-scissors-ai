import numpy as np
from typing import List, Dict, Optional

class RPSPredictorNumPy:
    """Deep Learning MLP Model for sequence prediction using NumPy."""
    def __init__(self, input_size=15, hidden_size=16, output_size=3, lr=0.1):
        self.W1 = np.random.randn(input_size, hidden_size) * 0.1
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * 0.1
        self.b2 = np.zeros((1, output_size))
        self.lr = lr
        
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
        
        dZ2 = self.A2 - Y_true_onehot
        dW2 = np.dot(self.A1.T, dZ2) / m
        db2 = np.sum(dZ2, axis=0, keepdims=True) / m
        
        dA1 = np.dot(dZ2, self.W2.T)
        dZ1 = dA1 * self.relu_deriv(self.Z1)
        dW1 = np.dot(self.X.T, dZ1) / m
        db1 = np.sum(dZ1, axis=0, keepdims=True) / m
        
        self.W1 -= self.lr * dW1
        self.b1 -= self.lr * db1
        self.W2 -= self.lr * dW2
        self.b2 -= self.lr * db2

class RPSAgent:
    """Thread-safe stateful agent for playing Rock-Paper-Scissors."""
    
    MOVE_TO_IDX = {'R': 0, 'P': 1, 'S': 2}
    IDX_TO_MOVE = {0: 'R', 1: 'P', 2: 'S'}
    
    def __init__(self, seq_len: int = 5):
        self.model = RPSPredictorNumPy(input_size=seq_len*3, hidden_size=16, output_size=3, lr=0.1)
        self.history_idx: List[int] = []
        self.seq_len = seq_len

    @staticmethod
    def _one_hot(idx: int) -> np.ndarray:
        t = np.zeros(3)
        t[idx] = 1.0
        return t

    @staticmethod
    def counter_move(move: str) -> str:
        """Return the winning move against the given move."""
        counters = {"R": "P", "P": "S", "S": "R"}
        return counters.get(move, "R")

    def predict_next_move(self) -> str:
        """Predict the user's next move and return the counter move."""
        if len(self.history_idx) >= self.seq_len:
            X_test_indices = self.history_idx[-self.seq_len:]
            X_test = np.array([self._one_hot(i) for i in X_test_indices]).flatten().reshape(1, -1)
            
            out = self.model.forward(X_test)
            predicted_idx = np.argmax(out, axis=1)[0]
            predicted_move = self.IDX_TO_MOVE[predicted_idx]
            
            return self.counter_move(predicted_move)
        else:
            # Fallback early in the game
            return "P"

    def record_and_train(self, opponent_move: str):
        """Record the opponent's true move and train the model online."""
        if not opponent_move:
            self.history_idx.clear()
            return
            
        idx = self.MOVE_TO_IDX[opponent_move]
        self.history_idx.append(idx)
        
        if len(self.history_idx) > self.seq_len:
            # Train the network
            X_train_indices = self.history_idx[-(self.seq_len+1):-1]
            y_train_idx = idx 
            
            X_train = np.array([self._one_hot(i) for i in X_train_indices]).flatten().reshape(1, -1)
            y_train = self._one_hot(y_train_idx).reshape(1, -1)
            
            self.model.forward(X_train)
            self.model.backward(y_train)

# Maintain backward compatibility with legacy `player` function for `main.py`
_global_agent = None

def player(prev_play: str, opponent_history: Optional[List[str]] = None, play_order: Optional[Dict] = None) -> str:
    """Legacy interface for automated testing scripts."""
    global _global_agent
    if _global_agent is None:
        _global_agent = RPSAgent()
        
    if not prev_play:
        _global_agent = RPSAgent()
        return "R"
        
    _global_agent.record_and_train(prev_play)
    return _global_agent.predict_next_move()