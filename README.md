# Popup

Setup your dev environment in a snap!

![popup image](popup.png)

## Introduction

Popup is a tool for making a fresh OS installation your own.  It takes care of installing and configuring all the packages you need to use.  It handles dependencies, tracking failures, and idempotency.  The tool was inspired by *Ansible* and *Airflow*.

### Why a New Tool?

I know... there are tools out there already for standing up a new environment: `Ansible`, `Chef`, etc.  I wanted something that was dead-simple to use out of the box but supported some of the fancier features typically found in some of the other solutions.

### Features

* Support arbitrary actions (like running bash commands).
* Expressive syntax
* Supported dependencies between tasks
* Track the status of individual tasks run-over-run.
* Task idempotency: If a task completed successfully, on a popup rerun, skip that task.

## Installation

TODO
`pip install popup_dev`

## Usage

Create a popup file (we will call ours `example.pu`):

```
dot_files = Git("https://github.com/jared-skinner/terraform")

main_task = Main(name = "test", deps = [
    Package("zsh"),
    Package("fzf"),
    Package("htop"),
    Package("bat"),
    Package("ag"),
    Package("ripgrep"),
    Package("neovim"),
    Package("npm", deps = [dot_files]),
    Copy(src="x", dest="y")
])

main_task.run()

```

Run popup

```
popup example.pu
```


## Tasks Types
Popup supports a handful of tasks:

*Git* - Clone a repository

*Bash* - Run an arbitrary bash command

*Package* - Install a package.  Popup will infer your distribution and use the appropriate package manager.
* `apt-get` for linux
* `brew` for osx

*Copy* - Copy a file or folder from `src` to `dest`

*Group* - A shell for organizing other tasks.

*Main* - Each popup file is required to have one and only on main task.  This is the task used for orchestrating the rest!


## Custom Task Types

If you would like to implement your own task types, you can!

```
from popup.tasks.base import Base

class CustomTask(Base):
    def __ini__(self, your, arguments, **kwargs):
      # your initialization stuff goes here
      super(CustomTask, self).__init__(name=f"main_{name}", **kwargs)

    def do_execute(self):
      # how yoru task works
```
