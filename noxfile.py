import nox


SOURCE_FILES = (
    "setup.py",
    "noxfile.py",
    "elastic_workplace_search/",
    "tests/",
)


@nox.session(python=["2.7", "3.4", "3.5", "3.6", "3.7", "3.8"])
def test(session):
    session.install(".", "pytest", "mock")
    session.run("pytest")


@nox.session()
def blacken(session):
    session.install("black")
    session.run("black", *SOURCE_FILES)

    lint(session)


@nox.session()
def lint(session):
    session.install("flake8", "black")
    session.run("black", "--check", *SOURCE_FILES)
    session.run("flake8", "--select=E,W,F", "--max-line-length=88", *SOURCE_FILES)
