
from __future__ import annotations
from typing import List

class Player_Turn():

    def __init__(self):
        self.reset()
        pass
    def reset(self):
        self._isActive: bool = False
        self._hasMadeAccusation: bool = False
        self._hasMadeSuggestion: bool = False
        self._hasEnteredRoom: bool = False
        self._hasMoved: bool = False

    def get_hasMadeAccusation(self) -> bool:
        return self._hasMadeAccusation

    def get_hasMadeSuggestion(self) -> bool:
        return self._hasMadeSuggestion

    def get_hasMoved(self) -> bool:
        return self._hasMoved

    def get_hasEnteredRoom(self) -> bool:
        return self._hasEnteredRoom

    def set_hasMadeAccusation(self, val: bool = True):
        self._hasMadeAccusation = val

    def set_hasMoved(self, val: bool = True):
        self._hasMoved = val

    def set_hasMadeSuggestion(self, val: bool = True):
        self._hasMadeSuggestion = val

    def set_hasEnteredRoom(self, val: bool = True):
        self._hasEnteredRoom = True
    # isActive becomes True only when get_valid_actions() is called

    def get_valid_actions(self) -> List[str]:
        return_list = []
        self._isActive = True
        if (self._hasEnteredRoom or self._hasMoved) and not self._hasMadeSuggestion:
            return_list.append("Suggestion")
        if not self._hasMadeAccusation:
            return_list.append("Accusation")
        if not self._hasMoved and not self._hasMadeAccusation:
            return_list.append("Move")
        return return_list
