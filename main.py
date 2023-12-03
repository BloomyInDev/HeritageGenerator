from utils.sql import Sql
from utils.tree import TreeGen


sql = Sql("data.db")
list_persons = sql.get_all_persons()
list_families = sql.get_all_families()
print(list_families)
TreeGen(list_persons, list_families).gen_tree()
# print(list_persons[0].get__birth_date())
# print(sql.get_all_families())
