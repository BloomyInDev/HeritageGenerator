import sqlite3, os
from utils.person import Person, Family
from utils.date import Date, parse_date


class Sql:
    def __init__(self, filepath: str, create_from_scratch: bool = False) -> None:
        """Create the Sql Object

        Args:
            filepath (str): Path to the database file
        """
        assert isinstance(filepath, str)
        does_file_already_exist = os.path.isfile(filepath)
        self.__sql_conn = sqlite3.connect(filepath)
        if not does_file_already_exist:
            self.__init_db()
        elif create_from_scratch:
            self.__sql_conn.close()
            os.remove(filepath)
            self.__sql_conn = sqlite3.connect(filepath)
            self.__init_db()
        pass

    def __init_db(self):
        init_db_cmd = """
        CREATE TABLE "Family" (
            "Id"	INTEGER NOT NULL UNIQUE,
            "Dad"	INTEGER NOT NULL,
            "Mom"	INTEGER NOT NULL,
            "Childs"	TEXT,
            "WeddingDate"	TEXT,
            "WeddingLocation"	TEXT,
            "DivorceDate"	TEXT,
            "DivorceLocation"	TEXT,
            "Notes"	TEXT,
            "AdditionalFiles"	TEXT,
            PRIMARY KEY("Id" AUTOINCREMENT)
        );
        CREATE TABLE "Person" (
            "Id"	INTEGER NOT NULL UNIQUE,
            "Name"	TEXT NOT NULL,
            "FirstName"	TEXT NOT NULL,
            "OldName"	TEXT,
            "BirthDate"	TEXT,
            "BirthLocation"	TEXT,
            "DeathDate"	TEXT,
            "DeathLocation"	TEXT,
            "Job"	TEXT,
            "Notes"	TEXT,
            "AdditionalFiles"	TEXT,
            PRIMARY KEY("Id" AUTOINCREMENT)
        );
        """
        self.__sql_conn.executescript(init_db_cmd)
        self.__sql_conn.commit()

    def get_all_persons_raw(self):
        data: list[
            tuple[
                int,
                str,
                str,
                str | None,
                str | None,
                str | None,
                str | None,
                str | None,
                str | None,
                str | None,
                str | None,
            ]
        ] = []
        cursor = self.__sql_conn.cursor()
        for row in cursor.execute("SELECT * FROM Person"):
            data.append(row)
        return data

    def parse_all_persons(
        self,
        to_parse: list[
            tuple[
                int,
                str,
                str,
                str | None,
                str | None,
                str | None,
                str | None,
                str | None,
                str | None,
                str | None,
                str | None,
            ]
        ],
    ) -> dict[int, Person]:
        persons: dict[int, Person] = {}
        for person in to_parse:
            birth_date, death_date = None, None
            if isinstance(person[4], str):
                birth_date: Date | None = parse_date(person[4])
            if isinstance(person[6], str):
                death_date: Date | None = parse_date(person[6])
            newperson = Person(
                person[0],
                person[1],
                person[2],
                person[3],
                birth_date,
                person[5],
                death_date,
                person[7],
                person[8],
                person[9],
            )
            persons[newperson.id] = newperson
        return persons

    def get_all_persons(self):
        return self.parse_all_persons(self.get_all_persons_raw())

    def get_all_families_raw(self):
        data: list[
            tuple[
                int,
                int,
                int,
                str | None,
                str | None,
                str | None,
                str | None,
                str | None,
                str | None,
                str | None,
            ]
        ] = []
        cursor = self.__sql_conn.cursor()
        for row in cursor.execute("SELECT * FROM Family"):
            data.append(row)
        return data

    def parse_all_families(
        self,
        to_parse: list[
            tuple[
                int,
                int,
                int,
                str | None,
                str | None,
                str | None,
                str | None,
                str | None,
                str | None,
                str | None,
            ]
        ],
        persons: dict[int, Person],
    ):
        families: dict[int, Family] = {}
        for family in to_parse:
            childs: list[Person] = []
            if family[3] != None:
                for child_id in str(family[3]).split(","):
                    childs.append(persons[int(child_id)])
            wedding_date: Date | None = None if family[4] is None else parse_date(family[4])

            families[family[0]] = Family(family[0], persons[family[1]], persons[family[2]], childs, wedding_date)
        return families

    def get_all_families(self):
        return self.parse_all_families(self.get_all_families_raw(), self.get_all_persons())

    def create_new_person(self, person: Person):
        assert isinstance(person, Person)
        person_list = self.get_all_persons()
        if person.id in person_list.keys():
            new_id = 0
            for i in person_list.keys():
                if i > new_id:
                    new_id = i
            person.id = new_id
        self.__sql_conn.cursor().execute(
            """
            INSERT INTO Person(Id,Name,FirstName,OldName,BirthDate,BirthLocation,DeathDate,DeathLocation,Job,Notes,AdditionalFiles)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                person.id,
                person.name,
                person.first_name,
                person.old_name,
                person.get_birth_date(),
                person.birth_location,
                person.get_death_date(),
                person.death_location,
                person.job,
                person.notes,
                person.get_additional_files(as_string=True),
            ),
        )
        self.__sql_conn.commit()

    def edit_person(self, person: Person):
        assert isinstance(person, Person)
        assert person.id in self.get_all_persons().keys()
        self.__sql_conn.cursor().execute(
            f"UPDATE Person SET Name=?, FirstName=?, OldName=?, BirthDate=?, BirthLocation=?, DeathDate=?, DeathLocation=?, Job=?, Notes=?, AdditionalFiles=? WHERE Id={person.id}",
            (
                person.name,
                person.first_name,
                person.old_name,
                person.get_birth_date(),
                person.birth_location,
                person.get_death_date(),
                person.death_location,
                person.job,
                person.notes,
                person.get_additional_files(as_string=True),
            ),
        )
        self.__sql_conn.commit()

    def delete_person(self, id: int):
        assert isinstance(id, int)
        assert id in self.get_all_persons().keys()
        self.__sql_conn.cursor().execute("DELETE FROM Person WHERE Id=?", (id,))
        self.__sql_conn.commit()

    def create_new_family(self, family: Family):
        assert isinstance(family, Family)
        family_list = self.get_all_families()
        if family.id in family_list.keys():
            new_id = 0
            for i in family_list.keys():
                if i > new_id:
                    new_id = i
            family.id = new_id
        format_childs = ""
        for child in family.childs:
            if len(format_childs) != 0:
                format_childs += f",{child.id}"
            else:
                format_childs += f"{child.id}"
        self.__sql_conn.cursor().execute(
            """
            INSERT INTO Family(Id,Dad,Mom,Childs,WeddingDate,WeddingLocation,DivorceDate,DivorceLocatio,Notes)
            VALUES (?,?,?,?,?,?,?,?,?)
            """,
            (
                family.id,
                family.dad,
                family.mom,
                format_childs,
                family.get_wedding_date(),
                family.wedding_location,
                family.get_divorce_date(),
                family.divorce_location,
                family.notes,
                None,
            ),
        )

    def close(self):
        self.__sql_conn.commit()
        self.__sql_conn.close()
        del self
        pass
