#!/usr/bin/env -S pytest -v

# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import pytest

import cronjob


@pytest.mark.parametrize(
    "args",
    [
        "*/15 0 1,15 * 1-5 cmd",
        "* * * * * cmd",
        "*  * * * * cmd",
        "*  * * * * cmd ",
    ],
)
def test_valid_arguments_parsing(args: str):
    args_list = cronjob.parse(args)
    assert len(args_list) == 6
    assert args_list[5] == "cmd"


def test_valid_cron_argument_parsing():
    value, every = cronjob.parse_cron_arg("*")
    assert value == "*"
    assert every == 1
    value, every = cronjob.parse_cron_arg("*/15")
    assert value == "*"
    assert every == 15
    value, every = cronjob.parse_cron_arg("1-10/15")
    assert value == "1-10"
    assert every == 15
    value, every = cronjob.parse_cron_arg("1-10")
    assert value == "1-10"
    assert every == 1


def test_valid_cron_argument_values_parsing():
    assert list(cronjob.parse_cron_arg_values("*", 1)) == [("*", "*")]
    assert list(cronjob.parse_cron_arg_values("1-15", 1)) == [("1", "15")]
    assert list(cronjob.parse_cron_arg_values("1-15,20", 1)) == [
        ("1", "15"),
        ("20", "20"),
    ]


def test_valid_minutes():
    minutes = cronjob.get_cron_values("*/15", 0, 60)
    assert list(minutes) == ["0", "15", "30", "45"]


def test_valid_minutes_range():
    minutes = cronjob.get_cron_values("20-30/5", 0, 60)
    assert list(minutes) == ["20", "25", "30"]

def test_valid_hours_range():
    minutes = cronjob.get_cron_values("10/2", 0, 24)
    assert list(minutes) == ["10", "12", "14", "16", "18", "20", "22"]

def test_valid_hours():
    hours = cronjob.get_cron_values("*/6", 0, 24)
    assert list(hours) == ["0", "6", "12", "18"]

def test_valid_months():
    months = cronjob.get_cron_values("1,12", 1, 13)
    assert list(months) == ["1", "12"]

def test_valid_months_as_text():
    months = cronjob.get_cron_values("JAN-MAR", 1, 13, {"jan": 1, "feb": 2, "mar": 3})
    assert list(months) == ["1","2", "3"]

def test_valid_days_of_week():
    days_of_week = cronjob.get_cron_values("*/2", 0, 7)
    assert list(days_of_week) == ["0", "2", "4", "6"]


def test_valid_cronjob_table():
    expression = "*/15 0 1,15 * 1-5 /usr/bin/find"
    assert cronjob.get_cron_table(expression) == (
        "minute        0 15 30 45\n"
        "hour          0\n"
        "day of month  1 15\n"
        "month         1 2 3 4 5 6 7 8 9 10 11 12\n"
        "day of week   1 2 3 4 5\n"
        "command       /usr/bin/find"
    )


def test_invalid_range():
    with pytest.raises(Exception) as exc_info:
        list(cronjob.get_cron_values("*/0", 0, 60))
    assert str(exc_info.value) == ("Zero interval cannot be defined */0")


def test_invalid_cronjob_table():
    expression = "*/15 0 * 1-5 /usr/bin/find"
    with pytest.raises(Exception) as exc_info:
        cronjob.get_cron_table(expression)
    assert str(exc_info.value) == (
        "Invalid cron expression: */15 0 * 1-5 /usr/bin/find. "
        "Number of arguments provided: 5 should not be less than 6"
    )
