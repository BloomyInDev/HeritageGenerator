from __future__ import annotations
from typing import Literal
from utils.date import Date


class Person:
    def __init__(
        self,
        id: int,
        name: str,
        first_name: str,
        old_name: str | None = None,
        birth_date: Date | None = None,
        birth_location: str | None = None,
        death_date: Date | None = None,
        death_location: str | None = None,
        job: str | None = None,
        notes: str | None = None,
        additional_files: list[str] = [],
    ) -> None:
        assert isinstance(id, int)
        assert isinstance(name, str)
        assert isinstance(first_name, str)
        assert isinstance(old_name, str | None)
        assert isinstance(birth_date, Date | None)
        self.id = id
        self.name = name
        self.first_name = first_name

        if isinstance(old_name, str):
            self.old_name = old_name
        else:
            self.old_name = None

        if isinstance(birth_date, Date):
            self.birth_date = birth_date
        else:
            self.birth_date = None
        if isinstance(birth_location, str):
            self.birth_location = birth_location
        else:
            self.birth_location = None

        if isinstance(death_date, Date):
            self.death_date = birth_date
        else:
            self.death_date = None
        if isinstance(death_location, str):
            self.death_location = death_location
        else:
            self.death_location = None
        if isinstance(job, str):
            self.job = job
        else:
            self.job = None
        if isinstance(notes, str):
            self.notes = notes
        else:
            self.notes = None

        ## Reimplement additional files system
        # for e in additional_files:
        #    assert isinstance(e, str)
        # self.__additional_files = additional_files
        self.__additional_files: list[str] = []

        self.attributes: list[tuple[Literal["dad", "mom", "child"], Family]] = []
        pass

    def __str__(self) -> str:
        return f"{self.first_name} {self.name}"

    def get_birth_date(self) -> str | None:
        if isinstance(self.birth_date, Date):
            return str(self.birth_date)
        return None

    def get_birth_str(self) -> str:
        final_str = ""
        if self.birth_date != None:
            final_str += self.birth_date.get_str()
            if self.birth_location != None:
                final_str += ", "
        if self.birth_location != None:
            final_str += self.birth_location
        return final_str

    def get_death_date(self) -> str | None:
        if isinstance(self.death_date, Date):
            return str(self.death_date)
        return None

    def get_death_str(self) -> str:
        final_str = ""
        if self.death_date != None:
            final_str += self.death_date.get_str()
            if self.death_location != None:
                final_str += ", "
        if self.death_location != None:
            final_str += self.death_location
        return final_str

    def get_additional_files(self, as_string: bool = False) -> list[str] | str | None:
        if as_string:
            final_string = ""
            for file in self.__additional_files:
                final_string += f'"{file}"'
            return final_string
        else:
            return self.__additional_files


class Sex:
    def __init__(self, sex: bool) -> None:
        """
        Input ->
            sex -> boolean, True if men, else False
        """
        assert isinstance(sex, bool)
        self.__sex = sex
        pass

    def get(self):
        return self.__sex


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
        notes: str | None = None,
    ) -> None:
        assert isinstance(id, int)
        assert isinstance(mom, Person)
        assert isinstance(dad, Person)
        assert isinstance(childs, list)
        self.id: int = id
        self.mom: Person = mom
        self.dad: Person = dad
        self.childs: list[Person] = []
        for child in childs:
            assert isinstance(child, Person)
            self.childs.append(child)
        if isinstance(wedding_date, Date):
            self.wedding_date = wedding_date
        else:
            self.wedding_date = None
        if isinstance(wedding_location, str):
            self.wedding_location = wedding_location
        else:
            self.wedding_location = None
        if isinstance(divorce_date, Date):
            self.divorce_date = divorce_date
        else:
            self.divorce_date = None
        if isinstance(divorce_location, str):
            self.divorce_location = divorce_location
        else:
            self.divorce_location = None
        if isinstance(notes, str):
            self.notes = notes
        else:
            self.notes = None
        pass

    def get_wedding_date(self) -> str | None:
        if isinstance(self.wedding_date, Date):
            return str(self.wedding_date)
        return None

    def get_wedding_str(self) -> str:
        final_str = ""
        if self.wedding_date != None:
            final_str += self.wedding_date.get_str()
            if self.wedding_location != None:
                final_str += ", "
        if self.wedding_location != None:
            final_str += self.wedding_location
        return final_str

    def get_divorce_date(self) -> str | None:
        if isinstance(self.divorce_date, Date):
            return str(self.divorce_date)
        return None

    def get_divorce_str(self) -> str:
        final_str = ""
        if self.divorce_date != None:
            final_str += self.divorce_date.get_str()
            if self.divorce_location != None:
                final_str += ", "
        if self.divorce_location != None:
            final_str += self.divorce_location
        return final_str


## Example for Family class

# "id":family[0],
# "dad":persons[family[1]],
# "mom":persons[family[2]],
# "childs":childs,
# "wedding":{"date":family[4],"location":family[5]},
# "divorce":{"date":family[6],"location":family[7]},
# "notes":
