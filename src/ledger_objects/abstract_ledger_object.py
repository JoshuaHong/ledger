from enum import StrEnum


class AbstractLedgerObject:
    """
    An abstract ledger object.
    """

    class Key(StrEnum):
        """
        The keys required in a ledger JSON.
        """
        pass


    def get(self, key: Key) -> any:
        """
        Returns the entry with the given key, or None if the key is not found.

        Parameters:
            key: A key associated to the entry to search.

        Returns: The entry with the given key, or None if the key is not found.
        """
        pass
