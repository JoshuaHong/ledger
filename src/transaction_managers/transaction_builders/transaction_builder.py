from enum import IntEnum
from pathlib import Path
from typing import Optional

import helpers.selector as selector

from .abstract_transaction_builder import AbstractTransactionBuilder
from .address_builder import AddressBuilder
from .item_builder import ItemBuilder
from .receipt_builder import ReceiptBuilder
from .timestamp_builder import TimestampBuilder

from ledger_objects.abstract_ledger_object import AbstractLedgerObject
from transaction_managers.abstract_transaction_manager \
        import AbstractTransactionManager
from ledger_objects.address import Address
from ledger_objects.item import Item
from ledger_objects.ledger import Ledger
from ledger_objects.timestamp import Timestamp
from ledger_objects.transaction import Transaction


class TransactionBuilder(AbstractTransactionBuilder):
    """
    Terminal user interface to build a transaction.
    """

    STEP: list[AbstractLedgerObject.Key] = [Transaction.Key.DESCRIPTION,
            Transaction.Key.ITEMS, Transaction.Key.ADDRESS,
            Transaction.Key.TIMESTAMP, Transaction.Key.PAYMENT_METHOD,
            Transaction.Key.RECEIPT]


    def __init__(self, ledger: Ledger, receipts_directory: Path,
                 search_directory: Optional[Path] = Path.home()) -> None:
        """
        Initializes the transaction builder.

        Parameters:
            ledger: A ledger containing a list of transactions.
            receipts_directory: A directory containing receipts.
            search_directory: An optional directory in which to search for
                    receipts.
        """
        super().__init__(ledger)
        self.receipts_directory: Path = receipts_directory
        self.search_directory: Path = search_directory
        self.item_builder: ItemBuilder = ItemBuilder(ledger)
        self.address_builder: AddressBuilder = AddressBuilder(ledger)
        self.timestamp_builder: TimestampBuilder = TimestampBuilder(ledger)
        self.receipt_builder: ReceiptBuilder = ReceiptBuilder(
                ledger, receipts_directory, search_directory)
        self.description: Optional[str] = None
        self.items = list()
        self.address: Optional[Address] = None
        self.timestamp: Optional[Timestamp] = None
        self.payment_method: str = None
        self.receipt: Path = None
        self.current_step: int = 0
        self.is_backwards: bool = False


    def build(self, prefill_description: Optional[str] = None,
              prefill_items: Optional[list[Item]] = None,
              prefill_address: Optional[Address] = None,
              prefill_timestamp: Optional[Timestamp] = None,
              prefill_payment_method: Optional[str] = None,
              prefill_receipt: Optional[Path] = None) -> Transaction:
        """
        Build a transaction.

        Parameters:
            prefill_description: An optional description to use as the prefill
                                 text.
            prefill_items: An optional list of items to use as the prefill text.
            prefill_address: An optional address to use as the prefill text.
            prefill_timestamp: An optional timestamp to use as the prefill text.
            prefill_payment_method: An optional payment method to use as the
                    prefill text.
            prefill_receipt: An optional receipt to use as the prefill text.

        Returns: The built transaction.
        """
        self._reset()
        while True:
            try:
                if (self.current_step == len(TransactionBuilder.STEP)):
                    if (self._confirm()):
                        return Transaction(self.address, self.description,
                                self.items, self.payment_method, self.receipt,
                                self.timestamp)
                    else:
                        self.current_step -= 1
                        continue
                match TransactionBuilder.STEP[self.current_step]:
                    case Transaction.Key.DESCRIPTION:
                        self.description = self.build_description(
                                self.description or prefill_description or "")
                        self._print_transaction(self.description)
                    case Transaction.Key.ITEMS:
                        self.items = self.build_items(self.items \
                                or prefill_items or list())
                    case Transaction.Key.ADDRESS:
                        self.address = self.build_address(self.address \
                                or prefill_address)
                    case Transaction.Key.TIMESTAMP:
                        self.timestamp = self.build_timestamp(self.timestamp \
                                or prefill_timestamp)
                    case Transaction.Key.PAYMENT_METHOD:
                        self.payment_method = self.build_payment_method(
                                self.payment_method or prefill_payment_method \
                                or "")
                    case Transaction.Key.RECEIPT:
                        self.receipt = self.build_receipt(str(self.receipt) \
                                if self.receipt else (str(prefill_receipt) \
                                if prefill_receipt else ""))
                self.current_step += 1
                self.is_backwards = False
            except (AbstractTransactionManager.Navigation.Back):
                match TransactionBuilder.STEP[self.current_step]:
                    case Transaction.Key.DESCRIPTION:
                        super().navigate_back()
                    case Transaction.Key.ITEMS:
                        self._print_transaction()
                    case Transaction.Key.ADDRESS:
                        self._print_transaction(self.description,
                                self.items[:-1] if self.items else None)
                    case Transaction.Key.TIMESTAMP:
                        self._print_transaction(self.description, self.items)
                    case Transaction.Key.PAYMENT_METHOD:
                        self._print_transaction(self.description, self.items,
                                self.timestamp)
                self.current_step -= 1
                self.is_backwards = True


    def build_description(self, prefill_description: Optional[str] = "") -> str:
        """
        Build a description.

        Parameters:
            prefill_description: An optional description to use as the prefill
                                 text.

        Returns: The built description.
        """
        description: str = super().input_handler(Transaction.Key.DESCRIPTION,
                prefill_description)
        return description


    def build_items(self,
                    prefill_items: Optional[list[Item]] = list()) -> list[Item]:
        """
        Build items.

        Parameters
            prefill_items: An optional list of items to use as the prefill text.

        Returns: The list of built items.
        """
        items: list[Item] = prefill_items
        current_item_step: int = len(items) - 1 if self.is_backwards else 0
        while True:
            print("Add an item:")
            try:
                if (current_item_step < len(items)):
                    items[current_item_step] = self.item_builder.build(
                        items[current_item_step])
                else:
                    items.append(self.item_builder.build())
            except (AbstractTransactionManager.Navigation.Back):
                if (current_item_step):
                    current_item_step -= 1
                    self._print_transaction(self.description,
                                            items[:current_item_step])
                    continue
                else:
                    super().navigate_back()
            current_item_step += 1
            self._print_transaction(self.description,
                                    items[:current_item_step])
            if (not selector.get_binary_input("Add another item? (y/n): ")):
                items[:current_item_step]
                break
        return items[:current_item_step]


    def build_address(self,
                       prefill_address: Optional[Address] = None) -> Address:
        """
        Build an address.

        Parameters:
            prefill_address: An optional address to use as the prefill text.

        Returns: The built address.
        """
        print("Add the address:")
        address: Address = self.address_builder.build(prefill_address)
        self._print_transaction(self.description, self.items, address)
        return address


    def build_timestamp(self,
            prefill_timestamp: Optional[Timestamp] = None) -> Timestamp:
        """
        Build a timestamp.

        Parameters:
            prefill_timestamp: An optional timestamp to use as the prefill text.

        Returns: The built timestamp.
        """
        print("Add the timestamp:")
        timestamp: Timestamp = self.timestamp_builder.build(prefill_timestamp)
        self._print_transaction(self.description, self.items, self.address,
                                timestamp)
        return timestamp


    def build_payment_method(self,
                             prefill_payment_method: Optional[str] = "") -> str:
        """
        Build a payment method.

        Parameters:
            prefill_payment_method: An optional description to use as the prefill
                                    text.

        Returns: The built payment method.
        """
        payment_method: str = super().input_handler(
                Transaction.Key.PAYMENT_METHOD, prefill_payment_method)
        return payment_method


    def build_receipt(self, prefill_receipt: Optional[str] = "") -> Path:
        """
        Build a receipt.

        Parameters:
            prefill_receipt: An optional receipt to use as the prefill text.

        Returns: The built receipt.
        """
        receipt: Receipt = self.receipt_builder.build(prefill_receipt)
        return receipt


    def _print_transaction(self, description: Optional[str] = None,
                          items: Optional[list[Item]] = list(),
                          address: Optional[Address] = None,
                          timestamp: Optional[Timestamp] = None,
                          payment_method: Optional[str] = None,
                          receipt: Optional[Path] = None) -> None:
        """
        Prints the current transaction based on the currently available
        information.

        Parameters:
            description: An optional description to print.
            items: An optional list of items to print.
            address: An optional address to print.
            timestamp: An optional timestamp to print.
            payment_method: An optional payment method to print.
            receipt: An optional receipt to print.
        """
        print("\nCurrent transaction:")
        if (description):
            print("\tDescription: " + description)
        else:
            print("\tEmpty")
        if (items):
            print("\tItems:")
            for item in items:
                print("\t\t" + item.get_formatted_string())
        if (address):
            print("\tAddress: " + address.get_formatted_string())
        if (timestamp):
            print("\tTimestamp: " + timestamp.get_formatted_string())
        if (payment_method):
            print("\tPayment method: " + payment_method)
        if (receipt):
            print("\tReceipt: " + str(receipt))
        print()


    def _confirm(self) -> bool:
        """
        Returns true if the user confirms the transaction, false otherwise.

        Returns: True if the user confirms the transaction, false otherwise.
        """
        self._print_transaction(self.description, self.items, self.address,
                self.timestamp, self.payment_method, self.receipt)
        if (selector.get_binary_input("Save this transaction? (y/n): ")):
            self.receipt = self.receipt_builder.copy(self.receipt)
            return True
        else:
            return False


    def _reset(self) -> None:
        """
        Reset the transaction builder.
        """
        self.description = None
        self.items = list()
        self.address = None
        self.timestamp = None
        self.payment_method = None
        self.receipt = None
        self.current_step = 0
        self.is_backwards = False
