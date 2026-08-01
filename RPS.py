def player(prev_play, opponent_history=[]):
    """
    Adaptive Rock-Paper-Scissors player.

    The bot:
    1. Stores the opponent's previous moves.
    2. Looks for repeated patterns.
    3. Predicts the opponent's next move.
    4. Plays the move that beats the prediction.
    """

    # Store opponent's previous move
    if prev_play:
        opponent_history.append(prev_play)

    # First move
    if not opponent_history:
        return "R"

    # -------------------------------------------------
    # Strategy 1: Look for a repeated sequence
    # -------------------------------------------------

    # We need at least 5 previous moves to find patterns.
    if len(opponent_history) >= 5:

        # Use the last 3 moves as our current pattern.
        pattern_length = 3
        current_pattern = opponent_history[-pattern_length:]

        predictions = []

        # Search previous history for the same pattern.
        for i in range(len(opponent_history) - pattern_length):
            pattern = opponent_history[i:i + pattern_length]

            if pattern == current_pattern:
                next_index = i + pattern_length

                if next_index < len(opponent_history):
                    predictions.append(opponent_history[next_index])

        # If we found a repeated pattern,
        # predict the most common following move.
        if predictions:

            counts = {
                "R": predictions.count("R"),
                "P": predictions.count("P"),
                "S": predictions.count("S")
            }

            predicted_move = max(counts, key=counts.get)

            return counter_move(predicted_move)

    # -------------------------------------------------
    # Strategy 2: Frequency analysis
    # -------------------------------------------------

    counts = {
        "R": opponent_history.count("R"),
        "P": opponent_history.count("P"),
        "S": opponent_history.count("S")
    }

    most_common_move = max(counts, key=counts.get)

    return counter_move(most_common_move)


def counter_move(move):
    """
    Return the move that beats the given move.

    Rock -> Paper
    Paper -> Scissors
    Scissors -> Rock
    """

    if move == "R":
        return "P"

    if move == "P":
        return "S"

    if move == "S":
        return "R"

    return "R"