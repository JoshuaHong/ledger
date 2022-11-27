from pathlib import Path
from zoneinfo import ZoneInfo

from ledger_objects.address import Address
from ledger_objects.item import Item
from ledger_objects.ledger import Ledger
from ledger_objects.timestamp import Timestamp
from ledger_objects.transaction import Transaction


def parse_ledger_json(ledger_json: dict[str, any]) -> Ledger:
    """
    Parses a ledger JSON and returns a ledger.
    Throws an error if the keys don't exist.

    Parameters:
        ledger: A JSON containing a ledger to parse.

    Returns: The parsed ledger.
    """
    transactions: list[Transaction] = list()
    for transaction_json in ledger_json[Ledger.Key.TRANSACTIONS]:
        transactions.append(parse_transaction_json(transaction_json))
    return Ledger(transactions)


def parse_transaction_json(transaction_json: dict[str, any]) -> Transaction:
    """
    Parses a transaction JSON and returns a transaction.
    Throws an error if the keys don't exist.

    Parameters:
        transaction_json: A JSON containing the transaction to parse.

    Returns: The parsed transaction.
    """
    address: Address = parse_address_json(
            transaction_json[Transaction.Key.ADDRESS])
    description: str = transaction_json[Transaction.Key.DESCRIPTION]
    items: list[Item] = [parse_item_json(item_json) for item_json
                         in transaction_json[Transaction.Key.ITEMS]]
    payment_method: str = transaction_json[Transaction.Key.PAYMENT_METHOD]
    receipt: Path = Path(transaction_json[Transaction.Key.RECEIPT])
    timestamp: Timestamp = parse_timestamp_json(
            transaction_json[Transaction.Key.TIMESTAMP])
    return Transaction(address, description, items, payment_method, receipt,
                       timestamp)


def parse_address_json(address_json: dict[str, any]) -> Address:
    """
    Parses an address JSON and returns an item.
    Throws an error if the keys don't exist.

    Parameters:
        address_json: A dictionary of the address to parse.

    Returns: The parsed address.
    """
    city: str = address_json[Address.Key.CITY]
    country: str = address_json[Address.Key.COUNTRY]
    name: str = address_json[Address.Key.NAME]
    postal_code: str = address_json[Address.Key.POSTAL_CODE]
    province: str = address_json[Address.Key.PROVINCE]
    street: str = address_json[Address.Key.STREET]
    return Address(city, country, name, postal_code, province, street)


def parse_item_json(item_json: dict[str, any]) -> Item:
    """
    Parses an item JSON and returns an item.
    Throws an error if the keys don't exist.

    Parameters:
        item_json: A dictionary of the item to parse.

    Returns: The parsed item.
    """
    name: str = item_json[Item.Key.NAME]
    price: float = item_json[Item.Key.PRICE]
    quantity: float = item_json[Item.Key.QUANTITY]
    tags: list[str] = item_json[Item.Key.TAGS]
    return Item(name, price, quantity, tags)


def parse_timestamp_json(timestamp_json: dict[str, any]) -> Timestamp:
    """
    Parses a timestamp JSON and returns a timestamp.
    Throws an error if the keys don't exist.

    Parameters:
        timestamp_json: A dictionary of the timestamp to parse.

    Returns: The parsed timestamp.
    """
    timestamp: int = timestamp_json[Timestamp.Key.TIMESTAMP]
    timezone: ZoneInfo = ZoneInfo(timestamp_json[Timestamp.Key.TIMEZONE])
    return Timestamp(timestamp, timezone)
