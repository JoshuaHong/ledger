import sys

from pathlib import Path
from typing import Optional

import helpers.selector as selector

from ledger_objects.item import Item
from ledger_objects.ledger import Ledger
from ledger_objects.transaction import Transaction

from .abstract_transaction_manager import AbstractTransactionManager
from .transaction_builders.address_builder import AddressBuilder
from .transaction_builders.item_builder import ItemBuilder
from .transaction_builders.receipt_builder import ReceiptBuilder
from .transaction_builders.timestamp_builder import TimestampBuilder
from .transaction_builders.transaction_builder import TransactionBuilder


class TransactionEditor(AbstractTransactionManager):
    """
    Terminal user interface to edit transactions in the ledger.
    """

    def __init__(self, ledger: Ledger, receipts_directory: Path,
                 search_directory: Optional[Path] = Path.home()) -> None:
        """
        Initializes the transaction editor.

        Parameters:
            ledger: A ledger containing a list of transactions.
            receipts_directory: A directory containing receipts.
            search_directory: An optional directory in which to search for
                    receipts.
        """
        self.ledger: Ledger = ledger
        self.receipts_directory: Path = receipts_directory
        self.address_builder: AddressBuilder = AddressBuilder(ledger)
        self.item_builder: ItemBuilder = ItemBuilder(ledger)
        self.receipt_builder: ReceiptBuilder = ReceiptBuilder(
                ledger, receipts_directory, search_directory)
        self.timestamp_builder: TimestampBuilder = TimestampBuilder(ledger)
        self.transaction_builder: TransactionBuilder = TransactionBuilder(
                ledger, receipts_directory)
        self.previous_receipt: Optional[Path] = \
                AbstractTransactionManager.NO_RECEIPT


    def edit_address(self, transaction: Transaction, index: int) -> None:
        """
        Edits the selected transaction address.

        Parameters:
            transaction: A transaction whose address to edit.
            index: The index of the transaction in the ledger.
        """
        try:
            transaction.set_address(self.address_builder.build(
                transaction.get_address()))
        except (AbstractTransactionManager.Navigation.Back):
            return None
        return transaction if self._confirm(transaction, index) else None


    def edit_description(self, transaction: Transaction, index: int) -> None:
        """
        Edits the selected transaction description.

        Parameters:
            transaction: A transaction whose description to edit.
            index: The index of the transaction in the ledger.
        """
        try:
            transaction.set_description(
                    self.transaction_builder.build_description(
                        transaction.get_description()))
        except (AbstractTransactionManager.Navigation.Back):
            return None
        return transaction if self._confirm(transaction, index) else None


    def edit_items(self, transaction: Transaction, index: int) -> None:
        """
        Edits the selected transaction items.

        Parameters:
            transaction: A transaction whose items to edit.
            index: The index of the transaction in the ledger.
        """
        items: list[Item] = transaction.get_items()
        item_and_index: tuple[Item, int] = self._get_selected_item_and_index(
                items)
        item: Item = item_and_index[0]
        index: int = item_and_index[1]
        try:
            items[index] = self.item_builder.build(item)
        except (AbstractTransactionManager.Navigation.Back):
            return None
        transaction.set_items(items)
        return transaction if self._confirm(transaction, index) else None


    def edit_timestamp(self, transaction: Transaction, index: int) -> None:
        """
        Edits the selected transaction timestamp.

        Parameters:
            transaction: A transaction whose timestamp to edit.
            index: The index of the transaction in the ledger.
        """
        try:
            transaction.set_timestamp(self.timestamp_builder.build(
                transaction.get_timestamp()))
        except (AbstractTransactionManager.Navigation.Back):
            return None
        return transaction if self._confirm(transaction, index) else None


    def edit_payment_method(self, transaction: Transaction, index: int) -> None:
        """
        Edits the selected transaction payment method.

        Parameters:
            transaction: A transaction whose payment method to edit.
            index: The index of the transaction in the ledger.
        """
        try:
            transaction.set_payment_method(
                    self.transaction_builder.build_payment_method(
                        transaction.get_payment_method()))
        except (AbstractTransactionManager.Navigation.Back):
            return None
        return transaction if self._confirm(transaction, index) else None


    def edit_receipt(self, transaction: Transaction, index: int) -> None:
        """
        Edits the selected transaction receipt.
        """
        try:
            self.previous_receipt = transaction.get_receipt()
            transaction.set_receipt(self.receipt_builder.build(
                self.previous_receipt))
        except (AbstractTransactionManager.Navigation.Back):
            return None
        return transaction if self._confirm(transaction, index,
                is_receipt_updated=True) else None


    def _get_selected_item_and_index(self,
                                     items: list[Item]) -> tuple[Item, int]:
        """
        Returns the tuple containnig the selected item and index.

        Returns: The tuple containing the selected item and index.
        """
        formatted_items: list[str] = self._get_formatted_items(items)
        while True:
            try:
                index: int = int(super().input_handler(Transaction.Key.ITEMS,
                        prompt="Enter the item number (c for commands): ",
                        list_command=(selector.display,
                            [formatted_items],
                            {"are_duplicates_hidden": True}),
                        search_command=(self._search_items,
                            [formatted_items], dict())))
                item: Item = items[index]
            except (ValueError, IndexError):
                print("\tError: Please enter a valid item number.",
                      file=sys.stderr)
                continue
            else:
                return (item, index)


    def _get_formatted_items(self, items: list[Item]) -> list[str]:
        """
        Returns a list of formatted items.

        Parameters:
            items: A list of items to format.

        Returns: The list of formatted items.
        """
        formatted_items: list[str] = list()
        for (index, item) in enumerate(items):
            formatted_items.append(str(index) + ": "
                                   + item.get_formatted_string())
        return formatted_items


    def _search_items(self, formatted_items: list[str]) -> int:
        """
        Search through a list of formatted items and return the selected item's
        index.

        Parameters:
            formatted_items: A list of formatted items.

        Returns: An integer representing the selected item's index.
        """
        return formatted_items.index(selector.search(formatted_items,
                are_duplicates_hidden=True, is_reversed=True,
                prompt="Search: "))


    def _confirm(self, transaction: Transaction, index: int,
                 is_receipt_updated: bool = False) -> bool:
        """
        Confirm and save the current transaction in the ledger.

        Parameters:
            transaction: The transaction to edit.
            index: The index of the transaction in the ledger.
            is_receipt_updated: A boolean denoting whether to update the receipt
                    in the receipts directory.

        Returns: True if the user confirms the transaction, false otherwise.
        """
        super().print_transaction(transaction)
        if (selector.get_binary_input("Save this transaction? (y/n): ")):
            if (is_receipt_updated):
                if (self.previous_receipt != \
                        AbstractTransactionManager.NO_RECEIPT):
                    self.receipts_directory.joinpath(
                            self.previous_receipt).unlink()
                transaction.set_receipt(
                        self.receipt_builder.copy(transaction.get_receipt()))
            return True
        else:
            return False
