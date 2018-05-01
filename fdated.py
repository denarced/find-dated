#!/usr/bin/env python3

import argparse
import datetime
import itertools
import os
import re

RE_OBJ = re.compile(r"(\d\d\d\d-\d\d-\d\d)")


def iterate_files(a_dir):
    for root, _, files in os.walk(a_dir):
        for each in files:
            yield os.path.join(root, each)


def to_limits(older, newer):
    returned = {}
    if older is not None:
        returned["older"] = older
    if newer is not None:
        returned["newer"] = newer
    return returned


def within(filepath, dates, today):
    match = re.search(RE_OBJ, filepath)
    if not match:
        return False
    date_str = match.group(1)
    try:
        files_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return False
    if "older" in dates:
        reference = today - datetime.timedelta(dates["older"])
        if files_date >= reference:
            return False
    if "newer" in dates:
        reference = today - datetime.timedelta(dates["newer"])
        if files_date <= reference:
            return False
    return True


def main(args):
    limits = to_limits(args.older, args.newer)
    dir_generators = [iterate_files(each) for each in args.dir]
    paths = itertools.chain(*dir_generators)
    if args.today is None:
        today = datetime.date.today()
    else:
        today = args.today
    within_range = (each for each in paths if within(each, limits, today))
    for each in within_range:
        print(each)


def to_date(date_str):
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid date: " + date_str)


def cli_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", nargs="+", help="directory to search")
    parser.add_argument("-n", "--newer", type=int, help="at most n days old")
    parser.add_argument("-o", "--older", type=int, help="at least n days old")
    parser.add_argument(
        "-t",
        "--today",
        type=to_date,
        help="date to use (e.g. 2001-12-01)")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main(cli_parse())
