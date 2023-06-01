import os
from pathlib import Path
from sys import platform 
from shutil import which
import subprocess as sp
from typing import Optional

from colorclass import Color

from popup.core.consts import (
    STATE_NOT_RUN,
    STATE_SUCCESS,
    STATE_FAILURE,
    STATE_IGNORED,
)
from popup.core.utility import Working, logger
from popup.tasks.base import BaseTask

class Bash(BaseTask):
    def __init__(self, comand: str, name = "", **kwargs) -> None:
        self.comand = comand

        if name == "":
            name = f"bash_{comand}"

        super(Bash, self).__init__(name=name, **kwargs)

    def do_execute(self) -> None:
        try:
            logger.info(Color("{autoyellow}running bash comand:   {/autoyellow}") + self.comand)
            process = sp.run(self.comand.split(), stdout=sp.DEVNULL, stderr=sp.DEVNULL)
            logger.debug(f"bash comand finished: {self.comand}")
            returncode = process.returncode

            if returncode == 0:
                logger.info(Color("{autogreen}bash comand succeeded: {/autogreen}") + self.comand)
                self.state = STATE_SUCCESS
                return
            else:
                logger.info(Color("{autored}bash comand failed:    {/autored}") + self.comand)
                self.state = STATE_FAILURE
                return
        except:
            self.state = STATE_FAILURE
            logger.info(f"Failed to run comand {self.comand}")
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
    def __init__(self, url: str, target: str, **kwargs) -> None:
        self.url = url
        self.working = Working()
        self.target = os.path.join(self.working.get_dir(), target)

        comand = f"git clone {self.url} {self.target} --quiet"
        super(Git, self).__init__(comand=comand, name=f"git_{self.url}", **kwargs)

        self.cache = False

    def do_execute(self) -> None:
        if not which("git"):
            logger.warning("Could not find git!")
            self.state = STATE_FAILURE

        process = sp.run(f"git ls-remote {self.url} --quiet".split())
        returncode = process.returncode

        if returncode != 0:
            logger.info(f"{self.url} is not a valid git repo!")

        super(Git, self).do_execute()

class Copy(Bash):
    def __init__(self, src: str, dest: str, overwrite: bool = False, **kwargs) -> None:
        self.src = src
        self.dest = dest
        self.overwrite = overwrite

        comand = f"cp -r {self.src} {self.dest}"

        super(Copy, self).__init__(comand=comand, name=f"copy_{self.dest}", **kwargs)

    def do_execute(self):
        if not Path(self.src):
            logger.warning(f"{self.src} is not a valid source")
            self.state = STATE_FAILURE
            return

        if not self.overwrite and Path(self.dest).exists():
            logger.warning(f"{self.dest} already exists")
            self.state = STATE_FAILURE
            return

        super(Copy, self).do_execute()


