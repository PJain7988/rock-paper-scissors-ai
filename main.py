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

    args = parser.parse_args()

    run_tests(games=args.games, verbose=args.verbose)


if __name__ == "__main__":
    main()