from Backend.gameboardGroupings.space import Room, CornerRoom, Hallway, Space
from typing import List

class GameBoard:
    """Represents the class Clue gameboard."""
    def __init__(self):
        self.spaces: List[Space] = []
        self.dictionarySpaces = {}
        self.setup_gameboard()

    def setup_gameboard(self):
        """Creates the default Clue board layout with all rooms and connections"""
        # Creates all room for the default Clue board layout
        study_room = CornerRoom("study")
        self.dictionarySpaces["study"] = study_room
        hall_room = Room("hall")
        self.dictionarySpaces["hall"] = hall_room
        lounge_room = CornerRoom("lounge")
        self.dictionarySpaces["lounge"] = lounge_room
        library_room = Room("library")
        self.dictionarySpaces["library"] = library_room
        billiard_room = Room("billiards")
        self.dictionarySpaces["billiards"] = billiard_room
        dining_room = Room("dining")
        self.dictionarySpaces["dining"] = dining_room
        conservatory_room = CornerRoom("conservatory")
        self.dictionarySpaces["conservatory"] = conservatory_room
        ballroom_room = Room("ballroom")
        self.dictionarySpaces["ballroom"] = ballroom_room
        kitchen_room = CornerRoom("kitchen")
        self.dictionarySpaces["kitchen"] = kitchen_room

        # Creats hallways between rooms
        # Horizontal hallways first (left to right)
        study_hall = Hallway("study-hall")
        self.dictionarySpaces["study-hall"] = study_hall
        hall_lounge = Hallway("hall-lounge")
        self.dictionarySpaces["hall-lounge"] = hall_lounge
        library_billiard = Hallway("library-billiards")
        self.dictionarySpaces["library-billiards"] = library_billiard
        billiard_dining = Hallway("billiards-dining")
        self.dictionarySpaces["billiards-dining"] = billiard_dining
        conservatory_ballroom = Hallway("conservatory-ballroom")
        self.dictionarySpaces["conservatory-ballroom"] = conservatory_ballroom
        ballroom_kitchen = Hallway("ballroom-kitchen")
        self.dictionarySpaces["ballroom-kitchen"] = ballroom_kitchen

        # Vertical hallways (top to bottom)
        study_library = Hallway("study-library")
        self.dictionarySpaces["study-library"] = study_library
        library_conservatory = Hallway("library-conservatory")
        self.dictionarySpaces["library-conservatory"] = library_conservatory
        hall_billiard = Hallway("hall-billiards")
        self.dictionarySpaces["hall-billiards"] = hall_billiard
        billiard_ballroom = Hallway("billiards-ballroom")
        self.dictionarySpaces["billiards-ballroom"] = billiard_ballroom
        lounge_dining = Hallway("lounge-dining")
        self.dictionarySpaces["lounge-dining"] = lounge_dining
        dining_kitchen = Hallway("dining-kitchen")
        self.dictionarySpaces["dining-kitchen"] = dining_kitchen

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

        # store all spaces
        self.spaces.extend([
            study_room, hall_room, lounge_room,
            library_room, billiard_room, dining_room,
            conservatory_room, ballroom_room, kitchen_room,
            study_hall, hall_lounge,
            library_billiard, billiard_dining,
            conservatory_ballroom, ballroom_kitchen,
            study_library, library_conservatory,
            hall_billiard, billiard_ballroom,
            lounge_dining, dining_kitchen])

    def get_space_by_name(self, space_name: str) -> Space:
        return self.dictionarySpaces[space_name]

    # def get_all_spaces(self) -> List[Space]:
    #     """Returns all sapces on the board"""
    #     return self.spaces

    # def get_starting_positions(self):


