from Backend.gameboardGroupings.space import Room, CornerRoom, Hallway, Space
from Backend.commons import ValidSuspect, ValidRooms, ValidHallways
from typing import Dict


class GameBoard:
    """Represents the class Clue gameboard."""

    def __init__(self):
        self._spaces: Dict = {}
        self._start_positions: Dict = {}
        self.setup_gameboard()

    def setup_gameboard(self):
        """Creates the default Clue board layout with all rooms
        and connections"""
        # Creates all room for the default Clue board layout
        study_room = CornerRoom(ValidRooms.STUDY)
        self._spaces[ValidRooms.STUDY] = study_room
        hall_room = Room(ValidRooms.HALL)
        self._spaces[ValidRooms.HALL] = hall_room
        lounge_room = CornerRoom(ValidRooms.LOUNGE)
        self._spaces[ValidRooms.LOUNGE] = lounge_room
        library_room = Room(ValidRooms.LIBRARY)
        self._spaces[ValidRooms.LIBRARY] = library_room
        billiard_room = Room(ValidRooms.BILLIARDS)
        self._spaces[ValidRooms.BILLIARDS] = billiard_room
        dining_room = Room(ValidRooms.DINING)
        self._spaces[ValidRooms.DINING] = dining_room
        conservatory_room = CornerRoom(ValidRooms.CONSERVATORY)
        self._spaces[ValidRooms.CONSERVATORY] = conservatory_room
        ballroom_room = Room(ValidRooms.BALLROOM)
        self._spaces[ValidRooms.BALLROOM] = ballroom_room
        kitchen_room = CornerRoom(ValidRooms.KITCHEN)
        self._spaces[ValidRooms.KITCHEN] = kitchen_room

        # Creats hallways between rooms
        # Horizontal hallways first (left to right)
        study_hall = Hallway(ValidHallways.STUDY_HALL)
        self._spaces[ValidHallways.STUDY_HALL] = study_hall
        hall_lounge = Hallway(ValidHallways.HALLWAY_LOUNGE)
        self._spaces[ValidHallways.HALLWAY_LOUNGE] = hall_lounge
        library_billiard = Hallway(ValidHallways.LIBRARY_BILLIARDS)
        self._spaces[ValidHallways.LIBRARY_BILLIARDS] = library_billiard
        billiard_dining = Hallway(ValidHallways.BILLIARDS_DINING)
        self._spaces[ValidHallways.BILLIARDS_DINING] = billiard_dining
        conservatory_ballroom = Hallway(ValidHallways.CONSERVATORY_BALLROOM)
        self._spaces[ValidHallways.CONSERVATORY_BALLROOM] = (
            conservatory_ballroom
        )
        ballroom_kitchen = Hallway(ValidHallways.BALLROOM_KITCHEN)
        self._spaces[ValidHallways.BALLROOM_KITCHEN] = ballroom_kitchen

        # Vertical hallways (top to bottom)
        study_library = Hallway(ValidHallways.STUDY_LIBRARY)
        self._spaces[ValidHallways.STUDY_LIBRARY] = study_library
        library_conservatory = Hallway(ValidHallways.LIBRARY_CONSERVATORY)
        self._spaces[ValidHallways.LIBRARY_CONSERVATORY] = (
            library_conservatory
        )
        hall_billiard = Hallway(ValidHallways.HALL_BILLARD)
        self._spaces[ValidHallways.HALL_BILLARD] = hall_billiard
        billiard_ballroom = Hallway(ValidHallways.BILLIARD_BALLROOM)
        self._spaces[ValidHallways.BILLIARD_BALLROOM] = (
            billiard_ballroom
        )
        lounge_dining = Hallway(ValidHallways.LOUNGE_DINING)
        self._spaces[ValidHallways.LOUNGE_DINING] = lounge_dining
        dining_kitchen = Hallway(ValidHallways.DINING_KITCHEN)
        self._spaces[ValidHallways.DINING_KITCHEN] = dining_kitchen

        # Connect rooms with hallways
        study_hall.add_adjacent_space(study_room)
        study_hall.add_adjacent_space(hall_room)

        hall_lounge.add_adjacent_space(hall_room)
        hall_lounge.add_adjacent_space(lounge_room)

        library_billiard.add_adjacent_space(library_room)
        library_billiard.add_adjacent_space(billiard_room)

        billiard_dining.add_adjacent_space(billiard_room)
        billiard_dining.add_adjacent_space(dining_room)

        conservatory_ballroom.add_adjacent_space(conservatory_room)
        conservatory_ballroom.add_adjacent_space(ballroom_room)

        ballroom_kitchen.add_adjacent_space(ballroom_room)
        ballroom_kitchen.add_adjacent_space(kitchen_room)

        study_library.add_adjacent_space(study_room)
        study_library.add_adjacent_space(library_room)

        library_conservatory.add_adjacent_space(library_room)
        library_conservatory.add_adjacent_space(conservatory_room)

        hall_billiard.add_adjacent_space(hall_room)
        hall_billiard.add_adjacent_space(billiard_room)

        billiard_ballroom.add_adjacent_space(billiard_room)
        billiard_ballroom.add_adjacent_space(ballroom_room)

        lounge_dining.add_adjacent_space(lounge_room)
        lounge_dining.add_adjacent_space(dining_room)

        dining_kitchen.add_adjacent_space(dining_room)
        dining_kitchen.add_adjacent_space(kitchen_room)

        # Add secret passages between corner rooms
        study_room.add_secret_passage(kitchen_room)
        # Study <-> Kitchen
        lounge_room.add_secret_passage(conservatory_room)
        # Lounge <-> Conservatory

    def get_spaces(self):
        """gets the space object associated with space name"""
        return self._spaces

    def get_space_by_name(self, space_name: str) -> Space:
        return self._spaces[space_name]

    def set_starting_positions(self):
        """sets the starting positions of"""
        self._start_positions[ValidSuspect.SCARLET] = self.get_space_by_name(
            ValidHallways.HALLWAY_LOUNGE
        )
        self._start_positions[ValidSuspect.PLUM] = self.get_space_by_name(
            ValidHallways.STUDY_LIBRARY
        )
        self._start_positions[ValidSuspect.MUSTARD] = self.get_space_by_name(
            ValidHallways.LOUNGE_DINING
        )
        self._start_positions[ValidSuspect.PEACOCK] = self.get_space_by_name(
            ValidHallways.LIBRARY_CONSERVATORY
        )
        self._start_positions[ValidSuspect.GREEN] = self.get_space_by_name(
            ValidHallways.CONSERVATORY_BALLROOM
        )
        self._start_positions[ValidSuspect.WHITE] = self.get_space_by_name(
            ValidHallways.BALLROOM_KITCHEN
        )

    def get_starting_position(self, character_name: str) -> Space:
        """returns the starting space location of the character"""
        return self._start_positions[character_name]
