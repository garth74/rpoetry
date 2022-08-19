#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import typing as t
from pathlib import Path

import typer

from .utils import check_installed, run_in_R

app = typer.Typer(name="precommitr")


def echo_lines(lines: t.Iterable[str]):
    """Echo lines of a command run in R."""
    for line in lines:
        typer.echo(line)


@app.callback()
def main():
    """precommitR - the cli for devtools."""
    if not check_installed("devtools"):
        typer.echo("devtools is not installed.")
        raise typer.Exit(1)


@app.command()
def document(pkg: Path = typer.Option(".", resolve_path=True)):
    """Calls devtools::document()."""
    echo_lines(run_in_R(f'devtools::document("{pkg.as_posix()}")'))
    raise typer.Exit(0)


@app.command()
def load_all(pkg: Path = typer.Option(".", resolve_path=True)):
    """Calls devtools::load_all()."""
    echo_lines(run_in_R(f'devtools::load_all("{pkg.as_posix()}")'))
    raise typer.Exit(0)


@app.command()
def check(pkg: Path = typer.Option(".", resolve_path=True)):
    """Calls devtools::check()."""
    echo_lines(run_in_R(f'devtools::check("{pkg.as_posix()}")'))
    raise typer.Exit(0)


def compare_modified_times(path1: Path, path2: Path):
    """Returns True if path1 was modified after path2."""
    return path1.stat().st_mtime > path2.stat().st_mtime


def create_paths_vector(paths_iterable: t.Iterable[Path]):
    """Create a string representing R syntax for a vector of file paths."""
    files = [f'"{path.as_posix()}"' for path in paths_iterable]
    return "c(" + ",".join(files) + ")"


@app.command()
def build_rmd(pkg: Path = typer.Option(".", resolve_path=True)):
    """Calls devtools::build_rmd() with .Rmd files."""
    paths: list[Path] = []
    for rmd_path in pkg.rglob("*.[Rr]md"):
        md_path = rmd_path.with_suffix(".md")
        if md_path.exists() and compare_modified_times(md_path, rmd_path):
            paths.append(rmd_path)

    if not paths:
        raise typer.Exit(0)

    vector_string = create_paths_vector(paths)
    echo_lines(run_in_R(f"devtools::build_rmd({vector_string})"))
    raise typer.Exit(0)
