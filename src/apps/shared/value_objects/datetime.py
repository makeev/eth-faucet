from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Union
from zoneinfo import ZoneInfo

DEFAULT_TIMEZONE = ZoneInfo("UTC")


@dataclass(frozen=True)
class DomainDateTime:
    dt: datetime

    def __post_init__(self):
        if self.dt.tzinfo is None:
            raise ValueError("datetime must be timezone-aware")

    @classmethod
    def now(cls, tz: ZoneInfo = DEFAULT_TIMEZONE) -> "DomainDateTime":
        return cls(dt=datetime.now(tz))

    def to_naive(self) -> datetime:
        return self.dt.astimezone(DEFAULT_TIMEZONE).replace(tzinfo=None)

    def strftime(self, format: str) -> str:
        return self.dt.strftime(format)

    def astimezone(self, tz: Union[ZoneInfo, None] = None) -> "DomainDateTime":
        return DomainDateTime(self.dt.astimezone(tz))

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, DomainDateTime):
            return self.dt == other.dt
        if isinstance(other, datetime):
            return self.dt == other
        return NotImplemented

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, DomainDateTime):
            return self.dt < other.dt
        if isinstance(other, datetime):
            return self.dt < other
        return NotImplemented

    def __le__(self, other: Any) -> bool:
        if isinstance(other, DomainDateTime):
            return self.dt <= other.dt
        if isinstance(other, datetime):
            return self.dt <= other
        return NotImplemented

    def __gt__(self, other: Any) -> bool:
        if isinstance(other, DomainDateTime):
            return self.dt > other.dt
        if isinstance(other, datetime):
            return self.dt > other
        return NotImplemented

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, DomainDateTime):
            return self.dt >= other.dt
        if isinstance(other, datetime):
            return self.dt >= other
        return NotImplemented

    def __add__(self, other: timedelta) -> "DomainDateTime":
        if isinstance(other, timedelta):
            return DomainDateTime(self.dt + other)
        return NotImplemented

    def __sub__(self, other: Union[timedelta, "DomainDateTime"]) -> Union["DomainDateTime", timedelta]:
        if isinstance(other, timedelta):
            return DomainDateTime(self.dt - other)
        if isinstance(other, DomainDateTime):
            return self.dt - other.dt
        if isinstance(other, datetime):
            return self.dt - other
        return NotImplemented

    @property
    def year(self) -> int:
        return self.dt.year

    @property
    def month(self) -> int:
        return self.dt.month

    @property
    def day(self) -> int:
        return self.dt.day

    @property
    def hour(self) -> int:
        return self.dt.hour

    @property
    def minute(self) -> int:
        return self.dt.minute

    @property
    def second(self) -> int:
        return self.dt.second

    @property
    def microsecond(self) -> int:
        return self.dt.microsecond

    @property
    def tzinfo(self) -> ZoneInfo | None:
        return self.dt.tzinfo if isinstance(self.dt.tzinfo, ZoneInfo) else None
