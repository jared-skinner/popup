from popup.core.consts import (
    STATE_NOT_RUN,
    STATE_SUCCESS,
    STATE_FAILURE,
    STATE_IGNORED,
)
from popup.tasks.base import BaseTask
from popup.core.utility import logger

class Group(BaseTask):
    """
    A task that does nothing just for organizing other tasks
    """
    def __init__(self, name: str, **kwargs) -> None:
        logger.debug(f"Initializing group: {name}")
        super(Group, self).__init__(name=name, **kwargs)

    def do_execute(self) -> None:
        """
        This just houses tasks which are run as part of run_deps in the parent class: Task
        """

        self.state = STATE_SUCCESS

