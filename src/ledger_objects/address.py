from .abstract_ledger_object import AbstractLedgerObject


class Address(AbstractLedgerObject):
    """
    An object containing the address data.
    """

    def __init__(self, city: str, country: str, name: str, postal_code: str, 
                 province: str, street: str) -> None:
        """
        Initializes a address.
        """
        self.city: str = city
        self.country: str = country
        self.name: str = name
        self.postal_code: str = postal_code
        self.province: str = province
        self.street: str = street


    class Key(AbstractLedgerObject.Key):
        """
        The keys required in an address JSON.
        """
        CITY: str = "city"
        COUNTRY: str = "country"
        NAME: str = "name"
        POSTAL_CODE: str = "postal code"
        PROVINCE: str = "province"
        STREET: str = "street"


    def get(self, key: Key) -> any:
        """
        Returns the entry with the given key, or None if the key is not found.

        Parameters:
            key: A key associated to the entry to search.

        Returns: The entry with the given key, or None if the key is not found.
        """
        match key:
            case Address.Key.CITY:
                return self.get_city()
            case Address.Key.COUNTRY:
                return self.get_country()
            case Address.Key.NAME:
                return self.get_name()
            case Address.Key.POSTAL_CODE:
                return self.get_postal_code()
            case Address.Key.PROVINCE:
                return self.get_province()
            case Address.Key.STREET:
                return self.get_street()
            case _:
                return None


    def get_formatted_string(self) -> str:
        """
        Returns the formatted address string.

        Returns: The formatted address string.
        """
        return self.get_name() + ", " + self.get_street() + ", " \
                + self.get_city() + ", " + self.get_province() + ", " \
                + self.get_postal_code() + ", " + self.get_country()


    def get_city(self) -> str:
        """
        Returns the address city.

        Returns: The address city.
        """
        return self.city


    def get_country(self) -> str:
        """
        Returns the address country.

        Returns: The address country.
        """
        return self.country


    def get_name(self) -> str:
        """
        Returns the address name.

        Returns: The address name.
        """
        return self.name


    def get_postal_code(self) -> str:
        """
        Returns the address postal code.

        Returns: The address postal code.
        """
        return self.postal_code


    def get_province(self) -> str:
        """
        Returns the address province.

        Returns: The address province.
        """
        return self.province


    def get_street(self) -> str:
        """
        Returns the address street.

        Returns: The address street.
        """
        return self.street


    def set_city(self, city: str) -> None:
        """
        Sets the address city.

        Parameters:
            city: The address city to set.
        """
        self.city = city


    def set_country(self, country: str) -> None:
        """
        Sets the address country.

        Parameters:
            country: The address country to set.
        """
        self.country = country


    def set_name(self, name: str) -> None:
        """
        Sets the address name.

        Parameters:
            name: The address name to set.
        """
        self.name = name


    def set_postal_code(self, postal_code: str) -> None:
        """
        Sets the address postal code.

        Parameters:
            postal_code: The address postal code to set.
        """
        self.postal_code = postal_code


    def set_province(self, province: str) -> None:
        """
        Sets the address province.

        Parameters:
            province: The address province to set.
        """
        self.province = province


    def set_street(self, street: str) -> None:
        """
        Sets the address street.

        Parameters:
            street: The address street to set.
        """
        self.street = street
