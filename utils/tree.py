from utils.person import Person, Family
from utils.image import PersonImage
import graphviz


class TreeGen:
    def __init__(self, persons: dict[int, Person], families: dict[int, Family]) -> None:
        self.__persons = persons
        self.__families = families
        self.__initialize_persons()
        pass

    def __initialize_persons(self):
        for person_id in self.__persons.keys():
            person = self.__persons[person_id]
            for family_id in self.__families.keys():
                family = self.__families[family_id]
                lst_family = [family.dad, family.mom]
                lst_family.extend(family.childs)
                lst_id_in_family = map(self.__get_id_of_person, lst_family)
                if person_id in lst_id_in_family:
                    if person_id == family.dad.id:
                        person.attributes.append(("dad", family))
                    elif person_id == family.mom.id:
                        person.attributes.append(("mom", family))
                    elif person_id in map(self.__get_id_of_person, family.childs):
                        person.attributes.append(("child", family))

    def __get_id_of_person(self, person: Person):
        return person.id

    def clear_attributes(self):
        for person_id in self.__persons.keys():
            self.__persons[person_id].attributes.clear()

    def update_persons(self, persons: dict[int, Person], families: dict[int, Family]):
        self.__persons = persons
        self.__families = families
        self.clear_attributes()
        self.__initialize_persons()

    def gen_cards(self):
        for person_id in self.__persons.keys():
            PersonImage(self.__persons[person_id], True).save()

    def gen_tree(self):
        self.gen_cards()
        dot = graphviz.Digraph("Tree", format="pdf", node_attr={"shape": "plaintext"})
        for person_id in self.__persons.keys():
            person = self.__persons[person_id]
            dot.node(f"{person.id}{person.first_name.lower()}", " ", image=f"./cards/{person.id}{person.first_name.lower()}.png")  # type: ignore
        dot.render("./data/tree.gv", view=True)  # type: ignore
        pass
