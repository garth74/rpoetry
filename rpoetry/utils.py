import typing as t
from pathlib import Path
from subprocess import PIPE, Popen

import typer
from loguru import logger

DEBUG = False


def execute(cmd: list[str]):
    """
    Execute a command in a subprocess and
    iterates over the lines as they are produced.
    """
    popen = Popen(cmd, stdout=PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):  # type: ignore
        yield stdout_line

    popen.stdout.close()  # type: ignore
    return_code = popen.wait()

    if return_code:
        raise typer.Exit(1)


def _run_in_R(command: str):
    """Run the command in an R subprocess."""
    cmd = ["Rscript", "-e", command]
    yield from execute(cmd)


def run_in_R(command: str, quiet: bool = False):
    """Run the command in an R subprocess."""
    for line in _run_in_R(command):
        if not quiet:
            typer.echo(line)

        if DEBUG:
            logger.debug(line)


def check_installed(package_name: str):
    """Check if a package is installed in R."""
    try:
        run_in_R(f"packageVersion('{package_name}')")
        return True
    except typer.Exit:
        return False


def compare_modified_times(path1: Path, path2: Path):
    """Returns True if path1 was modified after path2."""
    return path1.stat().st_mtime > path2.stat().st_mtime


def create_paths_vector(paths_iterable: t.Iterable[Path]):
    """Create a string representing R syntax for a vector of file paths."""
    return to_charcter_vector(paths_iterable, to_str=Path.as_posix)


def to_charcter_vector(
    iterable: t.Iterable[t.Any], to_str: t.Callable[[t.Any], str] = str
):
    """Convert an iterable to a character vector string."""
    quoted_iterable = (f'"{elem}"' for elem in map(to_str, iterable))
    return "c(" + ",".join(quoted_iterable) + ")"
