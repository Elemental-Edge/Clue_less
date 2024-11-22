from space import Room, CornerRoom, Hallway
from typing import List, Dict

class GameBoard:
    """Represents the classic Clue game board."""

    def __init__(self):
        self.spaces: List[Space] = []
        self._setup_board()

    def _setup_board(self) -> None:
        """Creates the default Clue board layout with all rooms and connections."""
        # Create all rooms
        study = CornerRoom("Study")
        hall = Room("Hall")
        lounge = CornerRoom("Lounge")
        library = Room("Library")
        billiard = Room("Billiard Room")
        dining = Room("Dining Room")
        conservatory = CornerRoom("Conservatory")
        ballroom = Room("Ballroom")
        kitchen = CornerRoom("Kitchen")

        # Create hallways between rooms
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
        study_hall.add_adjacent_space(study)
        study_hall.add_adjacent_space(hall)
        
        hall_lounge.add_adjacent_space(hall)
        hall_lounge.add_adjacent_space(lounge)
        
        library_billiard.add_adjacent_space(library)
        library_billiard.add_adjacent_space(billiard)
        
        billiard_dining.add_adjacent_space(billiard)
        billiard_dining.add_adjacent_space(dining)
        
        conservatory_ballroom.add_adjacent_space(conservatory)
        conservatory_ballroom.add_adjacent_space(ballroom)
        
        ballroom_kitchen.add_adjacent_space(ballroom)
        ballroom_kitchen.add_adjacent_space(kitchen)
        
        study_library.add_adjacent_space(study)
        study_library.add_adjacent_space(library)
        
        library_conservatory.add_adjacent_space(library)
        library_conservatory.add_adjacent_space(conservatory)
        
        hall_billiard.add_adjacent_space(hall)
        hall_billiard.add_adjacent_space(billiard)
        
        billiard_ballroom.add_adjacent_space(billiard)
        billiard_ballroom.add_adjacent_space(ballroom)
        
        lounge_dining.add_adjacent_space(lounge)
        lounge_dining.add_adjacent_space(dining)
        
        dining_kitchen.add_adjacent_space(dining)
        dining_kitchen.add_adjacent_space(kitchen)

        # Add secret passages between corner rooms
        study.add_secret_passage(kitchen)  # Study <-> Kitchen
        lounge.add_secret_passage(conservatory)  # Lounge <-> Conservatory

        # Store all spaces
        self.spaces.extend([
            study, hall, lounge,
            library, billiard, dining,
            conservatory, ballroom, kitchen,
            study_hall, hall_lounge,
            library_billiard, billiard_dining,
            conservatory_ballroom, ballroom_kitchen,
            study_library, library_conservatory,
            hall_billiard, billiard_ballroom,
            lounge_dining, dining_kitchen
        ])

    def get_all_spaces(self) -> List[Space]:
        """Returns all spaces on the board."""
        return self.spaces
