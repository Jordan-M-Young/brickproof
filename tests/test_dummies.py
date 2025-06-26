def add(i: int, j: int) -> int:
    return i + j

def bad_test():

    assert add(0,1) == 2

def test_units():
    real = add(1, 2)
    target = 3

    assert real == target
