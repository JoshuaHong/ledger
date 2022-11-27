from .abstract_ledger_object import AbstractLedgerObject
from .transaction import Transaction


class Ledger(AbstractLedgerObject):
    """
    An object containing the ledger data.
    """

    def __init__(self, transactions: list[Transaction]) -> None:
        """
        Initializes a ledger.
        """
        self.transactions = transactions
        self.transactions.sort(key=lambda transaction: \
                transaction.get_timestamp().get_timestamp())


    class Key(AbstractLedgerObject.Key):
        """
        The keys required in a ledger JSON.
        """
        TRANSACTIONS: str = "transactions"


    def get(self, key: Key) -> any:
        """
        Returns the entry with the given key, or None if the key is not found.

        Parameters:
            key: A key associated to the entry to search.

        Returns: The entry with the given key, or None if the key is not found.
        """
        match key:
            case Ledger.Key.TRANSACTIONS:
                return self.get_transactions()
            case _:
                return None


    def get_transactions(self) -> list[Transaction]:
        """
        Returns the list of transactions in the ledger.

        Returns: The list of transactions in the ledger.
        """
        return self.transactions


    def set_transactions(self, transactions: list[Transaction]) -> None:
        """
        Sets the list of transactions in the ledger.

        Parameters:
            transactions: The list of transactions to set.
        """
        self.transactions = transactions
        self.transactions.sort(key=lambda transaction: \
                transaction.get_timestamp().get_timestamp())


    def add_transaction(self, transaction: Transaction) -> None:
        """
        Adds a new transaction to the ledger.

        Parameters:
            transaction: The transaction to add.
        """
        self.transactions.append(transaction)
        self.transactions.sort(key=lambda transaction: \
                transaction.get_timestamp().get_timestamp())


    def remove_transaction(self, index: int) -> None:
        """
        Removes the transaction from the ledger at the given index if it exists.
        Does nothing otherwise.

        Parameters:
            index: The index of the transaction to remove from the ledger.
        """
        if (index < len(self.transactions)):
            del self.transactions[index]


    def clear_transactions(self) -> None:
        """
        Clears all transactions from the ledger.
        """
        self.transactions.clear()
