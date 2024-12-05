from Backend.gameboardGroupings.space import Room, CornerRoom, Hallway, Space
from typing import List

class GameBoard:
    """Represents the class Clue gameboard."""
    def __init__(self):
        self.spaces: List[Space] = []
        self.setup_gameboard()

    def setup_gameboard(self):
        """Creates the default Clue board layout with all rooms and connections"""
        # Creates all room for the default Clue board layout
        study_room = CornerRoom("Study")
        hall_room = Room("Hall")
        lounge_room = CornerRoom("Lounge")
        library_room = Room("Library")
        billiard_room = Room("Billiard Room")
        dining_room = Room("Dining Room")
        conservatory_room = CornerRoom("Conservatory")
        ballroom_room = Room("Ballroom")
        kitchen_room = CornerRoom("Kitchen")

        # Creats hallways between rooms
        # Horizontal hallways first (left to right)
        study_hall = Hallway()
        hall_lounge = Hallway()
        library_billiard = Hallway()
        billiard_dining = Hallway()
        conservatory_ballroom = Hallway()
        ballroom_kitchen = Hallway()

        # Vertical hallways (top to bottom)
        study_library = Hallway()
        library_conservatory = Hallway()
        hall_billiard = Hallway()
        billiard_ballroom = Hallway()
        lounge_dining = Hallway()
        dining_kitchen = Hallway()

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
        
    def get_all_spaces(self) -> List[Space]:
        """Returns all sapces on the board"""
        return self.spaces

    # def get_starting_positions(self):


