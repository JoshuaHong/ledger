import os
import sys
import readline
import shutil
import subprocess

from typing import Callable, Iterable, Optional


SEARCH_DEPENDENCIES: str = ["fzf"]
OPTIONAL_DEPENDENCIES = SEARCH_DEPENDENCIES


def get_input(prompt: str = "") -> str:
    """
    Returns the captured user input. Gracefully exits on EOFError.

    Parameters:
        prompt: An optional prompt to display for user input.

    Returns: The user input.
    """
    try:
        return input(prompt)
    except (EOFError):
        print()
        exit()


def get_binary_input(prompt: str = "", true_value: str = "y",
                     false_value: str = "n", prefill_text: str = "") -> bool:
    """
    Returns the captured binary user input.
    Display an error until the user input matches either the true or the false
    string value.

    Parameters:
        true: An optional string that the user must enter to select the true
              option.
        false: An optional string that the user must enter to select the false
               option.
        prompt: An optional prompt to display for user input.
        prefill_text: An optional prefill text to place in the input buffer.

    Returns: The boolean True if the user input matches the true string value,
             or False if the user input matches the false string value.
    """
    while True:
        binary_input: str = prefill_input(str(prefill_text), prompt)
        if (binary_input.lower() == true_value.lower()):
            return True
        elif (binary_input.lower() == false_value.lower()):
            return False
        else:
            print("\tError: Please enter either \"" + true_value + "\" or \""
                  + false_value + "\".", file=sys.stderr)


def menu(options: list[tuple[str, str]], prompt: str = "") -> int:
    """
    Selection menu which outputs a list of options to select.

    Parameters:
        options: A dictionary mapping the command of the option to the name of
                 the option to display.
        prompt: An optional prompt to display for the user input.

    Returns:
        The number of the option seleted.
    """
    for (command, description) in options:
        print("\t" + command + " - " + description)

    while True:
        command: str = get_input(prompt)
        commands: list[str] = [option[0] for option in options]
        try:
            return commands.index(command)
        except (ValueError):
            print("\tError: Please enter a valid command.", file=sys.stderr)
            continue


def display(items: Iterable[str], is_sorted: bool = False,
            is_reversed: bool = False,
            are_duplicates_hidden: bool = False) -> None:
    """
    Displays all items in the list provided to the "PAGER" command if the
    environment variable is set, or prints to standard output otherwise.

    Parameters:
        items: A list of items to display.
        is_sorted: A boolean denoting whether to sort the list of items.
        is_reversed: A boolean denoting whether to reverse the list of items.
        are_duplicates_hidden: A boolean denoting whether to display duplicates.
    """
    if (is_sorted):
        items = sorted(items)
    if (is_reversed):
        items = reversed(items)
    if (are_duplicates_hidden):
        items = list(dict.fromkeys(items))  # Sort list and preserve order.
    if ("PAGER" in os.environ):
        joined_items: str = '\n'.join(items)
        p1: Popen = subprocess.Popen(
                ["echo", joined_items], stdout=subprocess.PIPE)
        p2: Popen = subprocess.Popen([os.environ.get("PAGER")], stdin=p1.stdout)
        p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
        p2.communicate()  # Wait for the process to terminate.
    else:
        print("\tWarning: The \"PAGER\" environment variable is not set. "
              + "Printing to standard output instead:", file=sys.stderr)
        print("\t", items)


def search(items: Iterable[str], prompt: str = "", is_sorted: bool = False,
           is_reversed: bool = False,
           are_duplicates_hidden: bool = False) -> Optional[str]:
    """
    Search interface which displays a list of items to search.

    Parameters:
        items: A list of items to display.
        prompt: An optional prompt to display for the user input.
        is_sorted: A boolean denoting whether to sort the list of items.
        is_reversed: A boolean denoting whether to reverse the list of items.
        are_duplicates_hidden: A boolean denoting whether to display duplicates.

    Returns:
        The item selected, or None if a dependency is missing.
    """
    missing_dependencies: list[str] = get_missing_dependencies(
            SEARCH_DEPENDENCIES)
    if (len(missing_dependencies) > 0):
        print("\tError: Missing dependencies:", missing_dependencies,
              file=sys.stderr)
        return None

    if (is_sorted):
        items = sorted(items, reverse=True)
    if (is_reversed):
        items = reversed(items)
    if (are_duplicates_hidden):
        items = list(dict.fromkeys(items))  # Sort list and preserve order.
    joined_items: str = '\n'.join(items)
    p1: Popen = subprocess.Popen(
            ["echo", joined_items], stdout=subprocess.PIPE)
    p2: Popen = subprocess.Popen(
            ["fzf", "--prompt", prompt], stdin=p1.stdout,
            stdout=subprocess.PIPE, text=True)
    p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
    return p2.communicate()[0].strip()  # Return the item selected.


def prefill_input(prefill_text: str, prompt: str = "") -> str:
    """
    Prefill the input buffer with a given text for easier editing.

    Parameters:
        prefill_text: A prefill text to place in the input buffer.
        prompt: A prompt to display for the user input.

    Returns:
        The resultant user input.
    """
    def hook() -> None:
        readline.insert_text(str(prefill_text))
        readline.redisplay()

    readline.set_pre_input_hook(hook)
    result: str = get_input(prompt)
    readline.set_pre_input_hook()  # Reset the pre-input hook.
    return result


def function_execution_menu(options_map: dict[tuple[str, str],
                            tuple[Callable, list[any], dict[str, any]]],
                            prompt: str = "") -> any:
    """
    Displays a list of menu options to select and executes the function
    associated to the option selected.

    Parameters:
        options_map: A dictionary mapping a tuple containing the command and the
                     name of the option to select to a tuple containing the
                     function to call if the option is selected and a list of
                     arguments to the function.
        prompt: An optional prompt to display for the user input.

    Returns: The result of the selected function.
    """
    options: list[tuple[str, str]] = list(options_map.keys())
    index: int = menu(options, prompt)
    next_function: Callable = options_map[options[index]][0]
    args: list[any] = options_map[options[index]][1]
    kwargs: dict[str, any] = options_map[options[index]][2]
    return next_function(*args, **kwargs)


def get_missing_dependencies(programs: list[str]) -> list[str]:
    """
    Returns the list of dependencies that are not found on the system.

    Parameters:
        dependencies: A list of programs whose existence to check.

    Returns: The list of dependencies that are not found on the system.
    """
    missing_dependencies: list[str] = list()
    for program in programs:
        if (shutil.which(program) is None):
            missing_dependencies.append(program)
    return missing_dependencies
