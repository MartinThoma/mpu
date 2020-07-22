# Third party
import nox


@nox.session(python=["3.6", "3.7", "3.8"])
def test(session):
    session.install(".[all]")
    session.install("-r", "requirements-dev.txt")
    session.run("pytest")


@nox.session(python="3.8")
def lint(session):
    session.install("-r", "requirements-lint.txt")
    session.run("flake8", ".")
    session.run("black", ".", "--check")
