from subprocess import PIPE, CalledProcessError, Popen


def execute(cmd: list[str]):
    """Execute a command in a subprocess that iterates over the lines as they are produced."""
    popen = Popen(cmd, stdout=PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):  # type: ignore
        yield stdout_line

    popen.stdout.close()  # type: ignore
    return_code = popen.wait()

    if return_code:
        raise CalledProcessError(return_code, cmd)


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
    except CalledProcessError:
        return False
