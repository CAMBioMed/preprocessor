from ._version import __version__  # type: ignore


def test_add__two_integers():
    expected = 5
    result = 2 + 3
    assert result == expected, f"Expected {expected}, but got {result}."


def test_print_version():
    assert isinstance(__version__, str)
    assert len(__version__) > 0
