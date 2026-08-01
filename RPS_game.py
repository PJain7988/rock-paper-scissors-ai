import random
from typing import List, Callable, Tuple, Any

# Note: We intentionally use mutable default arguments `opponent_history=[]` 
# here to preserve state across function calls, which is a requirement for 
# the specific testing architecture used in this project.

def quincy(prev_play: str, opponent_history: List[str] = []) -> str:
    """Quincy follows a fixed repeating pattern.
    
    Args:
        prev_play (str): The opponent's previous move.
        opponent_history (list): A list tracking the opponent's moves.
        
    Returns:
        str: The selected move ('R', 'P', or 'S').
    """
    sequence = ["R", "R", "P", "P", "S"]
    move = sequence[len(opponent_history) % len(sequence)]
    opponent_history.append(move)
    return move


def abbey(prev_play: str, opponent_history: List[str] = []) -> str:
    """Abbey tries to respond to the player's previous move.
    
    Args:
        prev_play (str): The opponent's previous move.
        opponent_history (list): A list tracking the opponent's moves.
        
    Returns:
        str: The selected move.
    """
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


def kris(prev_play: str, opponent_history: List[str] = []) -> str:
    """Kris uses a simple counter strategy.
    
    Args:
        prev_play (str): The opponent's previous move.
        opponent_history (list): A list tracking the opponent's moves.
        
    Returns:
        str: The selected move.
    """
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


def mrugesh(prev_play: str, opponent_history: List[str] = []) -> str:
    """Mrugesh uses a simple pattern based on previous moves.
    
    Args:
        prev_play (str): The opponent's previous move.
        opponent_history (list): A list tracking the opponent's moves.
        
    Returns:
        str: The selected move.
    """
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


def get_player_name(player: Callable) -> str:
    """Return the function name."""
    return player.__name__


def play(player1: Callable, player2: Callable, num_games: int, verbose: bool = False) -> Tuple[int, int]:
    """
    Play a match between two players.

    player1 and player2 must be functions that accept
    the opponent's previous move and return R/P/S.
    
    Args:
        player1 (Callable): The first player function.
        player2 (Callable): The second player function.
        num_games (int): The number of games to play.
        verbose (bool): Whether to print out each game's result.
        
    Returns:
        Tuple[int, int]: The scores of player1 and player2.
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
    print(f"Player 1 ({get_player_name(player1)}): {p1_score}")
    print(f"Player 2 ({get_player_name(player2)}): {p2_score}")
    print(f"Ties: {num_games - p1_score - p2_score}")

    return p1_score, p2_score