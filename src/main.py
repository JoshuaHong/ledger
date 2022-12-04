#!/usr/bin/python
#
# Terminal user interface to manage transactions in the ledger.

from argparse import ArgumentParser, FileType
from pathlib import Path

from transaction_managers.transaction_manager import TransactionManager


def main() -> None:
    args: dict[str, any] = parse_arguments()
    ledger_file: Path = Path(args.ledger_file)
    receipts_directory: Path = Path(args.receipts_directory)
    is_new_file: bool = bool(args.new_file)
    search_directory: Path = Path(args.search_directory or Path.home())
    transaction_manager: TransactionManager = TransactionManager(
            ledger_file, receipts_directory, is_new_file, search_directory)
    transaction_manager.main_menu()


def parse_arguments() -> dict[str, any]:
    """
    Parses the program's command-line arguments.

    Returns:
        The program's parsed command-line arguments.
    """
    parser: ArgumentParser = ArgumentParser(
            description="Manage transactions in the ledger.")
    parser.add_argument("-n", "--new_file", action="store_true",
            help="Create a new ledger file.")
    parser.add_argument("ledger_file",
            help="The ledger file containing the transactions in JSON format.")
    parser.add_argument("receipts_directory",
            help="The directory containing the receipts.")
    parser.add_argument("-s", "--search-directory", type=Path,
            help="The directory in which to search for receipts recursively.")
    return parser.parse_args()


if __name__ == '__main__':
    main()
