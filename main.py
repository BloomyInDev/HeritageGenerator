from utils.sql import Sql


sql = Sql("data.db")
list_persons = sql.get_all_persons()
list_families = sql.get_all_families()
print(list_families)
# print(list_persons[0].get__birth_date())
# print(sql.get_all_families())
