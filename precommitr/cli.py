#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pathlib import Path

import typer

from .utils import check_installed, compare_modified_times, create_paths_vector, echo_lines, run_in_R

app = typer.Typer(name="precommitr")


@app.callback()
def main():
    """precommitR - the cli for devtools."""
    if not check_installed("devtools"):
        typer.echo("devtools is not installed.")
        raise typer.Exit(1)


@app.command()
def create(path: Path = typer.Argument(None, resolve_path=True)):
    """Create an R package."""
    echo_lines(run_in_R(f'devtools::create("{path}")'))
    raise typer.Exit(0)


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


@app.command()
def build_rmd(pkg: Path = typer.Option(".", resolve_path=True)):
    """Calls devtools::build_rmd() with .Rmd files."""
    paths: list[Path] = []
    for rmd_path in pkg.rglob("*.[Rr]md"):
        md_path = rmd_path.with_suffix(".md")
        if md_path.exists():
            if compare_modified_times(md_path, rmd_path):
                paths.append(rmd_path)
        else:
            paths.append(rmd_path)

    if not paths:
        raise typer.Exit(0)

    vector_string = create_paths_vector(paths)
    echo_lines(run_in_R(f'devtools::build_rmd({vector_string}, "{pkg.as_posix()}")'))
    raise typer.Exit(0)
