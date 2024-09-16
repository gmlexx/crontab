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


def parse_cron_arg_values(values: str, every: int) -> Generator[tuple[str, str], None, None]:
    """Parse values part of cron argument and returns allowed ranges of values"""
    items = values.split(",")
    for item in items:
        if "-" not in item:
            if every == 1:
                yield (item, item)
            else:
                yield (item, "*")
        else:
            from_value, to_value = item.split("-")
            yield (from_value, to_value)

def get_int_value(text_to_values_dict, value: str) -> int:
    """Get int value by text if available"""
    int_value = text_to_values_dict.get(value.lower())
    if not int_value:
        int_value = int(value)
    return int_value


def match_ranges(value: int, values_ranges: list[tuple[str, str]], text_to_values = None):
    """Returns True if the value matches any of values range in the list"""
    text_to_values_dict = {} if not text_to_values else text_to_values
    for values_range in values_ranges:
        from_match = False
        to_match = False
        from_value, to_value = values_range
        print(f"Values_range: {values_range}, from: {from_value}, to: {to_value}")
        if from_value == "*":
            from_match = True
        else:
            from_int_value = get_int_value(text_to_values_dict, from_value)
            from_match = from_int_value <= value
        if to_value == "*":
            to_match = True
        else:
            to_int_value = get_int_value(text_to_values_dict, to_value)
            to_match = value <= to_int_value
        if from_match and to_match:
            return True
    return False


def get_cron_values(
    cron_arg: str, range_from: int, range_to: int, text_to_values = None
) -> Generator[str, None, None]:
    """Returns minutes according to cronjob argument"""
    values, every = parse_cron_arg(cron_arg)
    values_ranges = list(parse_cron_arg_values(values, every))
    for index, value in enumerate(list(range(range_from, range_to))):
        if match_ranges(value, values_ranges, text_to_values) and index % every == 0:
            yield str(value)


def add_table_values(cron_arg: str, range_from: int, range_to: int, text_to_values = None) -> str:
    """Format cron values for the table output"""
    return " ".join(get_cron_values(cron_arg, range_from, range_to, text_to_values)) + "\n"


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
    table += "month         " + add_table_values(cron_args[3], 1, 13, {"jan": 1, "feb": 2})
    table += "day of week   " + add_table_values(cron_args[4], 0, 7)
    table += "command       " + " ".join(cron_args[5:])
    return table


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("Cronjob input argument is not provided")
    print(get_cron_table(sys.argv[1]))
