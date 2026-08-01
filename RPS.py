from typing import List, Dict

def player(prev_play: str, opponent_history: List[str] = [], play_order: Dict[str, int] = {}) -> str:
    """
    Adaptive Rock-Paper-Scissors player using a Multi-Order Markov Chain.

    The bot:
    1. Tracks sequences of opponent moves up to length `n`.
    2. Builds a transition probability dictionary (`play_order`).
    3. Predicts the next move by looking for the longest matching historical sequence.
    4. Seamlessly falls back to shorter sequences (n-gram decay) if the longest hasn't been observed.

    Args:
        prev_play (str): The opponent's last move ('R', 'P', 'S', or '' for first game).
        opponent_history (List[str]): Mutable list tracking the opponent's past moves.
        play_order (Dict[str, int]): Mutable dict tracking frequency of move sequences.

    Returns:
        str: Our move ('R', 'P', or 'S').
    """

    if not prev_play:
        prev_play = "R"

    opponent_history.append(prev_play)

    # Maximum sequence length to track (Multi-order limit)
    n = 6

    # Update the transition matrix for all observed sequence lengths
    if len(opponent_history) >= 2:
        max_len = min(len(opponent_history), n + 1)
        # Record sequences of lengths from 2 to max_len
        # e.g., if history is R, P, S, we record "RP", "PS", "RPS"
        for i in range(2, max_len + 1):
            seq = "".join(opponent_history[-i:])
            if seq in play_order:
                play_order[seq] += 1
            else:
                play_order[seq] = 1

    # Predict the opponent's next move
    potential_moves = ["R", "P", "S"]
    prediction = "P"  # Default prediction

    # Look back for patterns, starting from the longest context and decaying
    max_context = min(len(opponent_history), n)
    
    for i in range(max_context, 0, -1):
        context = "".join(opponent_history[-i:])
        
        # Calculate frequencies of possible next moves given this context
        counts = {}
        for move in potential_moves:
            counts[move] = play_order.get(context + move, 0)
            
        if sum(counts.values()) > 0:
            # We found a matching context! Pick the most probable next move.
            prediction = max(counts, key=counts.get)
            break

    return counter_move(prediction)


def counter_move(move: str) -> str:
    """
    Return the move that beats the given move.

    Args:
        move (str): The opponent's predicted move.
        
    Returns:
        str: The winning counter move.
    """
    counters = {
        "R": "P",
        "P": "S",
        "S": "R"
    }
    return counters.get(move, "R")