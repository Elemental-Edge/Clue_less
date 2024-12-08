from Backend.gameboardGroupings.space import Room, CornerRoom, Hallway, Space
from Backend.cardGroupings.Card import ValidRooms
from typing import List

class GameBoard:
    """Represents the class Clue gameboard."""
    def __init__(self):
        self._spaces = {}
        self.setup_gameboard()

    def setup_gameboard(self):
        """Creates the default Clue board layout with all rooms and connections"""
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
        study_hall = Hallway(f"{ValidRooms.STUDY}-{ValidRooms.HALL}")
        self._spaces[f"{ValidRooms.STUDY}-{ValidRooms.HALL}"] = study_hall
        hall_lounge = Hallway(f"{ValidRooms.HALL}-{ValidRooms.LOUNGE}")
        self._spaces[f"{ValidRooms.HALL}-{ValidRooms.LOUNGE}"] = hall_lounge
        library_billiard = Hallway(f"{ValidRooms.LIBRARY}-{ValidRooms.BILLIARDS}")
        self._spaces[f"{ValidRooms.LIBRARY}-{ValidRooms.BILLIARDS}"] = library_billiard
        billiard_dining = Hallway(f"{ValidRooms.BILLIARDS}-{ValidRooms.DINING}")
        self._spaces[f"{ValidRooms.BILLIARDS}-{ValidRooms.DINING}"] = billiard_dining
        conservatory_ballroom = Hallway(f"{ValidRooms.CONSERVATORY}-{ValidRooms.BALLROOM}")
        self._spaces[f"{ValidRooms.CONSERVATORY}-{ValidRooms.BALLROOM}"] = conservatory_ballroom
        ballroom_kitchen = Hallway(f"{ValidRooms.KITCHEN}-{ValidRooms.KITCHEN}")
        self._spaces[f"{ValidRooms.KITCHEN}-{ValidRooms.KITCHEN}"] = ballroom_kitchen

        # Vertical hallways (top to bottom)
        study_library = Hallway(f"{ValidRooms.STUDY}-{ValidRooms.LIBRARY}")
        self._spaces[f"{ValidRooms.STUDY}-{ValidRooms.LIBRARY}"] = study_library
        library_conservatory = Hallway(f"{ValidRooms.LIBRARY}-{ValidRooms.CONSERVATORY}")
        self._spaces[f"{ValidRooms.LIBRARY}-{ValidRooms.CONSERVATORY}"] = library_conservatory
        hall_billiard = Hallway(f"{ValidRooms.HALL}-{ValidRooms.BILLIARDS}")
        self._spaces[f"{ValidRooms.HALL}-{ValidRooms.BILLIARDS}"] = hall_billiard
        billiard_ballroom = Hallway(f"{ValidRooms.BILLIARDS}-{ValidRooms.BALLROOM}")
        self._spaces[f"{ValidRooms.BILLIARDS}-{ValidRooms.BALLROOM}"] = billiard_ballroom
        lounge_dining = Hallway(f"{ValidRooms.LOUNGE}-{ValidRooms.DINING}")
        self._spaces[f"{ValidRooms.LOUNGE}-{ValidRooms.DINING}"] = lounge_dining
        dining_kitchen = Hallway(f"{ValidRooms.DINING}-{ValidRooms.KITCHEN}")
        self._spaces[f"{ValidRooms.DINING}-{ValidRooms.KITCHEN}"] = dining_kitchen

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
        study_room.add_secret_passage(kitchen_room)  # Study <-> Kitchen
        lounge_room.add_secret_passage(conservatory_room)  # Lounge <-> Conservatory

    def get_spaces(self):
        return self._spaces

    def get_space_by_name(self, space_name: str) -> Space:
        return self._spaces[space_name]

    # def get_all_spaces(self) -> List[Space]:
    #     """Returns all sapces on the board"""
    #     return self.spaces

    # def get_starting_positions(self):


