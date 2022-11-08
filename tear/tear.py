import toml
import sys
import pathlib
from .cmdparser import command_parser
from typing import Optional
import subprocess


def path_to_str(path: pathlib.Path):
    return str(path.resolve())


def new_project(path: pathlib.Path, name: str):
    (path / name).mkdir()
    new_project = path / name
    with (new_project / "tear.pyproj.toml").open("w") as file:
        toml.dump(
            {
                "project": {
                    "name": name,
                    "version": "0.0.1",
                    "description": "No description given",
                },
                "python": {"path": "{python}", "options": []},
                "module": {"name": "main", "args": []},
                "scripts": {}
            },
            file,
        )
    with (new_project / "main.py").open("w") as file:
        file.write(
            """\
import sys


def main(argv: list[str]):
    print("Hello World!")

 
if __name__ == "__main__":
    sys.exit(main(sys.argv))
"""
        )

        
def run(script: Optional[str] = None):
    with open("tear.pyproj.toml") as config:
        data = toml.load(config)

    scripts: dict = data.get("scripts")
    if not script:
        if sys.platform == "win32" or sys.platform == "win64":
            python: dict = data.get("python")
            python_path: str = python["path"].replace("{python}", "python")
            python_options: list[str] = python["options"]
            python_options.append("-m")
            module: dict = data["module"]
            module_name: str = module["name"]
            _module_argv = [arg.split() for arg in module["args"]]
            module_argv = []
            for args in _module_argv:
                for arg in args:
                    module_argv.append(arg)
            subprocess.run([python_path, *python_options, module_name, *module_argv])
        else:
            python: dict = data.get("python")
            python_path: str = python["path"].replace("{python}", "python3")
            python_options: list[str] = python["options"]
            python_options.append("-m")
            module: dict = data["module"]
            module_name: str = module["name"]
            _module_argv = [arg.split() for arg in module["args"]]
            module_argv = []
            for args in _module_argv:
                for arg in args:
                    module_argv.append(arg)
            subprocess.run([python_path, *python_options, module_name, *module_argv])
    else:
        subprocess.run(scripts.get(script).split())


def main(args: list[str] = None):
    _, *argv = args or sys.argv
    cmdparser = command_parser(*argv)
    current_path = pathlib.Path.cwd().resolve()
    if cmd := cmdparser.get(0):
        if cmd == "new":
            if project_name := cmdparser.get(1):
                new_project(current_path, project_name)
            else:
                project_name = input("Please input the project name: ")
                new_project(current_path, project_name)

        elif cmd == "run":
            run(cmdparser.get(1))
