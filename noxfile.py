import shutil
import tempfile

import nox

nox.options.default_venv_backend = "none"


@nox.session()
def build(session: nox.Session) -> None:
    session.notify("build-images")


@nox.session(name="build-images")
def build_images(session: nox.Session) -> None:
    session.run(
        "docker",
        "compose",
        "--env-file",
        ".env",
        "--file",
        "stacks/base.docker-compose.yml",
        "build",
        external=True,
    )


@nox.session()
def develop(session: nox.Session) -> None:
    session.run(
        "docker",
        "compose",
        "--env-file",
        ".env",
        "--file",
        "stacks/docker-compose.yml",
        "--file",
        "stacks/docker-compose.override.yml",
        "up",
        external=True,
    )


@nox.session()
def test(session: nox.Session) -> None:
    session.notify("test-unit")
    session.notify("test-integration")
    session.notify("test-e2e")


@nox.session(name="test-unit")
def test_unit(session: nox.Session) -> None:
    session.run("pytest", "-m", "unit")


@nox.session(name="test-integration")
def test_integration(session: nox.Session) -> None:
    session.run("pytest", "-m", "integration")


@nox.session(name="test-e2e")
def test_e2e(session: nox.Session) -> None:
    session.run("pytest", "-m", "e2e")
