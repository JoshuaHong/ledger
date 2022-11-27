import copy
import sys

from pathlib import Path
from typing import Optional

import helpers.file_helper as file_helper
import helpers.json_builder as json_builder
import helpers.selector as selector

from .abstract_transaction_manager import AbstractTransactionManager
from .transaction_builders.transaction_builder import TransactionBuilder
from .transaction_editor import TransactionEditor

from ledger_objects.ledger import Ledger
from ledger_objects.transaction import Transaction


class TransactionManager(AbstractTransactionManager):
    """
    Terminal user interface to manage transactions in the ledger.
    """

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
        super().__init__(ledger_file, receipts_directory, is_new_file,
                         search_directory)
        self.transaction_builder: TransactionBuilder = TransactionBuilder(
                self.ledger, self.receipts_directory, self.search_directory)
        self.transaction_editor: TransactionEditor = TransactionEditor(
                self.ledger, self.receipts_directory, self.search_directory)


    def main_menu(self) -> None:
        """
        Executes the transaction management terminal user interface menu.
        """
        while True:
            print("Manage your transactions:")
            while True:
                try:
                    selector.function_execution_menu({
                        ("a", "Add a transaction"): (self._add, list(), dict()),
                        ("e", "Edit a transaction"):
                        (self._edit, list(), dict()),
                        ("r", "Remove a transaction"): (self._remove, list(),
                                dict()),
                        ("l", "List all transactions"): (self._list, list(),
                                dict()),
                        ("s", "Search all transactions"): (self._search, list(),
                                dict()),
                        ("c", "Print this command menu"):
                            (super().show_command_menu, list(), dict()),
                        ("q", "Quit"): (exit, list(), dict())},
                        "Command (c for commands): ")
                except (AbstractTransactionManager.Navigation.CommandMenu):
                    continue
                except (AbstractTransactionManager.Navigation.Back,
                        AbstractTransactionManager.Navigation.MainMenu):
                    print()
                    break


    def _add(self) -> None:
        """
        Add a new transaction to the ledger.
        """
        print("\nAdd a new transaction:")
        self.ledger.add_transaction(self.transaction_builder.build())
        file_helper.write_json(self.ledger_file,
                json_builder.build_ledger_json(self.ledger))
        print("Transaction saved.")
        super().navigate_to_main_menu()


    def _edit(self) -> None:
        """
        Edit a transaction in the ledger.
        """
        if (not self.ledger.get_transactions()):
            print("\tWarning: No transactions in the ledger.", file=sys.stderr)
            super().navigate_to_main_menu()

        print("\nEdit a transaction:")
        while True:
            transaction_and_index: tuple[Transaction, int] = \
                    self._get_selected_transaction_and_index()
            transaction: Transaction = transaction_and_index[0]
            index: int = transaction_and_index[1]
            while True:
                try:
                    new_transaction: Optional[Transaction] = \
                            selector.function_execution_menu({
                            ("a", "Edit the address"):
                                (self.transaction_editor.edit_address,
                                [transaction, index], dict()),
                            ("d", "Edit the description"):
                                (self.transaction_editor.edit_description,
                                [transaction, index], dict()),
                            ("i", "Edit the items"):
                                (self.transaction_editor.edit_items,
                                [transaction, index], dict()),
                            ("p", "Edit the payment method"):
                                (self.transaction_editor.edit_payment_method,
                                [transaction, index], dict()),
                            ("r", "Edit the receipt"):
                                (self.transaction_editor.edit_receipt,
                                [transaction, index], dict()),
                            ("t", "Edit the timestamp"):
                                (self.transaction_editor.edit_timestamp,
                                [transaction, index], dict()),
                            ("b", "Go back"):
                                (super().navigate_back, list(), dict()),
                            ("m", "Return to main menu"):
                                (super().navigate_to_main_menu, list(), dict()),
                            ("c", "Print this command menu"):
                                (super().show_command_menu, list(), dict())},
                            "Command (c for commands): ")
                except (AbstractTransactionManager.Navigation.CommandMenu):
                    continue
                except (AbstractTransactionManager.Navigation.Back):
                    print()
                    break
                else:
                    if (not new_transaction):
                        continue
                    self.ledger.remove_transaction(index)
                    self.ledger.add_transaction(new_transaction)
                    file_helper.write_json(self.ledger_file,
                            json_builder.build_ledger_json(self.ledger))
                    print("Transaction saved.")
                    super().navigate_to_main_menu()


    def _remove(self) -> None:
        """
        Remove a transaction from the ledger.
        """
        if (not self.ledger.get_transactions()):
            print("\tWarning: No transactions in the ledger.", file=sys.stderr)
            super().navigate_to_main_menu()

        print("\nRemove a transaction:")
        transaction_and_index: tuple[Transaction, int] = \
                self._get_selected_transaction_and_index()
        transaction: Transaction = transaction_and_index[0]
        index: int = transaction_and_index[1]
        super().print_transaction(self.ledger.get_transactions()[index])
        if (not selector.get_binary_input("Remove this transaction? (y/n): ")):
            super().navigate_to_main_menu()

        self.ledger.remove_transaction(index)
        file_helper.write_json(self.ledger_file,
                json_builder.build_ledger_json(self.ledger))
        if (str(transaction.get_receipt()) != "N/A"):
            try:
                self.receipts_directory.joinpath(
                        transaction.get_receipt()).unlink()
            except (FileNotFoundError):
                print("\tWarning: The receipt file was not found.",
                      file=sys.stderr)
        print("Transaction removed.")
        super().navigate_to_main_menu()


    def _list(self) -> None:
        """
        List previous transactions in the ledger.
        """
        if (not self.ledger.get_transactions()):
            print("\tWarning: No transactions in the ledger.", file=sys.stderr)
            super().navigate_to_main_menu()

        formatted_transactions: list[str] = self._get_formatted_transactions()
        selector.display(formatted_transactions, are_duplicates_hidden=True)
        super().navigate_to_main_menu()


    def _search(self) -> None:
        """
        Search previous transactions in the ledger.
        """
        if (not self.ledger.get_transactions()):
            print("\tWarning: No transactions in the ledger.", file=sys.stderr)
            super().navigate_to_main_menu()

        formatted_transactions: list[str] = self._get_formatted_transactions()
        try:
            super().print_transaction(self.ledger.get_transactions()[
                self._search_transactions(formatted_transactions)],
                has_newline=False)
        except (ValueError, IndexError):
            print("\tError: Please enter a valid transaction number.",
                    file=sys.stderr)
        super().navigate_to_main_menu()


    def _get_selected_transaction_and_index(self) -> tuple[Transaction, int]:
        """
        Returns the tuple containing the selected transaction and index.

        Returns: The tuple containnig the selected transaction and index.
        """
        formatted_transactions: list[str] = self._get_formatted_transactions()
        while True:
            try:
                index: int = int(super().input_handler(Ledger.Key.TRANSACTIONS,
                        prompt="Enter the transaction number "
                                + "(c for commands): ",
                        list_command=(selector.display,
                            [formatted_transactions],
                            {"are_duplicates_hidden": True}),
                        search_command=(self._search_transactions,
                            [formatted_transactions], dict())))
                transaction: Transaction = self.ledger.get_transactions()[index]
            except (ValueError, IndexError):
                print("\tError: Please enter a valid transaction number.",
                      file=sys.stderr)
                continue
            else:
                # Make a copy to not modify the transaction in the ledger.
                return (copy.deepcopy(transaction), index)


    def _get_formatted_transactions(self) -> list[str]:
        """
        Returns a list of formatted transactions.

        Returns: The list of formatted transactions.
        """
        formatted_transactions: list[str] = list()
        for (index, transaction) in enumerate(self.ledger.get_transactions()):
            formatted_transactions.append(str(index) + ": "
                                          + transaction.get_formatted_string())
        return formatted_transactions


    def _search_transactions(self, formatted_transactions: list[str]) -> int:
        """
        Search through a list of formatted transactions and return the selected
        transaction's index.

        Parameters:
            formatted_transactions: A list of formatted transactions.

        Returns: An integer representing the selected transaction's index.
        """
        return formatted_transactions.index(selector.search(
                formatted_transactions, are_duplicates_hidden=True,
                is_reversed=True, prompt="Search: "))
