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
        study_room = CornerRoom(ValidRooms.STUDY.value)
        self._spaces[ValidRooms.STUDY.value] = study_room
        hall_room = Room(ValidRooms.HALL.value)
        self._spaces[ValidRooms.HALL.value] = hall_room
        lounge_room = CornerRoom(ValidRooms.LOUNGE.value)
        self._spaces[ValidRooms.LOUNGE.value] = lounge_room
        library_room = Room(ValidRooms.LIBRARY.value)
        self._spaces[ValidRooms.LIBRARY.value] = library_room
        billiard_room = Room(ValidRooms.BILLIARDS.value)
        self._spaces[ValidRooms.BILLIARDS.value] = billiard_room
        dining_room = Room(ValidRooms.DINING.value)
        self._spaces[ValidRooms.DINING.value] = dining_room
        conservatory_room = CornerRoom(ValidRooms.CONSERVATORY.value)
        self._spaces[ValidRooms.CONSERVATORY.value] = conservatory_room
        ballroom_room = Room(ValidRooms.BALLROOM.value)
        self._spaces[ValidRooms.BALLROOM.value] = ballroom_room
        kitchen_room = CornerRoom(ValidRooms.KITCHEN.value)
        self._spaces[ValidRooms.KITCHEN.value] = kitchen_room

        # Creats hallways between rooms
        # Horizontal hallways first (left to right)
        study_hall = Hallway(ValidHallways.STUDY_HALL.value)
        self._spaces[ValidHallways.STUDY_HALL.value] = study_hall
        hall_lounge = Hallway(ValidHallways.HALLWAY_LOUNGE.value)
        self._spaces[ValidHallways.HALLWAY_LOUNGE.value] = hall_lounge
        library_billiard = Hallway(ValidHallways.LIBRARY_BILLIARDS.value)
        self._spaces[ValidHallways.LIBRARY_BILLIARDS.value] = library_billiard
        billiard_dining = Hallway(ValidHallways.BILLIARDS_DINING.value)
        self._spaces[ValidHallways.BILLIARDS_DINING.value] = billiard_dining
        conservatory_ballroom = Hallway(ValidHallways.CONSERVATORY_BALLROOM.value)
        self._spaces[ValidHallways.CONSERVATORY_BALLROOM.value] = (
            conservatory_ballroom
        )
        ballroom_kitchen = Hallway(ValidHallways.BALLROOM_KITCHEN.value)
        self._spaces[ValidHallways.BALLROOM_KITCHEN.value] = ballroom_kitchen

        # Vertical hallways (top to bottom)
        study_library = Hallway(ValidHallways.STUDY_LIBRARY.value)
        self._spaces[ValidHallways.STUDY_LIBRARY.value] = study_library
        library_conservatory = Hallway(ValidHallways.LIBRARY_CONSERVATORY.value)
        self._spaces[ValidHallways.LIBRARY_CONSERVATORY.value] = (
            library_conservatory
        )
        hall_billiard = Hallway(ValidHallways.HALL_BILLARD.value)
        self._spaces[ValidHallways.HALL_BILLARD.value] = hall_billiard
        billiard_ballroom = Hallway(ValidHallways.BILLIARD_BALLROOM.value)
        self._spaces[ValidHallways.BILLIARD_BALLROOM.value] = (
            billiard_ballroom
        )
        lounge_dining = Hallway(ValidHallways.LOUNGE_DINING.value)
        self._spaces[ValidHallways.LOUNGE_DINING.value] = lounge_dining
        dining_kitchen = Hallway(ValidHallways.DINING_KITCHEN.value)
        self._spaces[ValidHallways.DINING_KITCHEN.value] = dining_kitchen

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
        print(f"this is the actual space_name being passed in {space_name}\n\n")
        print(self._spaces.keys())
        for item in self._spaces.keys():
            if item == space_name:
                print("***********")
        return self._spaces[space_name]
    
    def get_space_by_enum_value(self, space_name: str) -> Space:
        for room in ValidRooms:
            if space_name == room.value:
                return self._spaces[space_name]
            #

    def set_starting_positions(self):
        """sets the starting positions of"""
        self._start_positions[ValidSuspect.SCARLET.value] = self.get_space_by_name(
            ValidHallways.HALLWAY_LOUNGE.value
        )
        self._start_positions[ValidSuspect.PLUM.value] = self.get_space_by_name(
            ValidHallways.STUDY_LIBRARY.value
        )
        self._start_positions[ValidSuspect.MUSTARD.value] = self.get_space_by_name(
            ValidHallways.LOUNGE_DINING.value
        )
        self._start_positions[ValidSuspect.PEACOCK.value] = self.get_space_by_name(
            ValidHallways.LIBRARY_CONSERVATORY.value
        )
        self._start_positions[ValidSuspect.GREEN.value] = self.get_space_by_name(
            ValidHallways.CONSERVATORY_BALLROOM.value
        )
        self._start_positions[ValidSuspect.WHITE.value] = self.get_space_by_name(
            ValidHallways.BALLROOM_KITCHEN.value
        )

    def get_starting_positions(self) -> Dict[str, Space]:
        return self._start_positions
    
    def get_starting_position(self, character_name: str) -> Space:
        """returns the starting space location of the character"""
        print(f"these are the keys {self._start_positions.keys()}")
        return self._start_positions[character_name]
