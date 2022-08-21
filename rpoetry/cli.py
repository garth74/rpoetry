#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import typing as t
from enum import Enum
from pathlib import Path

import typer

from .utils import check_installed, run_in_R, to_charcter_vector

app = typer.Typer(name="rpoetry", add_completion=False)


def abspath(path: Path):
    """Get the abosolute path."""
    if not path.is_absolute():
        return path.absolute()
    return path


@app.callback()
def main(
    check: bool = typer.Option(
        False,
        "--check",
        is_eager=True,
        help="Check whether the required R packages are installed.",
    )
):
    """rpoetry - the cli for devtools."""
    if check:
        required_packages = ["devtools", "renv", "usethis"]
        for package in required_packages:
            if not check_installed(package):
                typer.echo(f"{package} is not installed.")
                raise typer.Exit(1)


@app.command()
def new(
    path: Path = typer.Argument(..., help="The path to create the project at.")
):
    """Create a new R package."""
    posix_path = abspath(path).as_posix()
    run_in_R(f'devtools::create_package("{posix_path}")')
    run_in_R(f'renv::init("{posix_path}")')


class License(str, Enum):
    none = ""
    gpl3 = "gpl3"
    mit = "mit"


@app.command()
def add(
    packages: t.Optional[t.List[str]] = typer.Option(
        None, help="List of package names to install."
    ),
    upgrade: bool = typer.Option(False),
    license: License = typer.Option(License.none),
):
    """Add a package or packages to renv.lock."""
    if not Path.cwd().joinpath("renv.lock").exists():
        typer.echo("renv.lock file could not be found.")

    # install packages to a project
    if packages:
        if len(packages) > 1:
            charstr = to_charcter_vector(packages)
        else:
            charstr = f'"{packages[0]}"'

        if not upgrade:
            run_in_R(f"renv::install({charstr})")
        else:
            run_in_R(f"renv::upgrade({charstr})")

    # Add a license to the project
    if license is not None:

        if license.value == "gpl3":
            run_in_R("usethis::use_gpl3_license()")

        elif license.value == "mit":
            run_in_R("usethis::use_mit_license()")


@app.command()
def remove(
    packages: list[str] = typer.Argument(
        ..., help="List of package names to install."
    )
):
    """Remove packages from renv.lock"""
    if len(packages) > 1:
        charstr = to_charcter_vector(packages)
    else:
        charstr = f'"{packages[0]}"'
    run_in_R(f"renv::remove({charstr})")


@app.command()
def test(path: Path = typer.Argument(Path.cwd())):
    """Call devtools::document()."""
    path = abspath(path)
    run_in_R(f'devtools::test("{path.as_posix()}")')


@app.command()
def install(path: Path = typer.Argument(Path.cwd())):
    """Install a package at ``path``."""
    path = abspath(path)
    run_in_R(f'devtools::install("{path.as_posix()}")')


@app.command()
def build(path: Path = typer.Argument(Path.cwd())):
    """Build the package."""
    path = abspath(path)
    run_in_R(f'devtools::build("{path.as_posix()}")')


@app.command()
def document(path: Path = typer.Argument(Path.cwd())):
    """Calls devtools::document()."""
    run_in_R(f'devtools::document("{path.as_posix()}")')
    raise typer.Exit(0)


@app.command()
def check(path: Path = typer.Argument(Path.cwd())):
    """Calls devtools::check()."""
    run_in_R(f'devtools::check("{path.as_posix()}")')
    raise typer.Exit(0)


# @app.command()
# def build_rmd(pkg: Path = typer.Option(".", resolve_path=True)):
#     """Calls devtools::build_rmd() with .Rmd files."""
#     paths: list[Path] = []
#     for rmd_path in pkg.rglob("*.[Rr]md"):
#         md_path = rmd_path.with_suffix(".md")
#         if md_path.exists():
#             if compare_modified_times(md_path, rmd_path):
#                 paths.append(rmd_path)
#         else:
#             paths.append(rmd_path)

#     if not paths:
#         raise typer.Exit(0)

#     vector_string = create_paths_vector(paths)
#     run_in_R(f'devtools::build_rmd({vector_string}, "{pkg.as_posix()}")')
#     raise typer.Exit(0)
