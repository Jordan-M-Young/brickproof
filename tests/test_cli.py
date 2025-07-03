from brickproof.cli import version
from brickproof.version import VERSION


def test_version():
    target = f"brickproof-{VERSION}"

    assert target == version()


