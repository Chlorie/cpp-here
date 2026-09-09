# cpp-here

A [Copier](https://copier.readthedocs.io/) template for creating new CMake-based C++ projects quickly and effortlessly.
This is only meant for personal use, but feel free to take it if you need it.

This repo is the Copier-based successor of the now deprecated [cpp-init](https://github.com/Chlorie/cpp-init).

## Usage

```sh
copier copy --trust gh:Chlorie/cpp-here path/to/project
```

`--trust` is required because the template runs post-copy tasks (`git init`, `vcpkg x-update-baseline`).

To pull in later template improvements in a project that was already generated:

```sh
cd path/to/project
copier update --trust
```

## Features

- Project templates for executables, header-only libraries and compiled libraries.
- Optional vcpkg manifest mode setup.
- Project settings with warning presets for the three main C++ compilers.
- CMakePresets.json with Ninja Multi-Config out of the box.
- DLL import/export macros for shared libraries.
- Optional Catch2 unit tests (via vcpkg or FetchContent).
- Optional Breathe (Doxygen & Sphinx)-based documentation scaffold.
