#!/usr/bin/env python3

# pylint: disable=broad-exception-raised

"""This module parsing cronjob arguments and prints a table of execution times"""
import sys
from typing import Generator


def parse(args: str) -> list[str]:
    """Returns a list of parsed arguments string"""
    return [arg for arg in args.strip().split(" ") if arg.strip()]


def parse_cron_arg(arg: str) -> tuple[str, int]:
    """Parse cron argument to values/every parts"""
    if arg == "*":
        return ("*", 1)
    if "/" not in arg:
        return (arg, 1)
    value, every = arg.split("/")
    if every == "0":
        raise Exception(f"Zero interval cannot be defined {arg}")
    return (value, int(every))


def parse_cron_arg_values(values: str) -> Generator[tuple[str, str], None, None]:
    """Parse values part of cron argument and returns allowed ranges of values"""
    items = values.split(",")
    for item in items:
        if "-" not in item:
            yield (item, item)
        else:
            from_value, to_value = item.split("-")
            yield (from_value, to_value)


def match_ranges(value: int, values_ranges: list[tuple[str, str]]):
    """Returns True if the value matches any of values range in the list"""
    for from_value, to_value in values_ranges:
        if from_value == "*":
            return True
        if int(from_value) <= value <= int(to_value):
            return True
    return False


def get_cron_values(
    cron_arg: str, range_from: int, range_to: int
) -> Generator[str, None, None]:
    """Returns minutes according to cronjob argument"""
    values, every = parse_cron_arg(cron_arg)
    values_ranges = list(parse_cron_arg_values(values))
    for index, value in enumerate(range(range_from, range_to)):
        if match_ranges(value, values_ranges) and index % every == 0:
            yield str(value)


def add_table_values(cron_arg: str, range_from: int, range_to: int) -> str:
    """Format cron values for the table output"""
    return " ".join(get_cron_values(cron_arg, range_from, range_to)) + "\n"


def get_cron_table(arg: str) -> str:
    """Parse cron argument and returns a time table"""
    cron_args = parse(arg)
    cron_args_len = len(cron_args)
    if cron_args_len < 6:
        raise Exception(
            f"Invalid cron expression: {arg}. Number of arguments provided: {cron_args_len} should not be less than 6"
        )
    table = "minute        " + add_table_values(cron_args[0], 0, 60)
    table += "hour          " + add_table_values(cron_args[1], 0, 24)
    table += "day of month  " + add_table_values(cron_args[2], 1, 32)
    table += "month         " + add_table_values(cron_args[3], 1, 13)
    table += "day of week   " + add_table_values(cron_args[4], 0, 7)
    table += "command       " + " ".join(cron_args[5:])
    return table


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("Cronjob input argument is not provided")
    print(get_cron_table(sys.argv[1]))
