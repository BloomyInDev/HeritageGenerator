from utils.person import Person
from utils.date import Date


class Family:
    def __init__(
        self,
        id: int,
        dad: Person,
        mom: Person,
        childs: list[Person],
        wedding_date: Date | None = None,
        wedding_location: str | None = None,
        divorce_date: Date | None = None,
        divorce_location: str | None = None,
    ) -> None:
        assert isinstance(id, int)
        assert isinstance(mom, Person)
        assert isinstance(dad, Person)
        assert isinstance(childs, list)
        self.__id: int = id
        self.mom: Person = mom
        self.dad: Person = dad
        self.childs: list[Person] = []
        for child in childs:
            assert isinstance(child, Person)
            self.childs.append(child)
        if isinstance(wedding_date, Date):
            self.__wedding__date = wedding_date
        else:
            self.__wedding__date = None
        if isinstance(wedding_location, str):
            self.wedding_location = wedding_location
        else:
            self.wedding_location = None
        if isinstance(divorce_date, Date):
            self.__divorce__date = divorce_date
        else:
            self.__divorce__date = None
        if isinstance(divorce_location, str):
            self.divorce_location = divorce_location
        else:
            self.divorce_location = None
        pass


## Example

# "id":family[0],
# "dad":persons[family[1]],
# "mom":persons[family[2]],
# "childs":childs,
# "wedding":{"date":family[4],"location":family[5]},
# "divorce":{"date":family[6],"location":family[7]},
# "notes":
