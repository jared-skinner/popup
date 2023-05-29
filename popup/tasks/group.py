import logging

from popup.tasks.base import BaseTask

logging.basicConfig(level=logging.DEBUG)

class Group(BaseTask):
    """
    A task that does nothing just for organizing other tasks
    """
    def __init__(self, name: str, **kwargs) -> None:
        logging.debug(f"Initializing group: {name}")
        super(Group, self).__init__(name=name, **kwargs)

    def do_execute(self) -> None:
        """
        This just houses tasks which are run as part of run_deps in the parent class: Task
        """
        pass

