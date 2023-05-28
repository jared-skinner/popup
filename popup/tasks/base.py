import logging
from pathlib import Path
from shutil import which
import subprocess as sp
from sys import platform, stdout
from typing import Optional

from popup.core.consts import (
    STATE_NOT_RUN,
    STATE_SUCCESS,
    STATE_FAILURE,
    STATE_IGNORED,
)
from popup.core.errors import (
    CircularReferenceError,
    DuplicateTaskName,
)
from popup.core.utility import (
    singleton,
    TaskCache,
    Working,
)

logging.basicConfig(level=logging.INFO)

class BaseTask():
    def __init__(self, name = "", deps = []) -> None:
        logging.debug(f"Initializing deps: {deps}")
        for dep in deps:
            self.validate_dep(dep)

        self.deps = deps

        self.name = name
        self.state = STATE_NOT_RUN
        self.working = Working()

        self.cache = True

        self.task_cache = self.working.task_cache
        self.task_cache.register(name)

    def validate_dep(self, task) -> None:
        """
        Look for circular dependencies
        """
        logging.debug(f"validating task {task.name}")
        dep_stack = [task]
        while dep_stack:
            dep = dep_stack.pop()

            dep_stack += dep.deps

            if dep == self:
                CircularReferenceError(f"Task {self.name} can not be a dependency of itself!")

    def add_dep(self, task) -> None:
        """
        Add dependency
        """
        self.validate_dep(task)
        self.deps.append(task)

    def run_deps(self) -> None:
        for dep in self.deps:
            if dep.state == STATE_NOT_RUN:
                dep.run()

        return True

    def are_deps_success(self) -> bool:
        for dep in self.deps:
            if dep.state in (STATE_FAILURE, STATE_NOT_RUN):
                return False

        return True

    def run(self) -> None:
        cached_state = self.task_cache.get_state(self.name)
        if cached_state in (STATE_IGNORED, STATE_SUCCESS):
            self.state = cached_state
            return

        self.run_deps()

        if self.are_deps_success():
            self.do_execute()

        self.do_cleanup()

    def do_execute(self):
        """
        Not implemented here.  This is the place to put anything the subclassed task needs to do
        """
        pass

    def do_cleanup(self):
        """
        Not implemented here.  This is the place to put anything cleanup.  This will be called at
        the end of run method and only if do_execute was called
        """
        pass
