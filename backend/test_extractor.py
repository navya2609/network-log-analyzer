
from extractor import extract_timestamps


def test_network_timestamp():
    log = """
Network connection lost
Observed at 2026-08-14 09:17:31
"""
    assert extract_timestamps(log) == [
        "2026-08-14T09:17:31"
    ]


def test_backup_timestamp_excluded():
    log = """
Network connection lost
Observed at 2026-08-14 09:17:31

System backup completed
2026-08-14 10:00:00
"""
    assert extract_timestamps(log) == [
        "2026-08-14T09:17:31"
    ]


def test_time_only():
    log = "09:19:06 | monitoring resumed"

    assert extract_timestamps(log) == [
        "09:19:06"
    ]


def test_day_first_format():
    log = """
Network interface went DOWN
metadata={"observed":"14/08/2026 11:42:08"}
"""
    assert extract_timestamps(log) == [
        "2026-08-14T11:42:08"
    ]


def test_no_timestamps():
    log = "Network monitoring started"

    assert extract_timestamps(log) == []


def test_invalid_timestamp():
    log = "Network failure at 2026-99-99 25:80:90"

    assert extract_timestamps(log) == []
