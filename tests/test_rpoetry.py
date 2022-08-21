import tempfile
from pathlib import Path

from rpoetry import __version__
from rpoetry.cli import app
from typer.testing import CliRunner

runner = CliRunner()

tempdir = tempfile.TemporaryDirectory()
TEMP_DIRPATH = Path(tempdir.name)


def test_version():
    assert __version__ == "0.1.0"


def test_call_rscript():
    from rpoetry.utils import _run_in_R  # type: ignore

    assert "hello" in set(_run_in_R('cat("hello")'))


def test_create_package():
    """This must come first!!"""
    result = runner.invoke(app, ["create", TEMP_DIRPATH.as_posix()])
    assert result.exit_code == 0


# def test_build_rmd():  # this is slow
#     rmd_paths: list[Path] = []
#     for i in range(3):
#         rmd_path = TEMP_DIRPATH.joinpath(f"newfile{i}.Rmd")
#         rmd_path.touch()
#         rmd_path.write_text(f"---\ntitle: 'Doctitle {i}'\n---\n")
#         rmd_paths.append(rmd_path)

#     result = runner.invoke(app, ["build-rmd", "--pkg", TEMP_DIRPATH.as_posix()])
#     assert result.exit_code == 0

#     for rmd_path in rmd_paths:
#         md_path = rmd_path.with_suffix(".md")
#         assert md_path.exists()


tempdir.cleanup()
