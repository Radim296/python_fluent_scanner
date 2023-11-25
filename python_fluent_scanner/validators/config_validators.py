import os


def validate_path(value: str) -> str:
    """
    The function `validate_path` checks if a given string is a valid file path and returns it if it is.

    :param v: The parameter `v` is a string representing a file path
    :type v: str
    :return: the input path `v` if it passes all the validation checks.
    """
    current_dir: str = os.getcwd()

    assert value, f"{value}, must be a path, not empty string"
    assert value[0] != "/", f"{value} must not begin with /"
    assert os.path.isfile(
        f"{current_dir}/{value}"
    ), f"the file by {value} was not found, check the path"

    return value


def validate_dictionaries_dict(value: dict) -> dict:
    """
    The function `validate_dictionaries_dict` validates that a dictionary is provided as input and
    returns a dictionary.

    :param value: The parameter `value` is a dictionary
    :type value: dict
    :return: the built-in `dict` class.
    """
    assert value, "You should provide at least one dictionary"

    return dict
