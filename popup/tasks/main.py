import logging

from popup.core.consts import (
    STATE_NOT_RUN,
    STATE_SUCCESS,
    STATE_FAILURE,
    STATE_IGNORED,
)
from popup.tasks.base import BaseTask

logging.basicConfig(level=logging.DEBUG)

class Main(BaseTask):
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
