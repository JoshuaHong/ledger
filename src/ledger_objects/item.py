from .abstract_ledger_object import AbstractLedgerObject


class Item(AbstractLedgerObject):
    """
    An object containing the item data.
    """

    def __init__(self, name: str, price: float, quantity: int,
                 tags: list[str]) -> None:
        """
        Initializes an item.
        """
        self.name: str = name
        self.price: float = price
        self.quantity: int = quantity
        self.tags: list[str] = tags


    class Key(AbstractLedgerObject.Key):
        """
        The keys required in an item JSON.
        """
        NAME: str = "name"
        PRICE: str = "price"
        QUANTITY: str = "quantity"
        TAGS: str = "tags"


    def get(self, key: Key) -> any:
        """
        Returns the entry with the given key, or None if the key is not found.

        Parameters:
            key: A key associated to the entry to search.

        Returns: The entry with the given key, or None if the key is not found.
        """
        match key:
            case Item.Key.NAME:
                return self.get_name()
            case Item.Key.PRICE:
                return self.get_price()
            case Item.Key.QUANTITY:
                return self.get_quantity()
            case Item.Key.TAGS:
                return self.get_tags()
            case _:
                return None


    def get_formatted_string(self) -> str:
        """
        Returns the formatted item string.

        Returns: The formatted item string.
        """
        return self.get_name() + (", -$" if self.get_price() < 0 else ", $") \
               + str(abs(self.get_price())) + ", x" + str(self.get_quantity()) \
               + ", Tags: ['" + "', '".join(map(str, self.get_tags())) + "']"


    def get_name(self) -> str:
        """
        Returns the item name.

        Returns: The item name.
        """
        return self.name


    def get_price(self) -> float:
        """
        Returns the item price.

        Returns: The item price.
        """
        return self.price


    def get_quantity(self) -> int:
        """
        Returns the item quantity.

        Returns: The item quantity.
        """
        return self.quantity


    def get_tags(self) -> list[str]:
        """
        Returns the item tags.

        Returns: The item tags.
        """
        return self.tags


    def set_name(self, name: str) -> None:
        """
        Sets the item name.

        Parameters:
            name: The item name to set.
        """
        self.name = name


    def set_price(self, price: float) -> None:
        """
        Sets the item price.

        Parameters:
            price: The item price to set.
        """
        self.price = price


    def set_quantity(self, quantity: int) -> None:
        """
        Sets the item quantity.

        Parameters:
            quantity: The item quantity to set.
        """
        self.quantity = quantity


    def set_tags(self, tags: list[str]) -> None:
        """
        Sets the item tags.

        Parameters:
            tags: The item tags to set.
        """
        self.tags = tags


    def add_tag(self, tag: str) -> None:
        """
        Adds a new item tag to the list.

        Parameters:
            tag: The item tag to add.
        """
        self.tags.append(tag)


    def remove_tag(self, tag: str) -> None:
        """
        Removes the item tag provided if it exists. Does nothing otherwise.

        Parameters:
            tag: The item tag to remove.
        """
        if (tag in self.tags):
            self.tags.remove(tag)


    def clear_tags(self) -> None:
        """
        Clears all tags from the list.
        """
        self.tags.clear()
