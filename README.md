# Cronjob expression parser

Ccommand line application or script which parses a cron string and expands each field
to show the times at which it will run.

You should only consider the standard cron format with five time fields (minute, hour, day of
month, month, and day of week) plus a command, scrip doesn't handle time strings such as "@yearly". 
The input must be on a single line.

`~$ python3 cronjob.py "*/15 0 1,15 * 1-5 /usr/bin/find"`

The output is formatted as a table with the field name taking the first 14 columns and
the times as a space-separated list following it.
For example, the following input argument:

```
python3 cronjob.py */15 0 1,15 * 1-5 /usr/bin/find

Yields the following output:

minute        0 15 30 45
hour          0
day of month  1 15
month         1 2 3 4 5 6 7 8 9 10 11 12
day of week   1 2 3 4 5
command       /usr/bin/find
```

## How to run parser

1. Clone this git repo
1. Make sure that you have [python3 installed](https://www.python.org/downloads/) on your system (verified with 3.11)
1. Run script `python3 cronjob.py "<cron expression>"`

## How to setup dev environment and run tests

1. Install Python linters and formatters: [black](https://pypi.org/project/black/), [pylint](https://pypi.org/project/pylint/), and types checker [pyright](https://pypi.org/project/pyright/)
1. Install requirements for running test `pip3 install -r requirements.txt`
1. Run "pytest" in the current folder

