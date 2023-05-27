from shutil import which
from typing import Optional

STATE_NOT_RUN = 0
STATE_SUCCESS = 1
STATE_FAILURE = 2
STATE_IGNORED = 3

@singleton
class WorkDir():
    """
    Class for managing a temporary working directory

    This provides a shared context for all tasks
    """
    def __init__():
        # TODO: create temp directory
        self.tempdir = ""
        pass

    def cleanup():
        # TODO: 
        pass

class Task():
    def __init__(self, name = "", deps = []) -> None:
        for dep in deps:
            self.validate_dep(dep)

        self.deps = deps

        self.name = name
        self.state = STATE_NOT_RUN

    def validate_dep(self, task) -> None:
        """
        Look for circular dependencies
        """
        dep_stack = [task]
        while dep_stack:
            dep = dep_stack.pop()

            dep.stack += dep.deps

            if dep == self:
                # TODO: don't use Exception... use something more descriptive
                Exception(f"Circular reference found!  Task {self.name} can not be a dependency of itself!")

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
        self.run_deps()

        if self.are_deps_success():
            self.do_execute()

    def do_execute(self):
        pass

class Apt(Task):
    def __init__(self, package: str, version: Optional[str] = None, **kwargs) -> None:
        # TODO: subclass the bash task
        self.package = package
        self.version = version
        super(Apt, self).__init__(**kwargs)

    def do_execute(self) -> None:
        if which(self.package) is None:
            self.state = STATE_IGNORED
            return

        try:
            # TODO: check return code
            s = subprocess.Popen(f"sudo apt install {self.package} -y")
            s.wait()
        except:
            self.state = STATE_FAILURE

        self.state = STATE_SUCCESS

class Bash(Task):
    def __init__(self, command: str, sudo: bool = False, **kwargs) -> None:
        self.command = command
        self.sudo = sudo
        super(Apt, self).__init__(**kwargs)

    def do_execute(self) -> None:
        # TODO: how do we ensure idempotency here?
        try:
            # TODO: check return code
            s = subprocess.Popen(command)
            s.wait()
        except:
            self.state = STATE_FAILURE

        self.state = STATE_SUCCESS

class AppImage(Task):
    def __init__(self, **kwargs):
        super(Apt, self).__init__(**kwargs)

    def do_execute(self):
        # TODO: how does this work?
        pass

class Git(Task):
    def __init__(self, url, dest : str = "", **kwargs):
        # where the git clone is placed

        if target == "":
            pass
            # create a temporary folder
        else:
            self.target = target

        self.url = url
        super(Apt, self).__init__(**kwargs)

    def do_execute(self) -> None:
        # create a temp dir to execute in

        # how do we ensure idempotency?
 
        # TODO: make sure we have access to git

        # TODO: make sure the url is valid and we can access it

        # clone!
        subprocess.Popen(f"git clone {url}")

class Group(Task):
    """
    A task that does nothing just for organizing other tasks
    """
    def __init__(self, **kwargs):
        super(Apt, self).__init__(**kwargs)

class Copy(Task):
    def __init__(self, src: str, dst: str, overwrite: bool = False, **kwargs) -> None:
        self.src = src
        self.dst = dst
        super(Apt, self).__init__(**kwargs)

    def do_execute(self):
        # TODO: does src exist?

        # TODO: does dest exist?

        # TODO: permissions

        # TODO: how do we handle folders vs files?

        p = subprocess.Popen(f"cp -r {self.src} {self.dest}")
        p.wait()

class Main(Task):
    def __init__(self):
        pass

    def print_graph(self) -> None:
        """
        Perform a DFS to build out the dependency graph
        """
        pass

    def do_execute(self):
        failed_tasks = []
        succeeded_tasks = []
        not_run_tasks  = []
        ignored_tasks = []

        dep_stack = []
        for dep in self.deps:
            dep_state.append(dep)

        while dep_stack:
            task = dep_stack.pop()

            if task.state == STATE_SUCCESS:
                succeeded_tasks.append(task)
            elif task_state == STATE_FAILURE:
                failed_tasks.append(task)
            elif task_state == STATE_NOT_RUN:
                not_run_tasks.append(task)
            elif task_state == STATE_IGNORED:
                ignored_tasks.append(task)

            for dep in task.deps:
                if dep in failed_tasks + succeeded_tasks + not_run_tasks + ignored_tasks:
                    continue

                dep_stack.append(dep)

        print(f"not run tasks:   {str(not_run_tasks)}")
        print(f"ignored tasks:   {str(ignored_tasks)}")
        print(f"failed tasks:    {str(failed_tasks)}")
        print(f"succeeded tasks: {str(succeeded_tasks)}")

    def do_cleanup(self):
        work_dir = WorkDir()
        work_dir.cleanup()

# TODO: register things that have been run 
# Then we can use previous run information to infer what needs to be run
# Maybe with a pickle?
# Maybe with a sqlite db 
# Maybe with a json file?
# We will need to uniquly register everything that runs
