import json
import sys

from pathlib import Path


def assert_file_exists(file: Path) -> None:
    """
    Asserts that the file exists.
    Exits the program if it does not exist.

    Parameters:
        file: The file whose existance to check.
    """
    if (not file.is_file()):
        sys.exit("Error: File \"" + str(file) + "\" does not exist.")


def assert_file_not_exists(file: Path) -> None:
    """
    Asserts that the file does not exist.
    Exits the program if it exists.

    Parameters:
        file: The file whose existance to check.
    """
    if (file.is_file()):
        sys.exit("Error: File \"" + str(file) + "\" already exists.")


def assert_directory_exists(directory: Path) -> None:
    """
    Asserts that the directory exists.
    Exits the program if it does not exist.

    Parameters:
        directory: The directory whose existance to check.
    """
    if (not directory.is_dir()):
        sys.exit("Error: Directory \"" + str(directory) + "\" does not exist.")


def read_json(file: Path) -> dict[str, any]:
    """
    Reads JSON from a file.

    Parameters:
        file: The file from which to read JSON data.

    Returns: The decoded JSON data.
    """
    with file.open() as json_file:
        return json.load(json_file)


def write_json(file: Path, data: dict[str, any]) -> None:
    """
    Writes to a file.

    Parameters:
        file: The file to which to write JSON data.
        text: The JSON data to write to the file.
    """
    with file.open('w') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
        json_file.write('\n')
