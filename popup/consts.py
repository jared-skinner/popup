from enum import Enum
import os

MODULE_ROOT = os.path.abspath(os.path.dirname(__file__))

STATE_NOT_RUN = "NOT_RUN"
STATE_SUCCESS = "SUCCESS"
STATE_FAILURE = "FAILURE"
STATE_IGNORED = "IGNORED"
