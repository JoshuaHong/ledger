import os
import sys

from enum import StrEnum
from pathlib import Path
from typing import Callable, Optional

import helpers.file_helper as file_helper
import helpers.json_parser as json_parser
import helpers.selector as selector

from ledger_objects.abstract_ledger_object import AbstractLedgerObject
from ledger_objects.address import Address
from ledger_objects.item import Item
from ledger_objects.ledger import Ledger
from ledger_objects.timestamp import Timestamp
from ledger_objects.transaction import Transaction


class AbstractTransactionManager:
    """
    Abstract class to manage transactions in the ledger.
    """

    class Commands(StrEnum):
        """
        Commands that can be executed instead of entering an input.
        """
        BACK: str = "b"
        COMMANDS: str = "c"
        LIST: str = "l"
        MENU: str = "m"
        SEARCH: str = "s"


    class Navigation(Exception):
        """
        Exceptions used for navigating the control flow.
        """

        class MainMenu(Exception):
            """
            Exception to return to the main menu.
            """
            pass

        class Back(Exception):
            """
            Exception to return to the previous function.
            """
            pass

        class CommandMenu(Exception):
            """
            Exception to show the command menu.
            """
            pass


    EMPTY_LEDGER_JSON: dict[str, list[any]] = dict(
            [(Ledger.Key.TRANSACTIONS, list())])

    NO_RECEIPT: Path = Path("N/A")


    def __init__(self, ledger_file: Path, receipts_directory: Path,
                 is_new_file: bool = False,
                 search_directory: Optional[Path] = Path.home()) -> None:
        """
        Asserts that the ledger file exists and parses the transactions, or
        creates a new ledger file if "is_new_file" is true and asserts that the
        file dosen't already exist.

        Parameters:
            ledger_file: A ledger file to verify.
            receipts_directory: A directory containing receipts.
            is_new_file: A boolean denoting whether to create a new ledger file.
            search_directory: An optional directory in which to search for
                    receipts.
        """
        if (is_new_file):
            file_helper.assert_file_not_exists(ledger_file)
            file_helper.write_json(ledger_file, self.EMPTY_LEDGER_JSON)
        else:
            file_helper.assert_file_exists(ledger_file)
        file_helper.assert_directory_exists(receipts_directory)
        file_helper.assert_directory_exists(search_directory)
        self._warn_missing_optional_dependencies()

        self.ledger_file = ledger_file
        self.receipts_directory = receipts_directory
        self.search_directory = search_directory
        self.ledger: Ledger = json_parser.parse_ledger_json(
                file_helper.read_json(ledger_file))


    def input_handler(self, key: AbstractLedgerObject.Key,
            prefill_text: str = "",
            list_command: Optional[
                tuple[Callable, list[any], dict[str, any]]] = None,
            search_command: Optional[
                tuple[Callable, list[any], dict[str, any]]] = None,
            can_go_back: bool = True, can_list_and_search: bool = True,
            prompt: Optional[str] = None) -> str:
        """
        Prompts the user to enter their either their input or a command. If a
        command is entered, handle the appropriate command. If an input is
        entered, return it.

        Parameters:
            key: A key of the entry being added.
            prefill_text: An optional prefill text to place in the input buffer.
            list_command: An optional tuple containing a custom function to call
                    if the list command is selected and a list of arguments to
                    the function.
            search_command: An optional tuple containing a custom function to
                    call if the search command is selected and a list of
                    arguments to the function.
            can_go_back: A boolean denoting whether the back command should be
                    available.
            can_list_and_search: A boolean denoting whether the list and search
                    commands should be available.

        Returns: The user input.
        """
        if (not prompt):
            prompt: str = "Enter the " + key + " (c for commands): "
        while True:
            user_input: str = selector.prefill_input(
                    prefill_text, prompt).strip()
            prefill_text = ""
            match user_input:
                case "":
                    print("\tError: " + key.capitalize() +  " cannot be empty.",
                          file=sys.stderr)
                case AbstractTransactionManager.Commands.COMMANDS:
                    self._print_commands(can_go_back, can_list_and_search)
                case AbstractTransactionManager.Commands.BACK:
                    if (can_go_back):
                        self.navigate_back()
                    else:
                        return user_input
                case AbstractTransactionManager.Commands.LIST:
                    if (not can_list_and_search):
                        return user_input
                    if (list_command):
                        args: list[any] = list_command[1]
                        kwargs: dict[str, any] = list_command[2]
                        list_command[0](*args, **kwargs)
                    else:
                        selector.display(list(self.get_all(key)),
                                         are_duplicates_hidden=True)
                case AbstractTransactionManager.Commands.SEARCH:
                    if (not can_list_and_search):
                        return user_input
                    if (search_command):
                        args: list[any] = search_command[1]
                        kwargs: dict[str, any] = search_command[2]
                        prefill_text = search_command[0](*args, **kwargs)
                    else:
                        prefill_text = selector.search(
                                list(self.get_all(key)),
                                prompt="Search: ", is_reversed=True,
                                are_duplicates_hidden=True)
                case AbstractTransactionManager.Commands.MENU:
                    self.navigate_to_main_menu()
                case _:
                    return user_input


    def get_all(self, key: AbstractLedgerObject.Key) -> list[any]:
        """
        Returns a list of entries with the given key from all transactions.

        Parameters:
            key: A key associated to the entry to search.

        Returns: The list of all entries with the given key.
        """
        entries: list[any] = list()
        if (isinstance(key, Ledger.Key)):
            return self.ledger.get_transactions()
        for transaction in self.ledger.get_transactions():
            if (isinstance(key, Address.Key)):
                address: Address = transaction.get_address()
                entries.append(address.get(key))
            elif (isinstance(key, Item.Key)):
                items: list[Item] = transaction.get_items()
                for item in items:
                    if (key == Item.Key.TAGS):
                        entries.extend(item.get(key))
                    else:
                        entries.append(item.get(key))
            elif (isinstance(key, Transaction.Key)):
                entries.append(transaction.get(key))
            else:
                return list()
        return entries


    def print_transaction(self, transaction: Transaction,
                          has_newline: bool = True) -> None:
        """
        Print the formatted transaction.

        Parameters:
            transaction: A transaction to print.
            has_newline: A boolean denoting whether to add a trailing newline.
        """
        print("\nCurrent transaction:")
        print("\tDescription: " + transaction.get_description())
        print("\tItems:")
        for item in transaction.get_items():
            print("\t\t" + item.get_formatted_string())
        print("\tAddress: " + transaction.get_address().get_formatted_string())
        print("\tTimestamp: "
              + transaction.get_timestamp().get_formatted_string())
        print("\tPayment method: " + transaction.get_payment_method())
        print("\tReceipt: " + str(transaction.get_receipt()))
        if (has_newline):
            print()


    def navigate_back(self) -> None:
        """
        Helper function to navigate to the previous function.
        """
        raise AbstractTransactionManager.Navigation.Back()


    def navigate_to_main_menu(self) -> None:
        """
        Helper function to navigate to the main menu.
        """
        raise AbstractTransactionManager.Navigation.MainMenu()


    def show_command_menu(self) -> None:
        """
        Helper function to show the command menu.
        """
        raise AbstractTransactionManager.Navigation.CommandMenu()


    def _warn_missing_optional_dependencies(self) -> None:
        """
        Prints a warning if any optional dependencies are missing.
        """
        missing_dependencies: list[str] = selector.get_missing_dependencies(
                selector.OPTIONAL_DEPENDENCIES)
        if (len(missing_dependencies)):
            print("Warning: Missing optional dependencies:",
                  missing_dependencies, file=sys.stderr)

        if ("PAGER" not in os.environ):
            print("Warning: The \"PAGER\" environment variable is not set. ",
                  file=sys.stderr)


    def _print_commands(self, can_go_back: bool = True,
                        can_list_and_search: bool = True) -> None:
        """
        Prints the list of available commands.
        """
        if (can_go_back):
            print("\t" + AbstractTransactionManager.Commands.BACK
                  + " - Go back")
        if (can_list_and_search):
            print("\t" + AbstractTransactionManager.Commands.LIST
                + " - List previous entries")
            print("\t" + AbstractTransactionManager.Commands.SEARCH
                + " - Search previous entries")
        print("\t" + AbstractTransactionManager.Commands.MENU
              + " - Return to main menu")
