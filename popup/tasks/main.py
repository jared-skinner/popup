from terminaltables import AsciiTable
from asciidag.graph import Graph
from asciidag.node import Node

from popup.core.consts import (
    STATE_NOT_RUN,
    STATE_SUCCESS,
    STATE_FAILURE,
    STATE_IGNORED,
)
from popup.tasks.base import BaseTask
from popup.core.utility import logger

class Main(BaseTask):
    """
    Main task file.  A popup configuration should define this once
    """
    def __init__(self, name, **kwargs):
        logger.debug(f"Initializing Main task: {name}")
        super(Main, self).__init__(name=f"main_{name}", **kwargs)

    def do_cleanup(self):
        failed_tasks = []
        succeeded_tasks = []
        not_run_tasks  = []
        ignored_tasks = []

        dep_stack = []
        for dep in self.deps:
            dep_stack.append(dep)



        status_table = [["Task Name", "Status", "Dependencies"]]

        processed_tasks = []
        while dep_stack:
            task = dep_stack.pop()

            if task in processed_tasks:
                continue
            else:
                processed_tasks.append(task)

            # record result in cache
            # we can expand this later
            if task.cache:
                task.task_cache.set(task.name, {"state": task.state})

            state = self.color_by_state(task, task.state)
            if task.state == STATE_SUCCESS:
                succeeded_tasks.append(task.name)
            elif task.state == STATE_FAILURE:
                failed_tasks.append(task.name)
            elif task.state == STATE_NOT_RUN:
                not_run_tasks.append(task.name)
            elif task.state == STATE_IGNORED:
                ignored_tasks.append(task.name)

            status_table.append([task.name, state, " ".join([self.color_by_state(x, x.name) for x in task.deps])])

            for dep in task.deps:
                if dep in failed_tasks + succeeded_tasks + not_run_tasks + ignored_tasks:
                    continue

                dep_stack.append(dep)

        logger.info(f"\n{AsciiTable(status_table).table}")

        self.task_cache.persist()
        self.working.cleanup()

    def graph(self):
        graph = Graph()

        nodes = self.get_graph_node()
        graph.show_nodes([nodes])
