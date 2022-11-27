from pathlib import Path

from .abstract_ledger_object import AbstractLedgerObject
from .address import Address
from .item import Item
from .timestamp import Timestamp


class Transaction(AbstractLedgerObject):
    """
    An object containing the transaction data.
    """

    def __init__(self, address: Address, description: str, items: list[Item],
                 payment_method: str, receipt: Path,
                 timestamp: Timestamp) -> None:
        """
        Initializes a transaction.
        """
        self.address: Address = address
        self.description: str = description
        self.items: list[Item] = items
        self.payment_method: str = payment_method
        self.receipt: Path = receipt
        self.timestamp: Timestamp = timestamp
        self.total: float = self._calculate_total(items)


    class Key(AbstractLedgerObject.Key):
        """
        The keys required in a transaction JSON.
        """
        ADDRESS: str = "address"
        DESCRIPTION: str = "description"
        ITEMS: str = "items"
        PAYMENT_METHOD: str = "payment method"
        RECEIPT: str = "receipt"
        TIMESTAMP: str = "timestamp"
        TOTAL: str = "total"


    def get(self, key: Key) -> any:
        """
        Returns the entry with the given key, or None if the key is not found.

        Parameters:
            key: A key associated to the entry to search.

        Returns: The entry with the given key, or None if the key is not found.
        """
        match key:
            case Transaction.Key.ADDRESS:
                return self.get_address()
            case Transaction.Key.DESCRIPTION:
                return self.get_description()
            case Transaction.Key.ITEMS:
                return self.get_items()
            case Transaction.Key.PAYMENT_METHOD:
                return self.get_payment_method()
            case Transaction.Key.RECEIPT:
                return self.get_receipt()
            case Transaction.Key.TIMESTAMP:
                return self.get_timestamp()
            case Transaction.Key.TOTAL:
                return self.get_total()
            case _:
                return None


    def get_formatted_string(self) -> str:
        """
        Returns the formatted transaction string.

        Returns: The formatted transaction string.
        """
        return self.get_timestamp().get_formatted_string() + ", " \
                + self.get_description() + ", ['" \
                + "', '".join(map(
                    lambda item: str(item.get_name()), self.get_items())) \
                + "'], " + self.get_address().get_name()


    def get_address(self) -> Address:
        """
        Returns the transaction address.

        Returns: The transaction address.
        """
        return self.address


    def get_description(self) -> str:
        """
        Returns the transaction description.

        Returns: The transaction description.
        """
        return self.description


    def get_items(self) -> list[Item]:
        """
        Returns the transaction items.

        Returns: The transaction items.
        """
        return self.items


    def get_payment_method(self) -> str:
        """
        Returns the transaction payment method.

        Returns: The transaction payment method.
        """
        return self.payment_method


    def get_receipt(self) -> Path:
        """
        Returns the transaction receipt.

        Returns: The transaction receipt.
        """
        return self.receipt


    def get_timestamp(self) -> Timestamp:
        """
        Returns the transaction timestamp.

        Returns: The transaction timestamp.
        """
        return self.timestamp


    def get_total(self) -> float:
        """
        Returns the transaction total.

        Returns: The transaction total.
        """
        return self.total


    def set_address(self, address: Address) -> None:
        """
        Sets the transaction address.

        Parameters:
            address: The transaction address to set.
        """
        self.address = address


    def set_description(self, description: str) -> None:
        """
        Sets the transaction description.

        Parameters:
            description: The transaction description to set.
        """
        self.description = description


    def set_items(self, items: list[Item]) -> None:
        """
        Sets the transaction items and update the total.

        Parameters:
            items: The transaction items to set.
        """
        self.items = items
        self.total = self._calculate_total(items)


    def set_payment_method(self, payment_method: str) -> None:
        """
        Sets the transaction payment method.

        Parameters:
            payment_method: The transaction payment method to set.
        """
        self.payment_method = payment_method


    def set_receipt(self, receipt: Path) -> None:
        """
        Sets the transaction receipt.

        Parameters:
            receipt: The transaction receipt to set.
        """
        self.receipt = receipt


    def set_timestamp(self, timestamp: Timestamp) -> None:
        """
        Sets the transaction timestamp.

        Parameters:
            timestamp: The transaction timestamp to set.
        """
        self.timestamp = timestamp


    def _calculate_total(self, items: list[Item]) -> float:
        """
        Calculates the total value of all items.

        Parameters:
            items: The list of items whose prices to summate.

        Returns: The total value of all items.
        """
        total: float = 0
        for item in items:
            total += item.get_price()
        return total
