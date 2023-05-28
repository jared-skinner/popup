# Popup

Setup your dev environment in a snap!

![popup image](popup.png)

## Introduction

Popup is a tool for configuring a new os instalation to be your own!  This tool is similar to *Ansible* or *Chef* but is much simpler.  

### Why a New Tool?

I wanted something that was easier to use out of the box than Ansible and had features that were difficult to build into a shell script.  In particular I wanted a tool that could:

* Support arbitrary actions (like running bash commands).
* Was expressible.
* Supported dependencies.
* Tracked task-level status run over run.
* Would skip steps that had previously completed successfully.

The last requirement promotes idempotency.


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

Run popup: `popup example.pu`


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
