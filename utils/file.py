import shutil, os


class FileInDb:
    def __init__(self, id: int, name: str, idPerson: int) -> None:
        self.id = id
        self.name = name
        self.idPerson = idPerson
        pass


def create_file_template(filepath: str, person_id: int):
    new_filepath = f"./temp/file/cache/add_files/{filepath.split('/')[-1]}"
    if os.path.exists(new_filepath):
        return
    shutil.copy2(filepath, new_filepath)
    return FileInDb(0, new_filepath.split("/")[-1], person_id)


def remove_file(file: FileInDb):
    path = f"./temp/file/cache/add_files/{file.name}"
    if os.path.exists(path):
        os.remove(path)
    return
