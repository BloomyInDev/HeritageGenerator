import json, os

default_cfg = {
    "lang": "en",
}


class Config:
    def __init__(self) -> None:
        with open("./config.json", "r") as f:
            self.cfg = json.load(f)

        self.cfg = default_cfg | self.cfg
        self.save()

        pass

    def save(self):
        with open("./config.json", "w") as f:
            json.dump(self.cfg, f, indent=4)
    
    def get(self,path:list[str]):
        p = path
        result = self.cfg
        while len(p) != 0:
            result = result[p[0]]
            p.pop(0)

class Language:
    def __init__(self, lang: str) -> None:
        self.lang_name_list = os.listdir("./languages")

        for i in range(len(self.lang_name_list)):
            self.lang_name_list[i] = self.lang_name_list[i].split(".")[0]  # type: ignore
        self.lang_selected = "en" if "en" in self.lang_name_list else self.lang_name_list[0]
        self.lang_list = {}
        for lang in self.lang_name_list:
            with open(f"./languages/{lang}.json") as f:
                self.lang_list[lang] = json.load(f)  # type: ignore
        print(self.lang_name_list)
        pass

    def get(self, item: list[str]):
        item_lst = item
        thing = self.lang_list[self.lang_selected]  # type: ignore
        for item in item_lst:  # type: ignore
            thing = thing[item]  # type: ignore
