import logging
from functools import wraps
import os
from tempfile import TemporaryDirectory

import pickledb

from popup.core.consts import MODULE_ROOT

logging.basicConfig(level=logging.DEBUG)

def singleton(orig_cls):
    orig_new = orig_cls.__new__
    instance = None

    @wraps(orig_cls.__new__)
    def __new__(cls, *args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = orig_new(cls, *args, **kwargs)
        return instance
    orig_cls.__new__ = __new__
    return orig_cls

@singleton
class TaskCache():
    """
    Way to persist task information across runs.  This helps us to know which tasks need to be run
    if there was a partial success in a previous run.
    """
    # list of tasks which have been regiesterd.  We do this to make sure we don't have conflicts
    registered_tasks = []
    db_path = os.path.join(MODULE_ROOT, "task_cache.db")
    db = pickledb.load(location=db_path, auto_dump=False)

    def __init__(self) -> None:
        pass

    def register(self, task_name: str) -> None:
        logging.debug(f"Registering task {task_name}")
        logging.debug(TaskCache.registered_tasks)
        if task_name in TaskCache.registered_tasks:
            raise DuplicateTaskName(f"Two packages found with the name: {task_name}!")

        TaskCache.registered_tasks.append(task_name)

    def get_state(self, task_name: str) -> dict[str, str]:
        vals = TaskCache.db.get(task_name)
        logging.debug(f"Current state for {task_name}")
        logging.debug(vals)

        if vals:
            return vals["state"]
        else:
            return False

    def set(self, task_name: str, values: dict[str, str]) -> None:
        TaskCache.db.set(task_name, values)

    def persist(self):
        TaskCache.db.dump()

    def clear(self):
        os.remove(TaskCache.db_path)

@singleton
class Working():
    """
    An instance between all of the task classes for shared files/varliables/etc
    """
    def __init__(self, retain: bool = False) -> None:
        self.retain = retain
        self.working_dir = TemporaryDirectory()
        self.task_cache = TaskCache()

    def get_dir(self):
        return self.working_dir.name

    def cleanup(self):
        if not self.retain:
            self.working_dir.cleanup()

def clear_cache():
    tc = TaskCache()
    tc.clear()
