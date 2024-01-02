import json, os

default_cfg = {
    "lang": "en",
    "preview": {
        "window_size": (1166, 648),
    },
}


class Config:
    def __init__(self) -> None:
        if not os.path.exists("./config.json"):
            with open("./config.json", "w") as f:
                f.write("{}")
                f.close
        with open("./config.json", "r") as f:
            self.cfg = json.load(f)

        self.cfg = default_cfg | self.cfg
        self.save()

        pass

    def save(self):
        with open("./config.json", "w") as f:
            json.dump(self.cfg, f, indent=4)

    def get(self, path: list[str]):
        p = path
        result = self.cfg
        while len(p) != 0:
            result = result[p[0]]
            p.pop(0)
        return result


class Language:
    def __init__(self, lang: str) -> None:
        self.lang_name_list = os.listdir("./languages")

        for i in range(len(self.lang_name_list)):
            self.lang_name_list[i] = self.lang_name_list[i].split(".")[0]  # type: ignore
        self.lang_selected = lang if lang in self.lang_name_list else self.lang_name_list[0]
        self.lang_list = {}
        for lang in self.lang_name_list:
            with open(f"./languages/{lang}.json", "r", encoding="utf8") as f:
                self.lang_list[lang] = json.load(f)  # type: ignore
                f.close()
        print(f"[Lang] Loaded lang {self.lang_selected} and loaded langs {self.lang_name_list}")
        pass

    def get(self, item: list[str], alt_lang: str = "") -> str:
        item_lst = item
        if alt_lang == "":
            result = self.lang_list[self.lang_selected]  # type: ignore
            can_retry = True
        else:
            result = self.lang_list[alt_lang]  # type: ignore
            can_retry = False
        for item in item_lst:  # type: ignore
            try:
                result = result[item]  # type: ignore
            except KeyError:
                if can_retry:
                    return self.get(item, "en")
                else:
                    print(f"[Lang] Missing language translation in {item_lst}")
                    return ""
        return result  # type: ignore

    def reload(self):
        self.lang_list = {}
        for lang in self.lang_name_list:
            with open(f"./languages/{lang}.json", "r", encoding="utf8") as f:
                self.lang_list[lang] = json.load(f)  # type: ignore
                f.close()
        print(f"[Lang] Reloaded successfully")
