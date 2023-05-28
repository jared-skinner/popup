from tasks import Package, Bash, Git, Main, Group, Copy

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
