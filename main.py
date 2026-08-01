from RPS_game import play
from RPS import player
from RPS_game import abbey, quincy, kris, mrugesh


def run_tests():

    print("=" * 60)
    print("ROCK PAPER SCISSORS - AI TEST")
    print("=" * 60)

    print("\nTesting against Abbey...")
    play(player, abbey, 1000)

    print("\nTesting against Quincy...")
    play(player, quincy, 1000)

    print("\nTesting against Kris...")
    play(player, kris, 1000)

    print("\nTesting against Mrugesh...")
    play(player, mrugesh, 1000)


if __name__ == "__main__":
    run_tests()