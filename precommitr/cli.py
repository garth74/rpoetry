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
        raise typer.Abort(1)


@app.command()
def document(pkg: Path = typer.Option(".", resolve_path=True)):
    """Calls devtools::document()."""
    echo_lines(run_in_R(f'devtools::document("{pkg.as_posix()}")'))
    typer.Exit(0)


@app.command()
def load_all(pkg: Path = typer.Option(".", resolve_path=True)):
    """Calls devtools::load_all()."""
    echo_lines(run_in_R(f'devtools::load_all("{pkg.as_posix()}")'))
    typer.Exit(0)


@app.command()
def check(pkg: Path = typer.Option(".", resolve_path=True)):
    """Calls devtools::check()."""
    echo_lines(run_in_R(f'devtools::check("{pkg.as_posix()}")'))
    typer.Exit(0)
