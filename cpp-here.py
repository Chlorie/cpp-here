from typing import Dict, Optional
import stringcase as sc
from enum import IntEnum
import os
import subprocess as sp
import datetime
import shutil as sh
from pathlib import Path
import prompt
import json


def main():
    init = Initializer()
    init.run()


class ProjectType(IntEnum):
    APP = 0
    HEADERS = 1
    LIBRARY = 2


class Initializer:
    def __init__(self):
        self._cd = Path(os.getcwd())
        self._res_dir = Path(os.path.realpath(__file__)).parent / "res"
        self._name = sc.spinalcase(self._cd.stem)
        self._app_type = ProjectType.APP
        self._vars: Dict[str, str] = {}

    def run(self):
        self._check_cd()
        self._project_settings()
        self._universal_res()
        self._setup_vcpkg()
        if self._project_type == ProjectType.APP:
            self._initialize_app()
        else:
            self._initialize_lib()
            self._add_docs()
        self._add_readme()
        self._git()
        self._success("Finished project initialization")

    def _success(self, message: str):
        print("✓ " + message)

    def _error(self, message: str):
        print("✗ " + message)
        exit(1)

    def _system(self, command: str, *args: str, hint: Optional[str] = None):
        code = sp.call([command, *args], stdout=sp.DEVNULL, stderr=sp.DEVNULL)
        if code == 0:
            return
        message = f"[{command}] exited with code {code}"
        if hint is not None:
            message += f", {hint}"
        self._error(message)

    def _copy_res(self,
                  res_path: str,
                  tgt_path: Optional[str] = None,
                  config_vars: bool = False):
        if tgt_path is None:
            tgt_path = res_path
        tgt = self._cd / tgt_path
        res = self._res_dir / res_path
        if res.is_dir():
            sh.copytree(res, tgt)
        elif config_vars:
            text = res.read_text()
            for var, val in self._vars.items():
                text = text.replace(var, val)
            tgt.write_text(text)
        else:
            sh.copy(res, tgt)

    def _check_cd(self):
        if next(self._cd.iterdir(), None) is not None:
            self._error("The current directory is not empty")

    def _project_settings(self):
        self._name = prompt.input("Project name", self._name)
        self._vars["%project_name%"] = self._name
        self._vars["%upper_project_name%"] = sc.constcase(self._name)
        self._vars["%version%"] = prompt.input("Package", "0.1.0")
        self._project_type = ProjectType(prompt.choices(
            "What type of project?",
            "Application",
            "Header-only library",
            "Static/Shared library"))

    def _universal_res(self):
        (self._cd / "cmake").mkdir()
        self._copy_res(".editorconfig")
        self._copy_res(".gitignore")
        self._copy_res(".clang-format")
        self._copy_res("CMakePresets.json", config_vars=True)
        self._copy_res("cmake/ProjectSettings.cmake")

    def _setup_vcpkg(self):
        vcpkg = prompt.choices(
            "Set up vcpkg settings?",
            "Yes", "Yes, and also add vcpkg-configuration.json", "No")

        if vcpkg == 1:
            (self._cd / "vcpkg-configuration.json").write_text(json.dumps({
                "$schema": "https://raw.githubusercontent.com/microsoft/vcpkg-tool/main/docs/vcpkg-configuration.schema.json",
                "registries": [],
                "default-registry": {
                    "kind": "git",
                    "repository": "https://github.com/microsoft/vcpkg",
                    "baseline": "9c7c66471005cb132832786d5d65d83d2cf503ad"
                }
            }, indent=4))
        if vcpkg != 2:
            vcpkg_name = prompt.input(
                "vcpkg package name", sc.spinalcase(self._name))
            (self._cd / "vcpkg.json").write_text(json.dumps({
                "$schema": "https://raw.githubusercontent.com/microsoft/vcpkg-tool/main/docs/vcpkg.schema.json",
                "name": vcpkg_name,
                "version-string": self._vars["%version%"],
                "dependencies": []
            }, indent=4))
            vcpkg_args = ["x-update-baseline"]
            if vcpkg == 0:
                vcpkg_args.append("--add-initial-baseline")
            self._system("vcpkg", *vcpkg_args)

    def _initialize_app(self):
        self._copy_res("CMakeLists.txt", config_vars=True)
        (self._cd / "src").mkdir()
        self._copy_res("src/CMakeLists.txt", config_vars=True)
        self._copy_res("src/main.cpp")
        self._success("Created CMake project for the app")

    def _initialize_lib(self):
        self._copy_res("CMakeListsLibrary.txt",
                       "CMakeLists.txt", config_vars=True)
        (self._cd / "examples").mkdir()
        self._copy_res("examples/CMakeLists.txt", config_vars=True)
        self._copy_res("examples/playground.cpp")
        self._success("Created CMake directory for examples")
        include_dir = prompt.input(
            "Include directory name", sc.snakecase(self._name))
        self._vars["%include_dir%"] = include_dir
        include_dir = "lib/include/" + include_dir
        (self._cd / include_dir).mkdir(parents=True)
        if self._project_type == ProjectType.HEADERS:
            self._copy_res("lib/CMakeListsHeaderOnly.txt",
                           "lib/CMakeLists.txt", config_vars=True)
        else:
            self._vars["%macro_namespace%"] = prompt.input(
                "Preprocessor macro namespace", sc.constcase(self._name))
            self._copy_res("lib/include/dir/export.h",
                           include_dir + "/export.h", config_vars=True)
            self._copy_res("lib/CMakeLists.txt", config_vars=True)
            (self._cd / "lib/src").mkdir(parents=True)
            self._copy_res("lib/src/dummy.cpp")
        self._copy_res("cmake/libConfig.cmake.in",
                       f"cmake/{self._name}Config.cmake.in", config_vars=True)
        self._success("Created CMake project for the library")

    def _add_docs(self):
        if not prompt.confirm("Add Doxygen & Sphinx based docs support?"):
            return
        self._copy_res("cmake/FindSphinx.cmake")
        with (self._cd / "CMakeLists.txt").open("a") as file:
            prefix = f'{self._vars["%upper_project_name%"]}_'
            file.write(
                '\n'
                f'option({prefix}BUILD_DOCS "Build documentation using Doxygen & Sphinx" OFF)\n'
                f'if ({prefix}BUILD_DOCS)\n'
                '    add_subdirectory(docs)\n'
                'endif ()\n')
        (self._cd / "docs/custom").mkdir(parents=True)
        self._copy_res("docs/custom/custom.css")
        self._vars["%project_title%"] = prompt.input(
            "Project title", sc.titlecase(self._name))
        author = prompt.input("Author of the library/documentation")
        self._vars["%author%"] = author
        doc_copyright_def = f"{datetime.datetime.now().year}, {author}"
        self._vars["%doc_copyright%"] = prompt.input(
            "Docs copyright", doc_copyright_def)
        self._vars["%cpp_namespace%"] = prompt.input(
            "C++ namespace of the project", sc.snakecase(self._name))
        self._copy_res("docs/CMakeLists.txt", config_vars=True)
        self._copy_res("docs/conf.py", config_vars=True)
        self._copy_res("docs/Doxyfile.in", config_vars=True)
        self._copy_res("docs/index.rst", config_vars=True)
        self._copy_res("docs/requirements.txt")

    def _add_readme(self):
        if not prompt.confirm("Add a readme file?"):
            return
        if "%project_title%" in self._vars:
            title = self._vars["%project_title%"]
        else:
            title = prompt.input("Project title", sc.titlecase(self._name))
            self._vars["%project_title%"] = title
        (self._cd / "README.md").write_text(f"# {title}\n")

    def _git(self):
        git_sel = prompt.choices(
            "Set up git repo?",
            "Initialize and make an initial commit",
            "Just initialize",
            "Skip")
        if git_sel == 2:
            return
        self._system("git", "init",
                     hint="make sure you have git properly installed")
        if git_sel == 1:
            return
        self._system("git", "add", "-A")
        self._system("git", "commit", "-m", "Initialized project")


if __name__ == "__main__":
    main()
