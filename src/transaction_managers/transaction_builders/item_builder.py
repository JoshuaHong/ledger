import sys

from typing import Optional

import helpers.selector as selector

from .abstract_transaction_builder import AbstractTransactionBuilder

from ledger_objects.abstract_ledger_object import AbstractLedgerObject
from transaction_managers.abstract_transaction_manager \
        import AbstractTransactionManager
from ledger_objects.item import Item
from ledger_objects.ledger import Ledger


class ItemBuilder(AbstractTransactionBuilder):
    """
    Terminal user interface to build an item.
    """

    STEP: list[AbstractLedgerObject.Key] = [
            Item.Key.NAME, Item.Key.PRICE, Item.Key.QUANTITY, Item.Key.TAGS]


    def __init__(self, ledger: Ledger) -> None:
        """
        Initializes the item builder.

        Parameters:
            ledger: A ledger containing a list of transactions.
        """
        super().__init__(ledger)
        self.item: Optional[Item] = None
        self.name: Optional[str] = None
        self.price: Optional[float] = None
        self.quantity: Optional[int] = None
        self.tags: list[str] = list()
        self.current_step: int = 0


    def build(self, prefill_item: Optional[Item] = None) -> Item:
        """
        Build an item.

        Parameters:
            prefill_items: An optional item to use as the prefill text.

        Returns: The built item.
        """
        self._reset()
        while True:
            if (self.current_step == len(ItemBuilder.STEP)):
                return Item(self.name, self.price, self.quantity, self.tags)
            try:
                match ItemBuilder.STEP[self.current_step]:
                    case Item.Key.NAME:
                        self.name = self.build_name(self.name \
                                or (prefill_item.get_name() if prefill_item \
                                else ""))
                    case Item.Key.PRICE:
                        self.price = self.build_price(str(self.price) \
                                if self.price is not None \
                                else (prefill_item.get_price() if prefill_item \
                                else ""))
                    case Item.Key.QUANTITY:
                        self.quantity = self.build_quantity(str(self.quantity) \
                                if self.quantity is not None \
                                else (prefill_item.get_quantity() \
                                if prefill_item else ""))
                    case Item.Key.TAGS:
                        self.tags = self.build_tags(self.tags \
                                or (prefill_item.get_tags() if prefill_item \
                                else list()))
                self.current_step += 1
            except (AbstractTransactionManager.Navigation.Back):
                match ItemBuilder.STEP[self.current_step]:
                    case Item.Key.NAME:
                        super().navigate_back()
                self.current_step -= 1


    def build_name(self, prefill_name: Optional[str] = "") -> str:
        """
        Build a name and return it.

        Parameters:
            prefill_name: An optional name to use as the prefill text.

        Returns: The built name.
        """
        name: str = super().input_handler(Item.Key.NAME, prefill_name)
        return name


    def build_price(self, prefill_price: Optional[str] = None) -> float:
        """
        Build a price and return it.

        Parameters:
            prefill_price: An optional price to use as the prefill text.

        Returns: The built price.
        """
        while True:
            try:
                price: float = float(super().input_handler(Item.Key.PRICE,
                        abs(float(prefill_price)) if prefill_price else "",
                        can_list_and_search=False))
            except (ValueError):
                print("\tError: Please enter a positive number.",
                    file=sys.stderr)
            else:
                if (price <= 0):
                    print("\tError: Please enter a positive number.",
                        file=sys.stderr)
                else:
                    break
        prefill_sign: str = "" if not prefill_price else \
                ("g" if prefill_price > 0 else "l")
        price *= -1 if not selector.get_binary_input(
                "Is this a gain or a loss? (g/l): ", "g", "l",
                prefill_sign) else 1
        return price


    def build_quantity(self, prefill_quantity: Optional[str] = None) -> int:
        """
        Build a quantity and return it.

        Parameters:
            prefill_quantity: An optional quantity to use as the prefill text.

        Returns: The built quantity.
        """
        while True:
            try:
                quantity: int = int(super().input_handler(Item.Key.QUANTITY,
                        prefill_quantity, can_list_and_search=False))
            except (ValueError):
                print("\tError: Please enter a positive integer.",
                      file=sys.stderr)
            else:
                if (quantity <= 0):
                    print("\tError: Please enter a positive integer.",
                        file=sys.stderr)
                else:
                    break
        return quantity


    def build_tags(self,
                    prefill_tags: Optional[list[str]] = list()) -> list[str]:
        """
        Build tags and return it.

        Parameters:
            prefill_tags: An optional list of tags to use as the prefill text.

        Returns: The built tags.
        """
        tags: list[str] = prefill_tags
        current_tag_step: int = 0
        while True:
            try:
                if (current_tag_step < len(tags)):
                    tags[current_tag_step] = super().input_handler(
                        Item.Key.TAGS, tags[current_tag_step])
                else:
                    tags.append(super().input_handler(Item.Key.TAGS))
            except (AbstractTransactionManager.Navigation.Back):
                if (current_tag_step):
                    current_tag_step -= 1
                    continue
                else:
                    super().navigate_back()
            current_tag_step += 1
            if (not selector.get_binary_input("Add another tag? (y/n): ")):
                tags = tags[:current_tag_step]
                break
        return tags


    def _reset(self) -> None:
        """
        Reset the item builder.
        """
        self.item = None
        self.name = None
        self.price = None
        self.quantity = None
        self.tags = list()
        self.current_step = 0
