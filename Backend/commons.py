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
    STUDY_HALL = f"{ValidRooms.STUDY}-{ValidRooms.HALL}"
    HALLWAY_LOUNGE = f"{ValidRooms.HALL}-{ValidRooms.LOUNGE}"
    LIBRARY_BILLIARDS = f"{ValidRooms.LIBRARY}-{ValidRooms.BILLIARDS}"
    BILLIARDS_DINING = f"{ValidRooms.BILLIARDS}-{ValidRooms.DINING}"
    CONSERVATORY_BALLROOM = f"{ValidRooms.CONSERVATORY}-{ValidRooms.BALLROOM}"
    BALLROOM_KITCHEN = f"{ValidRooms.BALLROOM}-{ValidRooms.KITCHEN}"
    # Vertical Hallway connections
    STUDY_LIBRARY = f"{ValidRooms.STUDY}-{ValidRooms.LIBRARY}"
    LIBRARY_CONSERVATORY = f"{ValidRooms.LIBRARY}-{ValidRooms.CONSERVATORY}"
    HALL_BILLARD = f"{ValidRooms.HALL}-{ValidRooms.BILLIARDS}"
    BILLIARD_BALLROOM = f"{ValidRooms.BILLIARDS}-{ValidRooms.BALLROOM}"
    LOUNGE_DINING = f"{ValidRooms.LOUNGE}-{ValidRooms.DINING}"
    DINING_KITCHEN = f"{ValidRooms.DINING}-{ValidRooms.KITCHEN}"
