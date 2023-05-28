# Popup

Setup your dev environment in a snap!

![popup image](popup.png)

## Introduction

Popup is a tool for configuring a new os instalation to be your own!  This tool is similar to *Ansible* or *Chef* but is much simpler.  

### Why a New Tool?

I wanted something that was easier to use out of the box than Ansible and had features that were difficult to build into a shell script.  In particular I wanted a tool that could:

* Support arbitrary actions (like running bash commands)
* Was expressible
* Supported dependencies
* Tracked task-level status run over run
* Would skip steps that had previously completed successfully

The last requirement promotes idempotency.


## Installation

`pip install popup_dev`

## Usage

Create a popup file:

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

### Supported Task Types

* Git
* Bash
* Package
* Copy
* Group
