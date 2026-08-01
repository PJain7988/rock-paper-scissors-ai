import unittest

from RPS import player


class TestRPSPlayer(unittest.TestCase):

    def test_valid_first_move(self):
        move = player("")
        self.assertIn(move, ["R", "P", "S"])

    def test_valid_response(self):
        moves = ["R", "P", "S"]

        for move in moves:
            response = player(move)
            self.assertIn(response, ["R", "P", "S"])

    def test_counter_move(self):
        from RPS import counter_move

        self.assertEqual(counter_move("R"), "P")
        self.assertEqual(counter_move("P"), "S")
        self.assertEqual(counter_move("S"), "R")


if __name__ == "__main__":
    unittest.main()