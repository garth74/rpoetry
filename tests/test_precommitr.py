from precommitr import __version__


def test_version():
    assert __version__ == "0.1.0"


def test_call_rscript():
    from precommitr.utils import run_in_R

    assert "hello" in set(run_in_R('cat("hello")'))
