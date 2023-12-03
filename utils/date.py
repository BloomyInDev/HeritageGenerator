class Date:
    def __init__(self, day: int | str, month: int | str, year: int | str) -> None:
        if type(day) == str:
            assert day.isnumeric(), "day must be an string that can be converted to an int or an int"
            self.__day = int(day)
        else:
            assert isinstance(day, int), "day must be an string that can be converted to an int or an int"
            self.__day = day
        if type(month) == str:
            assert month.isnumeric(), "month must be an string that can be converted to an int or an int"
            self.__month = int(month)
        else:
            assert isinstance(month, int), "month must be an string that can be converted to an int or an int"
            self.__month = month
        if type(year) == str:
            assert year.isnumeric(), "year must be an string that can be converted to an int or an int"
            self.__year = int(year)
        else:
            assert isinstance(year, int), "year must be an string that can be converted to an int or an int"
            self.__year = year

        assert is_valid_date(self.__year, self.__month, self.__day), "date is invalid (1<=month<=12 or 1<=day<=last_day_of_month)"
        pass

    def get_str(self, separator: str = "/"):
        day = str(self.__day)
        if len(day) == 1:
            day = f"0{day}"
        month = str(self.__month)
        if len(month) == 1:
            month = f"0{month}"
        year = str(self.__year)
        return f"{day}{separator}{month}{separator}{year}"

    def __str__(self) -> str:
        return self.get_str("/")

    def get_day(self) -> int:
        return self.__day

    def get_month(self) -> int:
        return self.__month

    def get_year(self) -> int:
        return self.__year


def is_valid_date(year: int, month: int, day: int) -> bool:
    day_count_for_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        day_count_for_month[2] = 29
    return 1 <= month <= 12 and 1 <= day <= day_count_for_month[month]


def parse_date(date: str | None) -> Date | None:
    if isinstance(date, str):
        splitted_date = date.split("/")
        if len(splitted_date) == 3:
            return Date(splitted_date[0], splitted_date[1], splitted_date[2])
    return None
