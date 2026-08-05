import argparse
from RPS_game import play
from RPS import player
from RPS_game import abbey, quincy, kris, mrugesh


def run_tests(games: int, verbose: bool):
    """
    Run the AI player against all test bots.
    
    Args:
        games (int): The number of games to play against each bot.
        verbose (bool): If True, prints every single game's outcome.
    """
    print("=" * 60)
    print("ROCK PAPER SCISSORS - AI PERFORMANCE EVALUATION")
    print("=" * 60)

    bots = [
        ("Abbey", abbey),
        ("Quincy", quincy),
        ("Kris", kris),
        ("Mrugesh", mrugesh)
    ]

    for bot_name, bot_func in bots:
        print(f"\nTesting against {bot_name}...")
        play(player, bot_func, games, verbose=verbose)


def interactive_mode():
    print("=" * 60)
    print("ROCK PAPER SCISSORS - INTERACTIVE AI MODE")
    print("Type 'R' for Rock, 'P' for Paper, 'S' for Scissors, or 'Q' to Quit.")
    print("=" * 60)
    
    valid_moves = ["R", "P", "S"]
    prev_play = ""
    
    wins = 0
    losses = 0
    ties = 0

    while True:
        user_move = input("Your move (R/P/S/Q): ").strip().upper()
        if user_move == 'Q':
            break
        if user_move not in valid_moves:
            print("Invalid move. Please try again.")
            continue
        
        ai_move = player(prev_play)
        print(f"AI plays: {ai_move}")
        
        if user_move == ai_move:
            print("Result: Tie!")
            ties += 1
        elif (user_move == "R" and ai_move == "S") or \
             (user_move == "P" and ai_move == "R") or \
             (user_move == "S" and ai_move == "P"):
            print("Result: You win!")
            wins += 1
        else:
            print("Result: You lose!")
            losses += 1
            
        print(f"Score - You: {wins} | AI: {losses} | Ties: {ties}\n")
        prev_play = user_move

    print(f"\nFinal Score - You: {wins} | AI: {losses} | Ties: {ties}")
    print("Thanks for playing!")


def main():
    """Main entry point for CLI usage."""
    parser = argparse.ArgumentParser(description="Evaluate the RPS AI agent against standard bots.")
    parser.add_argument(
        "--games",
        type=int,
        default=1000,
        help="Number of games to play against each bot (default: 1000)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print the result of every individual game"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Play interactively against the AI"
    )

    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
    else:
        run_tests(games=args.games, verbose=args.verbose)


if __name__ == "__main__":
    main()