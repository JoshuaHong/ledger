from ledger_objects.address import Address
from ledger_objects.item import Item
from ledger_objects.ledger import Ledger
from ledger_objects.timestamp import Timestamp
from ledger_objects.transaction import Transaction


def build_ledger_json(ledger: Ledger) -> dict[str, any]:
    """
    Build a ledger JSON and return it.

    Parameters:
        ledger: A ledger to build into a JSON.

    Returns: The built ledger JSON.
    """
    transaction_jsons = list()
    for transaction in ledger.get_transactions():
        transaction_jsons.append(build_transaction_json(transaction))
    return dict(transactions = transaction_jsons)


def build_transaction_json(transaction: Transaction) -> dict[str, any]:
    """
    Build a transaction JSON and return it.

    Parameters:
        transaction: A transaction to build into a JSON.

    Returns: The built transaction JSON.
    """
    address_json: dict[str, any] = build_address_json(transaction.get_address())
    description: str = transaction.get_description()
    item_jsons: list[dict[str, any]] =  [build_item_json(item) for item \
            in transaction.get_items()]
    payment_method: str = transaction.get_payment_method()
    receipt: str = str(transaction.get_receipt())
    timestamp_json: dict[str, any] = build_timestamp_json(
            transaction.get_timestamp())
    return {"address": address_json, "description": description,
            "items": item_jsons, "payment method": payment_method,
            "receipt": receipt, "timestamp": timestamp_json}


def build_address_json(address: Address) -> dict[str, any]:
    """
    Build an address JSON and return it.

    Parameters:
        address: An address to build into a JSON.

    Returns: The built address JSON.
    """
    city: str = address.get_city()
    country: str = address.get_country()
    name: str = address.get_name()
    postal_code: str = address.get_postal_code()
    province: str = address.get_province()
    street: str = address.get_street()
    return {"city": city, "country": country, "name": name,
            "postal code": postal_code, "province": province, "street": street}


def build_item_json(item: Item) -> dict[str, any]:
    """
    Build an item JSON and return it.

    Parameters:
        item: An item to build into a JSON.

    Returns: The built item JSON.
    """
    name: str = item.get_name()
    price: float = item.get_price()
    quantity: int = item.get_quantity()
    tags: list[str] = item.get_tags()
    return {"name": name, "price": price, "quantity": quantity, "tags": tags}


def build_timestamp_json(timestamp: Timestamp) -> dict[str, any]:
    """
    Build a timestamp JSON and return it.

    Parameters:
        timestamp: A timestamp to build into a JSON.

    Returns: The built timestamp JSON.
    """
    unix_timestamp: int = timestamp.get_timestamp()
    timezone: str = str(timestamp.get_timezone())
    return {"timestamp": unix_timestamp, "timezone": timezone}
