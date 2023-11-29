import sqlite3, os
from utils.person import Person, Sex
from utils.family import Family
from utils.date import Date, parse_date


class Sql:
    def __init__(self, filepath: str) -> None:
        """Create the Sql Object

        Args:
            filepath (str): Path to the database file
        """
        assert isinstance(filepath, str)
        does_file_already_exist = os.path.isfile(filepath)
        self.__sql_conn = sqlite3.connect(filepath)
        self.__cursor = self.__sql_conn.cursor()
        if not does_file_already_exist:
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

    def get_all_persons(self):
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
        for row in self.__cursor.execute("SELECT * FROM Person"):
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

    def get_all_families(self):
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
        for row in self.__cursor.execute("SELECT * FROM Family"):
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
                for child_id in family[3]:
                    childs.append(persons[int(child_id)])
            wedding_date: Date | None = None if family[4] is None else parse_date(family[4])

            families[family[0]] = Family(family[0], persons[family[1]], persons[family[2]], childs, wedding_date)
        return families

    def __del__(self):
        self.__cursor.close()
        self.__sql_conn.close()
        pass
