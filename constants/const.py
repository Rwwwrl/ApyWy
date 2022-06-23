from typing import Dict, List


class ListOfConstants:
    def __init__(self, *constants):    # type: ignore
        self.constants = constants

    def to_representation(self) -> List[Dict]:
        return [const.to_representation() for const in self.constants]
