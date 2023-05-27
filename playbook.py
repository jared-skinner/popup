import argparse

from popup import Apt, Bash, AppImage, Git, Main, Group

git = Apt("git")
git_group = Group("git", deps=[Bash("setup username", deps=[git]), Bash("setup email", deps=[git])])

dot_files = Git("github.com/jared-skinner/terraform")
df_path = dot_files.target

zsh = Apt("zsh")

# setup neovim
#
#   - install neovim
#   - installnvim dot files 
#   - install python extensions
#   - install lanugage servers
nvim = Apt("neovim")
nvim_group = Group("neovim", deps=[fzf, nvim, dot_files])
# TODO: Install and update plugins through a task

copy_package_dots = Group(deps = [
    Copy(
        src=os.path.join(df_path, "nvim"),
        dest=os.path.join("~", ".config", "nvim"),
        deps=[get_dot_files, nvim]
    ),
    Copy(
        src=os.path.join(df_path, "tumx"),
        dest=os.path.join("~", ".tmux"),
        deps=[get_dot_files, Apt("tumx")]
    ),
    Copy(
        src=os.path.join(df_path, "zsh"),
        dest=os.path.join("~", ".zsh"),
        deps=[get_dot_files, Apt("zsh")]
    )
])

cmd = Group(deps = [
    copy_package_dots,
    nvim_group,
    fzf,
    git_group,
    zsh,
    Apt("htop"),
    Apt("ripgrep"),
])

kids = Group(deps = [
    Apt("scratch")
])

coding = Group(deps = [
    Apt("docker"),
    Apt("npm"),
    Apt("rust"),
    Apt("go"),
    Apt("gcc"),
    Apt("cgit"),
])

graphics = Group(deps = [
    Apt("krita"),
    Apt("gimp"),
    Apt("inkscape"),
    Apt("mypaint"),
    Apt("blender"),
])

math = Group(deps = [
    Apt("xaos"),
    Apt("gmp"),
])

browsing = Group(deps = [
    Apt("brave"),
    Apt("deluge"),
    Apt("clamav"), # open source  virus protection
    # TODO: firewall
    # TODO: password manager
])

audio = Group(deps = [
    Apt("audacity"),
    Apt("reaper"),
])

video = Group(deps = [
    Apt("vlc"),
])

gaming = Group(deps = [
    Apt("steam"),
    #TODO: emulators and roms
])

utilities = Group(deps = [
    Apt("alacrity")
])

office = Group(deps = [
    Apt("anki"),
    # TODO: LaTeX
    # TODO: Task warrior?
])

def parse_args():
    parser = argparse.parser()
    args = Null
    return args

def main():
    args = parse_args()

    tasks = [cmd]

    if args.personal:
        tasks += [audio, coding]

    if args.gui:
        tasks += [utilities]

    if args.personal and args.gui:
        tasks += [video, gaming, math, kids, browsing, office]

    if args.rpi:
        tasks += [alacrity]

    main_task = Main(deps=tasks)
    main_task.run()

if name == "__main__":
    main()
