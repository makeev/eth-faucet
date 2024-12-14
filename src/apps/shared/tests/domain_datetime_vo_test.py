import dataclasses
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pytest

from apps.shared.value_objects.datetime import DomainDateTime


@pytest.fixture
def utc_now():
    return datetime.now(ZoneInfo("UTC"))


@pytest.fixture
def domain_dt(utc_now):
    return DomainDateTime(dt=utc_now)


def test_creation_with_naive_datetime():
    naive_dt = datetime.now()
    with pytest.raises(ValueError, match="datetime must be timezone-aware"):
        DomainDateTime(dt=naive_dt)


def test_creation_with_aware_datetime(utc_now):
    domain_dt = DomainDateTime(dt=utc_now)
    assert domain_dt.dt == utc_now


def test_now_factory_method():
    domain_dt = DomainDateTime.now()
    assert domain_dt.dt.tzinfo is not None
    assert isinstance(domain_dt, DomainDateTime)


def test_now_with_specific_timezone():
    tz = ZoneInfo("Europe/Moscow")
    domain_dt = DomainDateTime.now(tz=tz)
    assert domain_dt.dt.tzinfo == tz


def test_to_naive(domain_dt):
    naive = domain_dt.to_naive()
    assert naive.tzinfo is None
    assert isinstance(naive, datetime)


def test_strftime(domain_dt):
    format_string = "%Y-%m-%d %H:%M:%S"
    expected = domain_dt.dt.strftime(format_string)
    assert domain_dt.strftime(format_string) == expected


def test_astimezone(domain_dt):
    moscow_tz = ZoneInfo("Europe/Moscow")
    moscow_time = domain_dt.astimezone(moscow_tz)
    assert moscow_time.tzinfo == moscow_tz
    assert isinstance(moscow_time, DomainDateTime)


@pytest.mark.parametrize(
    "operation,expected",
    [
        (lambda x, y: x == y, True),
        (lambda x, y: x < y + timedelta(seconds=1), True),
        (lambda x, y: x <= y, True),
        (lambda x, y: x > y - timedelta(seconds=1), True),
        (lambda x, y: x >= y, True),
    ],
)
def test_comparisons(domain_dt, operation, expected):
    assert operation(domain_dt, domain_dt) == expected


def test_comparison_with_datetime(domain_dt):
    assert domain_dt == domain_dt.dt
    assert domain_dt <= domain_dt.dt
    assert domain_dt >= domain_dt.dt


def test_invalid_comparison():
    dt = DomainDateTime.now()
    with pytest.raises(TypeError):
        dt < "invalid"  # type: ignore


def test_timedelta_addition(domain_dt):
    delta = timedelta(days=1)
    result = domain_dt + delta
    assert isinstance(result, DomainDateTime)
    assert result.dt == domain_dt.dt + delta


def test_timedelta_subtraction(domain_dt):
    delta = timedelta(days=1)
    result = domain_dt - delta
    assert isinstance(result, DomainDateTime)
    assert result.dt == domain_dt.dt - delta


def test_datetime_subtraction(domain_dt):
    other_dt = DomainDateTime.now()
    result = other_dt - domain_dt
    assert isinstance(result, timedelta)


def test_properties(domain_dt):
    assert domain_dt.year == domain_dt.dt.year
    assert domain_dt.month == domain_dt.dt.month
    assert domain_dt.day == domain_dt.dt.day
    assert domain_dt.hour == domain_dt.dt.hour
    assert domain_dt.minute == domain_dt.dt.minute
    assert domain_dt.second == domain_dt.dt.second
    assert domain_dt.microsecond == domain_dt.dt.microsecond
    assert domain_dt.tzinfo == domain_dt.dt.tzinfo


def test_immutability(domain_dt):
    with pytest.raises(dataclasses.FrozenInstanceError):
        domain_dt.dt = datetime.now(ZoneInfo("UTC"))


@pytest.mark.parametrize("tz_name", ["UTC", "Europe/London", "America/New_York", "Asia/Tokyo", "Australia/Sydney"])
def test_different_timezones(tz_name):
    tz = ZoneInfo(tz_name)
    dt = DomainDateTime.now(tz)
    assert dt.tzinfo == tz


def test_timezone_conversion_preserves_instant(domain_dt):
    original_timestamp = domain_dt.dt.timestamp()

    tokyo_time = domain_dt.astimezone(ZoneInfo("Asia/Tokyo"))
    ny_time = domain_dt.astimezone(ZoneInfo("America/New_York"))

    assert tokyo_time.dt.timestamp() == pytest.approx(original_timestamp)
    assert ny_time.dt.timestamp() == pytest.approx(original_timestamp)


def test_hash_consistency(domain_dt):
    same_time = DomainDateTime(dt=domain_dt.dt)
    assert hash(domain_dt) == hash(same_time)

    time_dict = {domain_dt: "value"}
    assert time_dict[same_time] == "value"


def test_addition_invalid_type(domain_dt):
    with pytest.raises(TypeError):
        domain_dt + "invalid"  # type: ignore


def test_subtraction_invalid_type(domain_dt):
    with pytest.raises(TypeError):
        domain_dt - "invalid"  # type: ignore


def test_comparison_chain(domain_dt):
    later = domain_dt + timedelta(hours=1)
    even_later = later + timedelta(hours=1)

    assert domain_dt < later < even_later
    assert domain_dt <= later <= even_later
    assert even_later > later > domain_dt
