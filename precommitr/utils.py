import typing as t
from pathlib import Path
from subprocess import PIPE, Popen

import typer
from loguru import logger


def execute(cmd: list[str]):
    """Execute a command in a subprocess that iterates over the lines as they are produced."""
    popen = Popen(cmd, stdout=PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):  # type: ignore
        yield stdout_line

    popen.stdout.close()  # type: ignore
    return_code = popen.wait()

    if return_code:
        raise typer.Exit(1)


def run_in_R(command: str):
    """Run the command in an R subprocess."""
    cmd = ["Rscript", "-e", command]
    yield from execute(cmd)


def check_installed(package_name: str):
    """Check if a package is installed in R."""
    try:
        for _ in run_in_R(f"packageVersion('{package_name}')"):
            pass

        return True
    except typer.Exit:
        return False


def compare_modified_times(path1: Path, path2: Path):
    """Returns True if path1 was modified after path2."""
    return path1.stat().st_mtime > path2.stat().st_mtime


def create_paths_vector(paths_iterable: t.Iterable[Path]):
    """Create a string representing R syntax for a vector of file paths."""
    files = [f'"{path.as_posix()}"' for path in paths_iterable]
    return "c(" + ",".join(files) + ")"


def echo_lines(lines: t.Iterable[str]):
    """Echo lines of a command run in R."""
    for line in lines:
        logger.debug(line)
        typer.echo(line)
