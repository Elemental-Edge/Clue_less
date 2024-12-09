from enum import Enum


class ValidRooms(Enum):
    """Enum representation of valid Room names"""

    BALLROOM = "ballroom"
    KITCHEN = "kitchen"
    LIBRARY = "library"
    STUDY = "study"
    HALL = "hall"
    LOUNGE = "lounge"
    DINING = "dining"
    CONSERVATORY = "conservatory"
    BILLIARDS = "billiards"


class ValidSuspect(Enum):
    """Enum representation of valid Suspects names"""

    SCARLET = "scarlet"
    PLUM = "plum"
    PEACOCK = "peacock"
    GREEN = "green"
    MUSTARD = "mustard"
    WHITE = "white"


class ValidWeapons(Enum):
    """Enum representation of Valid Weapons"""

    CANDLESTICK = "candlestick"
    KNIFE = "knife"
    PIPE = "pipe"
    REVOLVER = "revolver"
    ROPE = "rope"
    WRENCH = "wrench"


class ValidHallways(Enum):
    """Enum representations of Valid Hallways"""
    # Horizontal Hallway connections
    STUDY_HALL = f"{ValidRooms.STUDY.value}-{ValidRooms.HALL.value}"
    HALLWAY_LOUNGE = f"{ValidRooms.HALL.value}-{ValidRooms.LOUNGE.value}"
    LIBRARY_BILLIARDS = f"{ValidRooms.LIBRARY.value}-{ValidRooms.BILLIARDS.value}"
    BILLIARDS_DINING = f"{ValidRooms.BILLIARDS.value}-{ValidRooms.DINING.value}"
    CONSERVATORY_BALLROOM = f"{ValidRooms.CONSERVATORY.value}-{ValidRooms.BALLROOM.value}"
    BALLROOM_KITCHEN = f"{ValidRooms.BALLROOM.value}-{ValidRooms.KITCHEN.value}"
    # Vertical Hallway connections
    STUDY_LIBRARY = f"{ValidRooms.STUDY.value}-{ValidRooms.LIBRARY.value}"
    LIBRARY_CONSERVATORY = f"{ValidRooms.LIBRARY.value}-{ValidRooms.CONSERVATORY.value}"
    HALL_BILLARD = f"{ValidRooms.HALL.value}-{ValidRooms.BILLIARDS.value}"
    BILLIARD_BALLROOM = f"{ValidRooms.BILLIARDS.value}-{ValidRooms.BALLROOM.value}"
    LOUNGE_DINING = f"{ValidRooms.LOUNGE.value}-{ValidRooms.DINING.value}"
    DINING_KITCHEN = f"{ValidRooms.DINING.value}-{ValidRooms.KITCHEN.value}"
