import os, shutil
from utils.sql import Sql


class FileLoader:
    def __init__(self) -> None:
        self.file = None
        pass

    def load(self, file_path: str):
        assert os.path.isfile(file_path)
        shutil.copy2(file_path, "./temp/file/file.hgb")
        return self.__unbundle_file()

    def __unbundle_file(self):
        shutil.rmtree("./temp/file/cache")
        shutil.unpack_archive("./temp/file/file.hgb", "./temp/file/cache", "zip")
        return Sql("./temp/file/cache/data.db")

    def save(self, sql_obj: Sql, file_path: str):
        assert os.path.isfile(file_path)
        self.__bundle_file(sql_obj)
        shutil.copy("./temp/file/file.hgb", file_path)

    def __bundle_file(self, sql: Sql):
        sql.close()
        shutil.make_archive("./temp/file/file", "zip", "./temp/file/cache")
        shutil.move("./temp/file/file.zip", "./temp/file/file.hgb")

    def create_new_file(self):
        if not os.path.exists("./temp/file"):
            os.mkdir("./temp/file")
        if not os.path.exists("./temp/file/cache"):
            os.mkdir("./temp/file/cache")
        return Sql("./temp/file/cache/data.db", create_from_scratch=True)
