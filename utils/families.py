from utils.family import Family


class Families:
    def __init__(self) -> None:
        self.__families: dict[int, Family] = {}
        pass

    def add(self, family: Family) -> None:
        new_index = 0
        while new_index in list(self.__families.keys()):
            new_index += 1
        self.__families[new_index] = family
        pass
