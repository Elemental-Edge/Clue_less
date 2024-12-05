import unittest
from Backend.GameManagement.playerGroupings.player import Player
from Backend.gameboardGroupings.space import Space, Room, CornerRoom, Hallway, SpaceType
from Backend.cardGroupings.Card import Card, CardType


class SpaceTypeTest(unittest.TestCase):
    """Tests the functionality of the SpaceType enumeration."""
    def setUp(self):
        """Sets up the test data for SpaceType tests."""
        self.space_type1 = SpaceType.ROOM

    def test_str(self):
        """Tests the __str__ method of SpaceType."""
        self.assertEqual(str(self.space_type1), "Room")


class SpaceTest(unittest.TestCase):
    """Tests the functionality of the Space class."""
    def setUp(self):
        """Sets up the test data for Space tests."""
        self.space1 = Space("Space1")
        self.space2 = Space("Space2")
        self.player = Player(playerID=1, character="Player1")

    def test_add_adjacent_space(self):
        """Tests adding an adjacent space."""
        self.space1.add_adjacent_space(self.space2)
        self.assertIn(self.space2, self.space1._adjacent_spaces)
        self.assertIn(self.space1, self.space2._adjacent_spaces)

    def test_add_adjacent_space_error(self):
        """Tests error handling when adding an invalid adjacent space."""
        with self.assertRaises(ValueError):
            self.space1.add_adjacent_space(None)

    def test_remove_adjacent_space(self):
        """Tests removing an adjacent space."""
        self.space1.add_adjacent_space(self.space2)
        self.space1.remove_adjacent_space("Space2")
        self.assertNotIn(self.space2, self.space1.get_adjacent_spaces())
        self.assertNotIn(self.space1, self.space2.get_adjacent_spaces())

    def test_add_player(self):
        """Tests adding a player to the space."""
        self.space1.add_player(self.player)
        self.assertIn(self.player, self.space1.get_players())

    def test_remove_player(self):
        """Tests removing a player from the space."""
        self.space1.add_player(self.player)
        self.space1.remove_player(self.player.playerID)
        self.assertNotIn(self.player, self.space1.get_players())

    def test_get_player_count(self):
        """Tests retrieving the count of players in the space."""
        self.space1.add_player(self.player)
        self.assertEqual(self.space1.get_player_count(), 1)
        self.space1.remove_player(self.player.playerID)
        self.assertEqual(self.space1.get_player_count(), 0)

    def test_is_adjacent_room(self):
        """Tests checking if a space is adjacent to another room."""
        self.space1.add_adjacent_space(self.space2)
        self.assertTrue(self.space1.is_adjacent_room("Space2"))
        self.assertFalse(self.space1.is_adjacent_room("NonExistent"))

    def test_eq(self):
        """Tests equality comparison of spaces."""
        space3 = Space("Space1")
        space4 = Space("Space2")
        self.space1.add_adjacent_space(self.space2)
        space3.add_adjacent_space(space4)
        self.assertEqual(self.space1, space3)
        self.assertNotEqual(self.space1, space4)

    def test_get_adjacent_spaces(self):
        """Tests retrieving adjacent spaces."""
        self.space1.add_adjacent_space(self.space2)
        self.assertIn(self.space2, self.space1.get_adjacent_spaces())

    def test_is_player_in_room(self):
        """Tests checking if a player is in the space."""
        self.space1.add_player(self.player)
        self.assertTrue(self.space1.is_player_in_room(self.player.character))

    def test_clear_players(self):
        """Tests clearing all players from the space."""
        self.space1.add_player(self.player)
        self.space1.clear_players()
        self.assertEqual(self.space1.get_player_count(), 0)


class RoomTest(unittest.TestCase):
    """Tests the functionality of the Room class."""
    def setUp(self):
        """Sets up the test data for Room tests."""
        self.room = Room("Room1")
        self.weapon = Card(name="Knife", card_type=CardType.WEAPON)
        self.non_weapon_card = Card(name="RoomKey", card_type=CardType.ITEM)

    def test_add_weapon(self):
        """Tests adding a weapon to the room."""
        self.room.add_weapon(self.weapon)
        self.assertIn(self.weapon, self.room.get_weapons())

    def test_remove_weapon(self):
        """Tests removing a weapon from the room."""
        self.room.add_weapon(self.weapon)
        removed_weapon = self.room.remove_weapon("Knife")
        self.assertEqual(removed_weapon, self.weapon)
        self.assertNotIn(self.weapon, self.room.get_weapons())

    def test_add_invalid_weapon(self):
        """Tests error handling when adding an invalid weapon."""
        with self.assertRaises(ValueError):
            self.room.add_weapon(self.non_weapon_card)

    def test_get_weapons(self):
        """Tests retrieving all weapons in the room."""
        self.room.add_weapon(self.weapon)
        self.assertEqual(self.room.get_weapons(), [self.weapon])


class CornerRoomTest(unittest.TestCase):
    """Tests the functionality of the CornerRoom class."""
    def setUp(self):
        """Sets up the test data for CornerRoom tests."""
        self.corner_room1 = CornerRoom("CornerRoom1")
        self.corner_room2 = CornerRoom("CornerRoom2")
        self.weapon = Card(name="Revolver", card_type=CardType.WEAPON)

    def test_add_secret_passage(self):
        """Tests adding a secret passage to another corner room."""
        self.corner_room1.add_secret_passage(self.corner_room2)
        self.assertEqual(self.corner_room1.get_secret_passage(),
                         self.corner_room2)
        self.assertEqual(self.corner_room2.get_secret_passage(),
                         self.corner_room1)

    def test_remove_secret_passage(self):
        """Tests removing a secret passage."""
        self.corner_room1.add_secret_passage(self.corner_room2)
        removed_room = self.corner_room1.remove_secret_passage()
        self.assertEqual(removed_room, self.corner_room2)
        self.assertIsNone(self.corner_room1.get_secret_passage())
        self.assertIsNone(self.corner_room2.get_secret_passage())

    def test_has_secret_passage(self):
        """Tests checking if a corner room has a secret passage."""
        self.assertFalse(self.corner_room1.has_secret_passage())
        self.corner_room1.add_secret_passage(self.corner_room2)
        self.assertTrue(self.corner_room1.has_secret_passage())


class HallwayTest(unittest.TestCase):
    """Tests the functionality of the Hallway class."""
    def setUp(self):
        """Sets up the test data for Hallway tests."""
        self.hallway = Hallway("Hallway1")
        self.player = Player(playerID=1, character="Player1")

    def test_add_player_to_empty_hallway(self):
        """Tests adding a player to an empty hallway."""
        self.assertTrue(self.hallway.add_player(self.player))
        self.assertIn(self.player, self.hallway.get_players())

    def test_add_player_to_full_hallway(self):
        """Tests adding a player to a hallway that is already full."""
        self.hallway.add_player(self.player)
        new_player = Player(playerID=2, character="Player2")
        self.assertFalse(self.hallway.add_player(new_player))

    def test_is_empty(self):
        """Tests checking if the hallway is empty."""
        self.assertTrue(self.hallway.is_empty())
        self.hallway.add_player(self.player)
        self.assertFalse(self.hallway.is_empty())

    def test_remove_player(self):
        """Tests removing a player from the hallway."""
        self.hallway.add_player(self.player)
        self.hallway.remove_player(self.player.playerID)
        self.assertNotIn(self.player, self.hallway.get_players())
        self.assertTrue(self.hallway.is_empty())


#if __name__ == "__main__":
#    unittest.main()
