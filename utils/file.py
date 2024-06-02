import os
import shutil
from utils.sql import Sql


class FileInDb:
    def __init__(self, id: int, name: str, idPerson: int) -> None:
        self.id = id
        self.name = name
        self.idPerson = idPerson
        pass


def createFile(sql: Sql, path: str, idPerson: int):
    next_id = max(sql.get_all_files()) + 1
    if not os.path.exists("./temp/file/cache/add_files"):
        os.mkdir("./temp/file/cache")
    save_path = f"./temp/file/cache/add_files/{path.split('/')[-1]}"
    if os.path.exists(save_path):
        return
    shutil.copy(path, save_path)
    f = FileInDb(next_id, path.split("/")[-1], idPerson)
    return sql.create_new_file(f)
