# Popup

Setup your dev environment in a snap!

![popup image](popup.png)

## Introduction

Popup is a tool for making a fresh OS installation your own.  It takes care of installing and configuring all the packages you need to use.  It handles dependencies, tracking failures, and idempotency.  The tool was inspired by *Ansible* and *Apache Airflow*.

### Why a New Tool?

I know... there are tools out there already for standing up a new environment: `Ansible`, `Chef`, etc.  I wanted something that was dead-simple to use out of the box but supported some of the fancier features typically found in some of the other solutions.

### Features

* Support arbitrary actions (like running bash commands).
* Expressive syntax
* Supported dependencies between tasks
* Track the status of individual tasks run-over-run.
* Task idempotency: If a task completed successfully, on a popup rerun, skip that task.

## Installation

TODO: Register in pypi

`pip install popup_dev`

## Usage

### Create a popup file
we will call ours `example.pu`:

```py
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

This file defined several different *tasks* and composes the tasks.  In our example we are using the following types of tasks: *Git*, *Package*, *Copy*, *Main*.  Each task defines a unit of work to be done.  Here we are installing some packages, cloning a git repository, and copying a file.

*NOTE:* Each popup file must contain a  Main task.  This task is responsible to orchestrating the rest.

*NOTE:* popup files are actually python files.  Feel free to do fancier stuff :).


### Run popup

```sh
> popup example.pu

INFO:root:not run tasks:   ['git_https://github.com/jared-skinner/terraform', '']
INFO:root:ignored tasks:   []
INFO:root:failed tasks:    ['copy_x_y']
INFO:root:succeeded tasks: ['package_npm', 'package_neovim', 'package_ripgrep', 'package_ag', 'package_bat', 'package_htop', 'package_fzf', 'package_zsh']
```

## Pulling from a URL

Popup also supports pulling a popup file from a URL.  This makes it easy to include a popup file in your dot files repo.


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

If you would like to implement your own task types, you can!  Create your custom tasks as follows:

```py
from popup.tasks.base import Base

class CustomTask(Base):
    def __init__(self, your, arguments, **kwargs):
      # your initialization stuff goes here
      super(CustomTask, self).__init__(name=f"main_{name}", **kwargs)

    def do_execute(self):
      # how your task works
```

The import your custom task in your `pu` file:

```pypi
from custom import CustomTask

# use custom task here
```
