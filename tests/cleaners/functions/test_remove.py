import pytest

from maha.cleaners.functions import remove_extra_spaces


@pytest.mark.parametrize(
    "input, expected, max_keep",
    [
        ("", "", 1),
        ("   ", "  ", 2),
        ("test remove extra spaces", "test remove extra spaces", 1),
        ("  test   remove extra  spaces  ", " test remove extra spaces ", 1),
        ("   test    remove extra  spaces ", "   test    remove extra  spaces ", 5),
    ],
)
def test_remove_extra_spaces(input: str, expected: str, max_keep: int):
    assert remove_extra_spaces(input, max_keep) == expected


def test_remove_extra_spaces_raise_valueerror():
    with pytest.raises(ValueError):
        remove_extra_spaces("", -5)

    with pytest.raises(ValueError):
        remove_extra_spaces("", 4.5)

    with pytest.raises(ValueError):
        remove_extra_spaces("", 0)
