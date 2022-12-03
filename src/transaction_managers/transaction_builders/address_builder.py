from typing import Optional

import helpers.selector as selector

from .abstract_transaction_builder import AbstractTransactionBuilder

from ledger_objects.abstract_ledger_object import AbstractLedgerObject
from transaction_managers.abstract_transaction_manager \
        import AbstractTransactionManager
from ledger_objects.address import Address
from ledger_objects.ledger import Ledger
from ledger_objects.transaction import Transaction


class AddressBuilder(AbstractTransactionBuilder):
    """
    Terminal user interface to build an address.
    """

    STEP: list[AbstractLedgerObject.Key] = [
            Address.Key.NAME, Address.Key.STREET, Address.Key.CITY,
            Address.Key.PROVINCE, Address.Key.POSTAL_CODE, Address.Key.COUNTRY]
    URL_PREFIXES: list[str] = ["http://", "https://", "www."]


    def __init__(self, ledger: Ledger) -> None:
        """
        Initializes the address builder.

        Parameters:
            ledger: A ledger containing a list of transactions.
        """
        super().__init__(ledger)
        self.name: Optional[str] = None
        self.street: Optional[str] = None
        self.city: Optional[str] = None
        self.province: Optional[str] = None
        self.postal_code: Optional[str] = None
        self.country: Optional[str] = None
        self.current_step: int = 0


    def build(self, prefill_address: Optional[Address] = None) -> Address:
        """
        Build an address.

        Parameters:
            prefill_address: An optional address to use as the prefill text.

        Returns: The built address.
        """
        self._reset()
        latest_address: Optional[Address] = self._get_latest_address()
        while True:
            if (self.current_step == len(AddressBuilder.STEP)):
                return Address(self.city, self.country, self.name,
                               self.postal_code, self.province, self.street)
            try:
                match AddressBuilder.STEP[self.current_step]:
                    case Address.Key.NAME:
                        self.name = self.build_name(self.name \
                                or (prefill_address.get_name() \
                                if prefill_address else ""))
                        if (self._is_url(self.name)):
                            self._prefill_no_address()
                    case Address.Key.STREET:
                        self.street = self.build_street(self.street \
                                or (prefill_address.get_street() \
                                if prefill_address else ""))
                    case Address.Key.CITY:
                        self.city = self.build_city(self.city \
                                or (prefill_address.get_city() \
                                if prefill_address \
                                else (latest_address.get_city() \
                                if latest_address else "")))
                    case Address.Key.PROVINCE:
                        self.province = self.build_province(self.province \
                                or (prefill_address.get_province() \
                                if prefill_address \
                                else (latest_address.get_province() \
                                if latest_address else "")))
                    case Address.Key.POSTAL_CODE:
                        self.postal_code = self.build_postal_code(
                                self.postal_code \
                                or (prefill_address.get_postal_code() \
                                if prefill_address \
                                else (latest_address.get_postal_code() \
                                if latest_address else "")))
                    case Address.Key.COUNTRY:
                        self.country = self.build_country(self.country \
                                or (prefill_address.get_country() \
                                if prefill_address \
                                else (latest_address.get_country() \
                                if latest_address else "")))
                self.current_step += 1
            except (AbstractTransactionManager.Navigation.Back):
                match AddressBuilder.STEP[self.current_step]:
                    case Address.Key.NAME:
                        super().navigate_back()
                self.current_step -= 1


    def build_name(self, prefill_name: Optional[str] = "") -> str:
        """
        Build a name and return it.

        Parameters:
            prefill_name: An optional name to use as the prefill text.

        Returns: The built name.
        """
        previous_addresses: list[Address] = super().get_all(
                Transaction.Key.ADDRESS)
        formatted_address_pairs: list[(str, Address)] = [(
                address.get_formatted_string(), address)
                for address in previous_addresses]
        formatted_addresses: list[str] = [address[0] for address
                                          in formatted_address_pairs]
        return super().input_handler(Address.Key.NAME, prefill_name,
                list_command=(selector.display, [formatted_addresses],
                    {"are_duplicates_hidden": True}),
                search_command=(self._search_addresses,
                    [formatted_address_pairs], dict()))


    def build_street(self, prefill_street: Optional[str] = "") -> str:
        """
        Build a street and return it.

        Parameters:
            prefill_street: An optional street to use as the prefill text.

        Returns: The built street.
        """
        street: str = super().input_handler(Address.Key.STREET, prefill_street)
        return street


    def build_city(self, prefill_city: Optional[str] = "") -> str:
        """
        Build a city and return it.

        Parameters:
            prefill_city: An optional city to use as the prefill text.

        Returns: The built city.
        """
        city: str = super().input_handler(Address.Key.CITY, prefill_city)
        return city


    def build_province(self, prefill_province: Optional[str] = "") -> str:
        """
        Build a province and return it.

        Parameters:
            prefill_province: An optional province to use as the prefill text.

        Returns: The built province.
        """
        province: str = super().input_handler(Address.Key.PROVINCE,
                                              prefill_province)
        return province


    def build_postal_code(self, prefill_postal_code: Optional[str] = "") -> str:
        """
        Build a postal_code and return it.

        Parameters:
            prefill_postal_code: An optional postal_code to use as the prefill
                                 text.

        Returns: The built postal_code.
        """
        postal_code: str = super().input_handler(Address.Key.POSTAL_CODE,
                                                 prefill_postal_code)
        return postal_code


    def build_country(self, prefill_country: Optional[str] = "") -> str:
        """
        Build a country and return it.

        Parameters:
            prefill_country: An optional country to use as the prefill text.

        Returns: The built country.
        """
        country: str = super().input_handler(Address.Key.COUNTRY,
                                             prefill_country)
        return country


    def _search_addresses(self, addresses: list[(str, Address)]) -> str:
        """
        Search through a list of previous addresses and prefills the input text
        to the selected address name. Sets the current address fields to the
        search result address to prefill the remaining address fields.

        Parameters:
            addresses: A list of pairs containing the string representing the
                       full comma-separated address and the Address itself.

        Returns: The search result to use as the prefill text.
        """
        formatted_addresses: list[str] = [address[0] for address in addresses]
        formatted_address: str = selector.search(formatted_addresses,
                are_duplicates_hidden=True, is_reversed=True, prompt="Search: ")
        try:
            index: int = [a[0] for a in addresses].index(formatted_address)
            address: Address = addresses[index][1]
            self.name = address.get_name()
            self.street = address.get_street()
            self.city = address.get_city()
            self.province = address.get_province()
            self.postal_code = address.get_postal_code()
            self.country = address.get_country()
            return self.name
        except (ValueError):
            return ""


    def _get_latest_address(self) -> Optional[Address]:
        """
        Returns the latest transaction's address if it exists.

        Returns: The latest transaction's address.
        """
        latest_address: Optional[Address] = None
        transactions: list[transactions] = self.ledger.get_transactions()
        if (transactions):
            latest_transaction: Transaction = transactions[-1]
            latest_address = latest_transaction.get_address()
            return latest_address 
        else:
            return None


    def _is_url(self, name: str) -> bool:
        """
        Returns true if the name is a standard URL, false otherwise.

        Parameters:
            name: The name of the string to check if it is a URL.

        Returns: A boolean denoting whether the name is a URL.
        """
        for url_prefix in AddressBuilder.URL_PREFIXES:
            if (name.startswith(url_prefix)):
                return True
        return False


    def _prefill_no_address(self) -> None:
        """
        Prefills the remaining address fields with "N/A".
        """
        self.street = "N/A"
        self.city = "N/A"
        self.province = "N/A"
        self.postal_code = "N/A"
        self.country = "N/A"


    def _reset(self) -> None:
        """
        Reset the item builder.
        """
        self.name = None
        self.street = None
        self.city = None
        self.province = None
        self.postal_code = None
        self.country = None
        self.current_step = 0
