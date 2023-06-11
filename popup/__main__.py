import argparse

import requests
import validators

from popup.core.consts import *


def parse_args():
    parser = argparse.ArgumentParser(
        prog='popup',
        description='unfold a wonderful development experience',
        epilog='A program to setup your development environment'
    )

    # TODO: implement
    parser.add_argument("--force", "-f", action="store_true", help="force all tasks to rerun")

    # TODO: implement
    parser.add_argument("--clear", "-c", action="store_true", help="clear task cache")

    parser.add_argument("--graph", "-g", action="store_true", help="display a the dependency graph with status information")

    parser.add_argument("popup_path")

    return parser.parse_args()

def main():
    args = parse_args()

    if validators.url(args.popup_path):
        f = requests.get(args.popup_path)
        contents = f.text
    else:
        with open(args.popup_path, 'r') as f:
            contents = f.read()

        if args.graph:
            contents += "\nmain_task.graph()"
        else:
            contents += "\nmain_task.run()"

        exec(contents)

if __name__ == "__main__":
    main()
