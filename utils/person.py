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
            self.__birth_date = birth_date
        else:
            self.__birth_date = None
        if isinstance(birth_location, str):
            self.birth_location = birth_location
        else:
            self.birth_location = None

        if isinstance(death_date, Date):
            self.__death_date = birth_date
        else:
            self.__death_date = None
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
        for e in additional_files:
            assert isinstance(e, str)
        self.__additional_files = additional_files
        pass

    def __str__(self) -> str:
        return f"{self.first_name} {self.name}"

    def get__birth_date(self) -> str | None:
        if isinstance(self.__birth_date, Date):
            return str(self.__birth_date)
        return None

    def get__death_date(self) -> str | None:
        if isinstance(self.__death_date, Date):
            return str(self.__death_date)
        return None


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
