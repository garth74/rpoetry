#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

import typer

from .utils import check_installed, run_in_R

app = typer.Typer(name="precommitr")


@app.callback()
def main():
    """precommitR is essentially a commandline tool for devtools."""
    if not check_installed("devtools"):
        typer.echo("devtools is not installed.")
        raise typer.Abort(1)


@app.command()
def document(pkg: Path = typer.Option(".", resolve_path=True)):
    """Calls the devtools::document() function on the current working directory."""
    for line in run_in_R(f'devtools::document("{pkg.as_posix()}")'):
        typer.echo(line)
    typer.Exit(0)
