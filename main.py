from utils.date import Date
from utils.family import Family
from utils.person import Person, Sex
from utils.sql import Sql



sql = Sql('data.db')
list_persons = sql.parse_all_persons(sql.get_all_persons())
print(sql.parse_all_families(sql.get_all_families(),list_persons))
#print(list_persons[0].get__birth_date())
#print(sql.get_all_families())