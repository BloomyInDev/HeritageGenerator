from typing import Literal
from utils.person import Person, Family
from utils.images import PersonCard, FamilyCard
import graphviz, shutil, os, datetime  # type: ignore

graphviz_supported_format = Literal["png", "pdf", "svg"]


class TreeGen:
    def __init__(self, ui, persons: dict[int, Person], families: dict[int, Family]) -> None:
        """Class TreeGen
        It also run initializes all the persons

        Args:
            persons (dict[int, Person]): The output of Sql.get_all_persons() (preferably)
            families (dict[int, Family]): The output of Sql.get_all_families() (preferably)
        """
        self.__persons = persons
        self.__families = families
        self.__initialize_persons()
        pass

    def get_persons(self):
        """
        Get Persons
        """
        return self.__persons

    def get_families(self):
        """
        Get Families
        """
        return self.__families

    def __initialize_persons(self):
        """
        Simple helper method to set all Person theirs family links
        """
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
        """
        Simple helper method to get the id of a Person

        Args:
            person (Person): A person

        Returns:
            int: id of the person
        """
        return person.id

    def clear_attributes(self):
        """
        Simple helper method that remove ALL attributes to ALL persons
        """
        for person_id in self.__persons.keys():
            self.__persons[person_id].attributes.clear()

    def update_persons(self, persons: dict[int, Person], families: dict[int, Family]):
        """
        Redo all the things done on init with new values

        Args:
            persons (dict[int, Person]): The output of Sql.get_all_persons() (preferably)
            families (dict[int, Family]): The output of Sql.get_all_families() (preferably)
        """
        self.__persons = persons
        self.__families = families
        self.clear_attributes()
        self.__initialize_persons()

    def gen_cards(self):
        """
        Generate images for every Person and Family
        """
        for person_id in self.__persons.keys():
            PersonCard(self.__persons[person_id], prepare_image=True).save()
        for family_id in self.__families.keys():
            FamilyCard(self.__families[family_id], prepare_image=True).save()

    def gen_tree(self, tree_type: Literal["full", "ancestors", "descendants"], person_id: int | None, format: graphviz_supported_format = "pdf", open: bool = False):
        match tree_type:
            case "full":
                return self.__gen_full_tree(format, open)
            case "ancestors":
                assert isinstance(person_id, int)
                return self.__gen_ancestors_tree(person_id, format, open)
            case "descendants":
                assert isinstance(person_id, int)
                return self.__gen_descendants_tree(person_id, format, open)

    def __gen_full_tree(self, format: graphviz_supported_format, open: bool = False):
        """
        Generate the Family Tree of everyone

        Args:
            format (Literal[&quot;png&quot;, &quot;pdf&quot;], optional): Export file type.
        """
        self.gen_cards()
        dot = graphviz.Digraph("Tree", format=format, node_attr={"shape": "plaintext"})
        for person_id in self.__persons.keys():
            person = self.__persons[person_id]
            dot.node(f"P{person.id}{person.first_name.lower()}", " ", image=f"../cards/p{person.id}{person.first_name.lower()}.png")  # type: ignore
        for family_id in self.__families.keys():
            family = self.__families[family_id]
            dot.node(f"F{family.id}", " ", image=f"../cards/f{family.id}.png")  # type: ignore
        for person_id in self.__persons.keys():
            person = self.__persons[person_id]
            print(f"Debug => {person.id},{person.attributes}")
            for person_attributes in person.attributes:
                if person_attributes[0] == "dad" or person_attributes[0] == "mom":
                    dot.edge(f"P{person.id}{person.first_name.lower()}", f"F{person_attributes[1].id}")  # type: ignore
                elif person_attributes[0] == "child":
                    dot.edge(f"F{person_attributes[1].id}", f"P{person.id}{person.first_name.lower()}")  # type: ignore
        return self.__render_and_save_tree(dot, format, open)

    def __gen_ancestors_tree(self, person_id: int, format: graphviz_supported_format, open: bool = False):
        """
        Generate the Family Tree of the ancestor of person_id

        Args:
            person_id (int): The id of a Person
            format (Literal[&quot;png&quot;, &quot;pdf&quot;], optional): Export file type.
        """
        assert person_id in self.__persons.keys()
        self.gen_cards()
        dot = graphviz.Digraph("Tree", format=format, node_attr={"shape": "plaintext"})
        persons: list[Person] = [self.__persons[person_id]]
        while len(persons) != 0:
            for person in persons:
                dot.node(f"P{person.id}{person.first_name.lower()}", " ", image=f"../cards/p{person.id}{person.first_name.lower()}.png")  # type: ignore
            new_list_person: list[Person] = []
            print(f"Debug => {persons}")
            for person in persons:
                # print(f"Debug => {person.id},{person.attributes}")
                for attribute in person.attributes:
                    if attribute[0] == "child":
                        new_list_person.append(self.__persons[attribute[1].dad.id])
                        new_list_person.append(self.__persons[attribute[1].mom.id])
                        dot.node(f"F{attribute[1].id}", " ", image=f"../cards/f{attribute[1].id}.png")  # type: ignore
                        dot.edge(f"F{attribute[1].id}", f"P{person.id}{person.first_name.lower()}")  # type: ignore
                        dot.edge(f"P{attribute[1].dad.id}{attribute[1].dad.first_name.lower()}", f"F{attribute[1].id}")  # type: ignore
                        dot.edge(f"P{attribute[1].mom.id}{attribute[1].mom.first_name.lower()}", f"F{attribute[1].id}")  # type: ignore
            persons = new_list_person
        return self.__render_and_save_tree(dot, format, open)

    def __gen_descendants_tree(self, person_id: int, format: graphviz_supported_format, open: bool = False):
        assert person_id in self.__persons.keys()
        self.gen_cards()
        dot = graphviz.Digraph("Tree", format=format, node_attr={"shape": "plaintext"})
        persons: list[Person] = [self.__persons[person_id]]
        while len(persons) != 0:
            for person in persons:
                dot.node(f"P{person.id}{person.first_name.lower()}", " ", image=f"../cards/p{person.id}{person.first_name.lower()}.png")  # type: ignore
            new_person_list: list[Person] = []
            print(f"Debug => {self.__print_person_list(persons)}")
            for person in persons:
                for attribute in person.attributes:
                    if attribute[0] in ["dad", "mom"]:
                        dot.node(f"F{attribute[1].id}", " ", image=f"../cards/f{attribute[1].id}.png")  # type: ignore
                        dot.edge(f"P{person.id}{person.first_name.lower()}", f"F{attribute[1].id}")  # type: ignore
                        for child in attribute[1].childs:
                            new_person_list.append(self.__persons[child.id])
                            dot.edge(f"F{attribute[1].id}", f"P{child.id}{child.first_name.lower()}")  # type: ignore
            persons = new_person_list
        return self.__render_and_save_tree(dot, format, open)

    def __print_person_list(self, list_persons: list[Person]):
        newlist: list[str] = []
        for person in list_persons:
            newlist.append(str(person))
        return newlist

    def __render_and_save_tree(self, dot: graphviz.Digraph, format: graphviz_supported_format, open: bool = False):
        """
        Save a Tree

        Args:
            dot (graphviz.Digraph): A Tree
            format (Literal[&quot;png&quot;, &quot;pdf&quot;]): Export file type
        """
        new_filename = f"./temp/trees/tree.{datetime.datetime.now().isoformat('-').split('.')[0].replace(':', '-')}.gv"
        dot.render(new_filename, view=open)  # type: ignore
        return f"{new_filename}.{format}"
