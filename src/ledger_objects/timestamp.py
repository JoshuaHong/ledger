import datetime

from typing import Optional
from zoneinfo import ZoneInfo

from .abstract_ledger_object import AbstractLedgerObject


class Timestamp(AbstractLedgerObject):
    """
    An object containing the timestamp data.
    """

    def __init__(self, timestamp: int,
                 timezone: Optional[ZoneInfo] = datetime.timezone.utc) -> None:
        """
        Initializes a timestamp.
        """
        self.timestamp: datetime.datetime = datetime.datetime.fromtimestamp(
                timestamp, tz=timezone)


    class Key(AbstractLedgerObject.Key):
        """
        The keys required in a timestamp JSON.
        """
        TIMESTAMP: str = "timestamp"
        TIMEZONE: ZoneInfo = "timezone"
        # Additional keys required for the timestamp builder.
        YEAR: str = "year"
        MONTH: str = "month"
        DAY: str = "day"
        HOUR: str = "hour"
        MINUTE: str = "minute"
        SECOND: str = "second"


    def get(self, key: Key) -> any:
        """
        Returns the entry with the given key, or None if the key is not found.

        Parameters:
            key: A key associated to the entry to search.

        Returns: The entry with the given key, or None if the key is not found.
        """
        match key:
            case Timestamp.Key.TIMESTAMP:
                return self.get_timestamp()
            case Timestamp.Key.YEAR:
                return self.get_year()
            case Timestamp.Key.MONTH:
                return self.get_month()
            case Timestamp.Key.DAY:
                return self.get_day()
            case Timestamp.Key.HOUR:
                return self.get_hour()
            case Timestamp.Key.MINUTE:
                return self.get_minute()
            case Timestamp.Key.SECOND:
                return self.get_second()
            case Timestamp.Key.TIMEZONE:
                return self.get_timezone()
            case _:
                return None


    def get_formatted_string(self) -> str:
        """
        Returns the formatted timestamp string.

        Returns: The formatted timestamp string.
        """
        return self.timestamp.strftime("%c %Z")


    def get_timestamp(self) -> int:
        """
        Returns the timestamp in Unix time.

        Returns: The timestamp in Unix time.
        """
        return self.timestamp.timestamp()


    def get_year(self) -> int:
        """
        Returns the timestamp year.

        Returns: The timestamp year
        """
        return self.timestamp.year


    def get_month(self) -> int:
        """
        Returns the timestamp month.

        Returns: The timestamp month
        """
        return self.timestamp.month


    def get_day(self) -> int:
        """
        Returns the timestamp day.

        Returns: The timestamp day
        """
        return self.timestamp.day


    def get_hour(self) -> int:
        """
        Returns the timestamp hour.

        Returns: The timestamp hour
        """
        return self.timestamp.hour


    def get_minute(self) -> int:
        """
        Returns the timestamp minute.

        Returns: The timestamp minute
        """
        return self.timestamp.minute


    def get_second(self) -> int:
        """
        Returns the timestamp second.

        Returns: The timestamp second
        """
        return self.timestamp.second


    def get_timezone(self) -> ZoneInfo:
        """
        Returns the timestamp timezone.

        Returns: The timestamp timezone
        """
        return self.timestamp.tzinfo


    def set_timestamp(self, timestamp: int) -> None:
        """
        Sets the timestamp in Unix time.

        Parameters:
            timestamp: The timestamp to set.
        """
        self.timestamp = datetime.datetime.fromtimestamp(timestamp)


    def set_year(self, year: int) -> None:
        """
        Sets the timestamp year.

        Parameters:
            timestamp: The timestamp year to set.
        """
        self.timestamp = self.timestamp.replace(year=year)


    def set_month(self, month: int) -> None:
        """
        Sets the timestamp month.

        Parameters:
            timestamp: The timestamp month to set.
        """
        self.timestamp = self.timestamp.replace(month=month)


    def set_day(self, day: int) -> None:
        """
        Sets the timestamp day.

        Parameters:
            timestamp: The timestamp day to set.
        """
        self.timestamp = self.timestamp.replace(day=day)


    def set_hour(self, hour: int) -> None:
        """
        Sets the timestamp hour.

        Parameters:
            timestamp: The timestamp hour to set.
        """
        self.timestamp = self.timestamp.replace(hour=hour)


    def set_minute(self, minute: int) -> None:
        """
        Sets the timestamp minute.

        Parameters:
            timestamp: The timestamp minute to set.
        """
        self.timestamp = self.timestamp.replace(minute=minute)


    def set_second(self, second: int) -> None:
        """
        Sets the timestamp second.

        Parameters:
            timestamp: The timestamp second to set.
        """
        self.timestamp = self.timestamp.replace(second=second)


    def set_timezone(self, timezone: ZoneInfo) -> None:
        """
        Sets the timestamp timezone.

        Parameters:
            timestamp: The timestamp timezone to set.
        """
        self.timestamp = self.timestamp.replace(tzinfo=timezone)
