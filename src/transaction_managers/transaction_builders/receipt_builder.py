import shutil
import sys

from pathlib import Path
from typing import Optional

import helpers.selector as selector

from .abstract_transaction_builder import AbstractTransactionBuilder

from transaction_managers.abstract_transaction_manager \
        import AbstractTransactionManager
from ledger_objects.ledger import Ledger
from ledger_objects.transaction import Transaction


class ReceiptBuilder(AbstractTransactionBuilder):
    """
    Terminal user interface to build a receipt.
    """

    MAX_RESULTS: int = 1000
    RECEIPT_FILETYPES: list[str] = ["*.jpg", "*.pdf", "*.png"]


    def __init__(self, ledger: Ledger, receipts_directory: Path,
                 search_directory: Optional[Path] = Path.home()) -> None:
        """
        Initializes the item builder.

        Parameters:
            ledger: A ledger containing a list of transactions.
            receipts_directory: A directory containing receipts.
            search_directory: An optional directory in which to search for
                    receipts.
        """
        super().__init__(ledger)
        self.receipts_directory: Path = receipts_directory
        self.search_directory: Path = search_directory
        self.receipt_files: list[str] = list()


    def build(self, prefill_receipt: Optional[str] = None) -> Path:
        """
        Build a receipt.

        Parameters:
            prefill_receipt: An optional receipt to use as the prefill text.

        Returns: The built receipt.
        """
        while True:
            receipt: Path = Path(super().input_handler(Transaction.Key.RECEIPT,
                    prefill_receipt,
                    list_command=(self._list_receipts, [], dict()),
                    search_command=(self._search_receipts, [], dict())))
            if (receipt == AbstractTransactionManager.NO_RECEIPT):
                return receipt
            elif (not receipt.is_file()):
                print("\tError: File does not exist. Please enter the full " \
                        + "path, or \"" \
                        + str(AbstractTransactionManager.NO_RECEIPT) + "\".",
                      file=sys.stderr)
            elif (not receipt.suffix):
                print("\tError: Please enter a valid receipt file:",
                      ReceiptBuilder.RECEIPT_FILETYPES, file=sys.stderr)
            else:
                return receipt


    def copy(self, receipt) -> Path:
        """
        Copies the receipt to the receipts directory.

        Returns: The new receipt path.
        """
        if (receipt == AbstractTransactionManager.NO_RECEIPT):
            return AbstractTransactionManager.NO_RECEIPT
        new_receipt: Path = self._get_new_receipt(receipt.suffix)
        shutil.copy2(str(receipt),
                     self.receipts_directory.joinpath(new_receipt))
        return new_receipt


    def _get_new_receipt(self, suffix: str) -> Path:
        """
        Search the receipts directory for the next incremental receipt name, and
        return it.

        Parameters:
            suffix: A suffix of the new receipt name.

        Returns: The new receipt path.
        """
        previous_receipts: list[str] = sorted([receipt.stem for receipt in \
                Path(self.receipts_directory).iterdir() if receipt.is_file()])
        for i in range(len(previous_receipts)):
            if previous_receipts[i] != str(i):
                return Path(str(i)).with_suffix(suffix)
        return Path(str(len(previous_receipts))).with_suffix(suffix)


    def _list_receipts(self) -> None:
        """
        List all potential receipts in the search directory.
        """
        selector.display(
                self._find_receipt_files()[:ReceiptBuilder.MAX_RESULTS],
                are_duplicates_hidden=True)


    def _search_receipts(self) -> str:
        """
        Serach all potential receipts in the search directory.

        Returns: The search result to use as the prefill text.
        """
        return selector.search(
                self._find_receipt_files()[:ReceiptBuilder.MAX_RESULTS],
                are_duplicates_hidden=True, is_reversed=True, prompt="Search :")


    def _find_receipt_files(self) -> list[str]:
        """
        Find all potential receipts in the search directory and return it.

        Returns: The list of potential receipts.
        """
        receipt_files = list()
        for filetype in ReceiptBuilder.RECEIPT_FILETYPES:
            receipt_files.extend(self.search_directory.glob(filetype))
        self.receipt_files = \
                [str(receipt_file) for receipt_file in receipt_files]
        return self.receipt_files
