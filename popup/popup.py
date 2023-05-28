import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        prog='popup',
        description='unfold a wonderful development experience',
        epilog='A program to setup your development environment'
    )

    parser.add_argument("--force", "-f", action="store_true", help="force all tasks to rerun")

    parser.add_argument("popup_file")

    return parser.parse_args()

def main():
    args = parse_args()

    with open(args.popup_file, 'r') as f:
        contents = f.read()

        contents = "from tasks import Package, Bash, Git, Main, Group, Copy\n" + contents
        exec(contents)

if __name__ == "__main__":
    main()
