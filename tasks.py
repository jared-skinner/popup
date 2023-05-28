import logging
from pathlib import Path
from shutil import which
import subprocess as sp
from sys import platform, stdout
from typing import Optional

from consts import (
    STATE_NOT_RUN,
    STATE_SUCCESS,
    STATE_FAILURE,
    STATE_IGNORED,
)
from errors import (
    CircularReferenceError,
    DuplicateTaskName,
)
from utility import (
    singleton,
    TaskCache,
    Working,
)

logging.basicConfig(level=logging.DEBUG)

class Task():
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

class Cmd(Task):
    def __init__(self, comand: str, sudo: bool = False, **kwargs) -> None:
        self.comand = comand
        self.sudo = sudo
        super(Bash, self).__init__(**kwargs)

    def do_execute(self) -> None:
        try:
            process = sp.run(comand.split())
            returncode = process.returncode

            if returncode == 0:
                self.state = STATE_SUCCESS
                return
            else:
                self.state = STATE_FAILURE
                return

        except:
            self.state = STATE_FAILURE
            return

        self.state = STATE_SUCCESS

class Bash(Task):
    def __init__(self, comand: str, sudo: bool = False, **kwargs) -> None:
        self.comand = comand
        self.sudo = sudo
        super(Bash, self).__init__(**kwargs)

    def do_execute(self) -> None:
        try:
            logging.debug(f"running bash comand: {self.comand}")
            process = sp.run(self.comand.split(), stdout=sp.DEVNULL, stderr=sp.STDOUT)
            logging.debug(f"bash comand finished: {self.comand}")
            returncode = process.returncode

            if returncode == 0:
                logging.debug(f"bash comand succeeded: {self.comand}")
                self.state = STATE_SUCCESS
                return
            else:
                logging.debug(f"bash comand failed: {self.comand}")
                self.state = STATE_FAILURE
                return
        except:
            self.state = STATE_FAILURE
            logging.info(f"Failed to run comand {self.comand}")
            return

        self.state = STATE_SUCCESS

class Package(Bash):
    def __init__(self, package: str, version: Optional[str] = None, **kwargs) -> None:
        self.package = package
        self.version = version

        if platform in ("linux", "linux2"):
            if self.version:
                comand = f"sudo apt install {self.package}={self.version} -y"
            else:
                comand = f"sudo apt install {self.package} -y"
        else:
            if self.version:
                comand = f"brew install {self.package}@{self.version}"
            else:
                comand = f"brew install {self.package}"

        super(Package, self).__init__(comand=comand, name=f"package_{package}", **kwargs)

class Git(Bash):
    def __init__(self, url: str, **kwargs) -> None:
        self.url = url
        self.working = Working()


        comand = f"git clone {self.url} {self.working.get_dir()}"
        super(Git, self).__init__(comand=comand, name=f"git_{self.url}", **kwargs)

        self.cache = False

    def do_execute(self) -> None:
        if not which("git"):
            logging.warning("Could not find git!")
            self.state = STATE_FAILURE

        process = sp.run(f"git ls-remote {self.url}".split())
        returncode = process.returncode

        if returncode != 0:
            logging.info(f"{self.url} is not a valid git repo!")

        super(Git, self).do_execute()

class Copy(Bash):
    def __init__(self, src: str, dest: str, overwrite: bool = False, **kwargs) -> None:
        self.src = src
        self.dest = dest

        comand = f"cp -r {self.src} {self.dest}"

        super(Copy, self).__init__(comand=comand, name=f"copy_{self.src}_{self.dest}", **kwargs)

    def do_execute(self):
        if not Path(self.src):
            logging.warning(f"{self.src} is not a valid source")
            self.state = STATE_FAILURE
            return

        if Path(self.dest).exists():
            logging.warning(f"{self.dest} already exists")
            self.state = STATE_FAILURE
            return

        super(Copy, self).do_execute()

class Group(Task):
    """
    A task that does nothing just for organizing other tasks
    """
    def __init__(self, name: str, **kwargs) -> None:
        logging.debug(f"Initializing group: {name}")
        super(Group, self).__init__(**kwargs)

    def do_execute(self) -> None:
        """
        This just houses tasks which are run as part of run_deps in the parent class: Task
        """
        pass

class Main(Task):
    def __init__(self, name, **kwargs):
        logging.debug(f"Initializing Main task: {name}")
        super(Main, self).__init__(name=f"main_{name}", **kwargs)

    def do_cleanup(self):
        failed_tasks = []
        succeeded_tasks = []
        not_run_tasks  = []
        ignored_tasks = []

        dep_stack = []
        for dep in self.deps:
            dep_stack.append(dep)

        while dep_stack:
            task = dep_stack.pop()

            if task.state == STATE_SUCCESS:
                succeeded_tasks.append(task.name)
            elif task.state == STATE_FAILURE:
                failed_tasks.append(task.name)
            elif task.state == STATE_NOT_RUN:
                not_run_tasks.append(task.name)
            elif task.state == STATE_IGNORED:
                ignored_tasks.append(task.name)

            # record result in cache
            # we can expand this later
            if task.cache:
                task.task_cache.set(task.name, {"state": task.state})

            for dep in task.deps:
                if dep in failed_tasks + succeeded_tasks + not_run_tasks + ignored_tasks:
                    continue

                dep_stack.append(dep)

        logging.info(f"not run tasks:   {str(not_run_tasks)}")
        logging.info(f"ignored tasks:   {str(ignored_tasks)}")
        logging.info(f"failed tasks:    {str(failed_tasks)}")
        logging.info(f"succeeded tasks: {str(succeeded_tasks)}")

        self.task_cache.persist()
        self.working.cleanup()
