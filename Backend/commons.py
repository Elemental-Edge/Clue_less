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
    DAGGER = "dagger"
    PIPE = "pipe"
    REVOLVER = "revolver"
    ROPE = "rope"
    WRENCH = "wrench"
