from typing import Literal
from utils.family import Family
from utils.person import Person


class Person4Tree:
    def __init__(self, person: Person, family: Family) -> None:
        assert isinstance(person, Person)
        assert isinstance(family, Family)
        self.person = person

        self.attributes: list[tuple[Literal["dad", "mom", "child"], Family]] = []

        if person.id == family.dad.id:
            self.attributes.append(("dad", family))
        elif person.id == family.mom.id:
            self.attributes.append(("mom", family))
        for child in family.childs:
            if child.id == person.id:
                self.attributes.append(("child", family))

        pass


class Families:
    def __init__(self, families: dict[int, Family]) -> None:
        self.__families = families[0]

    def add(self, family: Family) -> None:
        pass
