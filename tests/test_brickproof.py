from brickproof.__main__ import main


def test_main():
    real = main()
    target = 0

    assert real == target
