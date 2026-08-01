import random


def quincy(prev_play, opponent_history=[]):
    """Quincy follows a fixed repeating pattern."""
    sequence = ["R", "R", "P", "P", "S"]
    move = sequence[len(opponent_history) % len(sequence)]
    opponent_history.append(move)
    return move


def abbey(prev_play, opponent_history=[]):
    """Abbey tries to respond to the player's previous move."""
    if prev_play == "":
        move = "R"
    elif prev_play == "R":
        move = "P"
    elif prev_play == "P":
        move = "S"
    else:
        move = "R"

    opponent_history.append(move)
    return move


def kris(prev_play, opponent_history=[]):
    """Kris uses a simple counter strategy."""
    if prev_play == "":
        move = "R"
    elif prev_play == "R":
        move = "P"
    elif prev_play == "P":
        move = "S"
    else:
        move = "R"

    opponent_history.append(move)
    return move


def mrugesh(prev_play, opponent_history=[]):
    """Mrugesh uses a simple pattern based on previous moves."""
    if prev_play:
        opponent_history.append(prev_play)

    if len(opponent_history) < 3:
        return "R"

    last_three = opponent_history[-3:]

    if last_three.count("R") >= 2:
        return "P"
    elif last_three.count("P") >= 2:
        return "S"
    else:
        return "R"


def get_player_name(player):
    """Return the function name."""
    return player.__name__


def play(player1, player2, num_games, verbose=False):
    """
    Play a match between two players.

    player1 and player2 must be functions that accept
    the opponent's previous move and return R/P/S.
    """

    p1_prev_play = ""
    p2_prev_play = ""

    p1_score = 0
    p2_score = 0

    for game in range(num_games):

        p1_play = player1(p2_prev_play)
        p2_play = player2(p1_prev_play)

        if p1_play not in ["R", "P", "S"]:
            raise ValueError("Player 1 returned an invalid move.")

        if p2_play not in ["R", "P", "S"]:
            raise ValueError("Player 2 returned an invalid move.")

        if p1_play == p2_play:
            result = "Tie"

        elif (
            (p1_play == "R" and p2_play == "S")
            or (p1_play == "P" and p2_play == "R")
            or (p1_play == "S" and p2_play == "P")
        ):
            p1_score += 1
            result = "Player 1 wins"

        else:
            p2_score += 1
            result = "Player 2 wins"

        if verbose:
            print(
                f"Game {game + 1}: "
                f"Player 1 = {p1_play}, "
                f"Player 2 = {p2_play} -> {result}"
            )

        p1_prev_play = p1_play
        p2_prev_play = p2_play

    print("\nMatch Result")
    print("-" * 30)
    print(f"Player 1: {p1_score}")
    print(f"Player 2: {p2_score}")
    print(f"Ties: {num_games - p1_score - p2_score}")

    return p1_score, p2_score