from ledger_objects.ledger import Ledger
from transaction_managers.abstract_transaction_manager \
        import AbstractTransactionManager


class AbstractTransactionBuilder(AbstractTransactionManager):
    """
    Abstract class to build transactions.
    """

    def __init__(self, ledger: Ledger) -> None:
        """
        Initializes the transaction builder.

        Parameters:
            ledger: A ledger containing a list of transactions.
        """
        self.ledger: Ledger = ledger


    def build() -> any:
        """
        Build a new ledger object.

        Returns: The built ledger object.
        """
        pass
