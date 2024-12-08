import unittest
from Backend.gameboardGroupings.gameboard import GameBoard
from Backend.commons import ValidRooms


class GameboardTest(unittest.TestCase):
    """Tests the functionality of the Gameboard Module."""

    NUM_OF_SPACES = 21

    def setUp(self):
        """Sets up the test data for Gameboard tests."""
        self._game_board = GameBoard()
        self.assertEqual(len(self._game_board.get_spaces()), self.NUM_OF_SPACES)

    def test_get_space_by_name(self):
        """Tests the look up functionality of the spaces"""
        space_billiards = self._game_board.get_space_by_name(ValidRooms.BILLIARDS)
        self.assertEqual(space_billiards._name, ValidRooms.BILLIARDS)

    def test_get_space_by_name_invalid(self):
        """Tests the look up functionality of the spaces"""
        with self.assertRaises(KeyError):
            self._game_board.get_space_by_name("St. Thomas")
