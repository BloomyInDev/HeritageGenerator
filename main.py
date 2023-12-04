from utils.sql import Sql
from utils.tree import TreeGen

# from utils.images import get_text_width, Font

print()
sql = Sql("data.db")
list_persons = sql.get_all_persons()
list_families = sql.get_all_families()
print(list_families)
TreeGen(list_persons, list_families).gen_tree("full", 1, "pdf")
# dict_sizes = {}
# for font in [("smol", Font.small), ("medium", Font.medium), ("big", Font.big), ("really_big", Font.really_big)]:
#    dict_sizes[font[0]] = get_text_width("Bonjour", font[1])
# print(dict_sizes)
# print(list_persons[0].get__birth_date())
# print(sql.get_all_families())
