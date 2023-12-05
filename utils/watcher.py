from typing import Callable


class Watcher:
    """A simple class, set to watch its variable."""

    def __init__(self, value: int | None):
        self.__variable = value
        self.__watchers: list[Callable[[], None]] = []

    def get(self):
        return self.__variable

    def set(self, new_value: int):
        if self.__variable != new_value:
            self.__variable = new_value
            self.on_change()

    def watch_changes(self, watcher: Callable[[], None]):
        self.__watchers.append(watcher)

    def __execute_watcher(self, watcher: Callable[[], None]):
        return watcher()

    def on_change(self):
        map(self.__execute_watcher, self.__watchers)
        pass  # do stuff right after variable has changed
