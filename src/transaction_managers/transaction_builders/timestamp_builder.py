import datetime
import sys
import zoneinfo

from typing import Optional

import helpers.selector as selector

from .abstract_transaction_builder import AbstractTransactionBuilder

from ledger_objects.abstract_ledger_object import AbstractLedgerObject
from transaction_managers.abstract_transaction_manager \
        import AbstractTransactionManager
from ledger_objects.ledger import Ledger
from ledger_objects.timestamp import Timestamp


class TimestampBuilder(AbstractTransactionBuilder):
    """
    Terminal user interface to build a timestamp.
    """

    STEP: list[AbstractLedgerObject.Key] = [Timestamp.Key.YEAR,
            Timestamp.Key.MONTH, Timestamp.Key.DAY, Timestamp.Key.HOUR,
            Timestamp.Key.MINUTE, Timestamp.Key.SECOND, Timestamp.Key.TIMEZONE]


    def __init__(self, ledger: Ledger) -> None:
        """
        Initializes the timestamp builder.

        Parameters:
            ledger: A ledger containing a list of transactions.
        """
        super().__init__(ledger)
        self.year: Optional[int] = None
        self.month: Optional[int] = None
        self.day: Optional[int] = None
        self.hour: Optional[int] = None
        self.minute: Optional[int] = None
        self.second: Optional[int] = None
        self.timezone: Optional[zoneinfo.ZoneInfo] = None
        self.current_step: int = 0


    def build(self, prefill_timestamp: Optional[Timestamp] = None) -> Timestamp:
        """
        Build a timestamp.

        Parameters:
            prefill_timestamp: An optional timestamp to use as the prefill text.

        Returns: The built timestamp.
        """
        self._reset()
        timestamp_now: Timestamp = self._get_timestamp_now()
        while True:
            if (self.current_step == len(TimestampBuilder.STEP)):
                timestamp: datetime.datetime = datetime.datetime(self.year,
                        self.month, self.day, self.hour, self.minute,
                        self.second, tzinfo=self.timezone)
                return Timestamp(timestamp.timestamp(), self.timezone)
            try:
                match TimestampBuilder.STEP[self.current_step]:
                    case Timestamp.Key.YEAR:
                        self.year = self.build_year(str(self.year) \
                                if self.year is not None \
                                else (prefill_timestamp.get_year() \
                                if prefill_timestamp \
                                else timestamp_now.get_year()))
                    case Timestamp.Key.MONTH:
                        self.month = self.build_month(str(self.month) \
                                if self.month is not None \
                                else (prefill_timestamp.get_month() \
                                if prefill_timestamp \
                                else timestamp_now.get_month()))
                    case Timestamp.Key.DAY:
                        self.day = self.build_day(str(self.day) \
                                if self.day is not None \
                                else (prefill_timestamp.get_day() \
                                if prefill_timestamp \
                                else timestamp_now.get_day()))
                    case Timestamp.Key.HOUR:
                        self.hour = self.build_hour(str(self.hour) \
                                if self.hour is not None \
                                else (prefill_timestamp.get_hour() \
                                if prefill_timestamp else ""))
                    case Timestamp.Key.MINUTE:
                        self.minute = self.build_minute(str(self.minute) \
                                if self.minute is not None \
                                else (prefill_timestamp.get_minute() \
                                if prefill_timestamp else ""))
                    case Timestamp.Key.SECOND:
                        self.second = self.build_second(str(self.second) \
                                if self.second is not None \
                                else (prefill_timestamp.get_second() \
                                if prefill_timestamp else ""))
                    case Timestamp.Key.TIMEZONE:
                        self.timezone = self.build_timezone(self.timezone \
                                or (prefill_timestamp.get_timezone() \
                                if prefill_timestamp \
                                else self._get_timestamp_now().get_timezone()))
                self.current_step += 1
            except (AbstractTransactionManager.Navigation.Back):
                match TimestampBuilder.STEP[self.current_step]:
                    case Timestamp.Key.YEAR:
                        super().navigate_back()
                self.current_step -= 1


    def build_year(self, prefill_year: Optional[str]) -> int:
        """
        Build a year and return it.

        Parameters:
            prefill_year: An optional year to use as the prefill text.

        Returns: The built year.
        """
        while True:
            try:
                year: int = int(super().input_handler(Timestamp.Key.YEAR,
                        prefill_year, can_list_and_search=False))
            except (ValueError):
                print("\tError: Please enter a valid year [YYYY].",
                      file=sys.stderr)
            else:
                if (year < 0):
                    print("\tError: Please enter a valid year [YYYY].",
                        file=sys.stderr)
                else:
                    break
        return year


    def build_month(self, prefill_month: Optional[str]) -> int:
        """
        Build a month and return it.

        Parameters:
            prefill_month: An optional month to use as the prefill text.

        Returns: The built month.
        """
        while True:
            try:
                month: int = int(super().input_handler(Timestamp.Key.MONTH,
                        prefill_month, can_list_and_search=False))
            except (ValueError):
                print("\tError: Please enter a valid month [1-12].",
                      file=sys.stderr)
            else:
                if (month < 1 or month > 12):
                    print("\tError: Please enter a valid month [1-12].",
                        file=sys.stderr)
                else:
                    break
        return month


    def build_day(self, prefill_day: Optional[str]) -> int:
        """
        Build a day and return it.

        Parameters:
            prefill_day: An optional day to use as the prefill text.

        Returns: The built day.
        """
        while True:
            try:
                day: int = int(super().input_handler(Timestamp.Key.DAY,
                        prefill_day, can_list_and_search=False))
            except (ValueError):
                print("\tError: Please enter a valid day [1-31].",
                      file=sys.stderr)
            try:
                datetime.datetime(self.year, self.month, day)
            except (ValueError):
                print("\tError: Please enter a valid day in this month.",
                      file=sys.stderr)
            else:
                break
        return day


    def build_hour(self, prefill_hour: Optional[str]) -> int:
        """
        Build a hour and return it.

        Parameters:
            prefill_hour: An optional hour to use as the prefill text.

        Returns: The built hour.
        """
        while True:
            try:
                hour: int = int(super().input_handler(Timestamp.Key.HOUR,
                        prefill_hour, can_list_and_search=False))
            except (ValueError):
                print("\tError: Please enter a valid hour [0-23].",
                      file=sys.stderr)
            else:
                if (hour < 0 or hour > 23):
                    print("\tError: Please enter a valid hour [0-23].",
                        file=sys.stderr)
                else:
                    break
        return hour


    def build_minute(self, prefill_minute: Optional[str]) -> int:
        """
        Build a minute and return it.

        Parameters:
            prefill_minute: An optional minute to use as the prefill text.

        Returns: The built minute.
        """
        while True:
            try:
                minute: int = int(super().input_handler(Timestamp.Key.MINUTE,
                        prefill_minute, can_list_and_search=False))
            except (ValueError):
                print("\tError: Please enter a valid minute [0-59].",
                      file=sys.stderr)
            else:
                if (minute < 0 or minute > 59):
                    print("\tError: Please enter a valid minute [0-59].",
                        file=sys.stderr)
                else:
                    break
        return minute


    def build_second(self, prefill_second: Optional[str]) -> int:
        """
        Build a second and return it.

        Parameters:
            prefill_second: An optional second to use as the prefill text.

        Returns: The built second.
        """
        while True:
            try:
                second: int = int(super().input_handler(Timestamp.Key.SECOND,
                        prefill_second, can_list_and_search=False))
            except (ValueError):
                print("\tError: Please enter a valid second [0-59].",
                      file=sys.stderr)
            else:
                if (second < 0 or second > 59):
                    print("\tError: Please enter a valid second [0-59].",
                        file=sys.stderr)
                else:
                    break
        return second


    def build_timezone(self, prefill_timezone: Optional[
                zoneinfo.ZoneInfo]) -> zoneinfo.ZoneInfo:
        """
        Build a timezone and return it.

        Parameters:
            prefill_timezone: An optional timezone to use as the prefill text.

        Returns: The built timezone.
        """
        timezones: list[str] = zoneinfo.available_timezones()
        while True:
            timezone: str = super().input_handler(Timestamp.Key.TIMEZONE,
                    prefill_timezone,
                    list_command=(selector.display, [timezones],
                                  {"are_duplicates_hidden": True}),
                    search_command=(selector.search, [timezones],
                                    {"are_duplicates_hidden": True,
                                     "prompt": "Search: "}))
            if (timezone not in timezones):
                print("\tError: Please enter a valid timezone.",
                      file=sys.stderr)
            else:
                break
        return zoneinfo.ZoneInfo(timezone)


    def _get_timestamp_now(self) -> Timestamp:
        """
        Returns the current timestamp based on the latest transaction's
        timezone if it exists, or UTC otherwise.

        Returns: The current timestamp.
        """
        latest_timezone: Optional[ZoneInfo] = None
        transactions: list[transactions] = self.ledger.get_transactions()
        if (transactions):
            latest_transaction: Transaction = transactions[-1]
            latest_timezone = latest_transaction.get_timestamp().get_timezone()
        datetime_now: datetime.datetime = datetime.datetime.now(
                latest_timezone or datetime.timezone.utc)
        timestamp_now: Timestamp = Timestamp(
                datetime_now.timestamp(),
                latest_timezone or datetime.timezone.utc)
        return timestamp_now


    def _reset(self) -> None:
        """
        Reset the timestamp builder.
        """
        self.year = None
        self.month = None
        self.day = None
        self.hour = None
        self.minute = None
        self.second = None
        self.timezone = None
        self.current_step = 0
