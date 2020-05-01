import argparse
import configparser
import importlib
import logging
import pathlib
import sys
import textwrap
import typing
import webbrowser

from . import _cli
from . import _utility


def main():
    parser = argparse.ArgumentParser(
        description="Submit FILES to URL.", parents=[_cli.common_options]
    )
    parser.add_argument(
        "-c",
        "--certificate",
        default=_utility.nearest(".kattisrc"),
        help="a file that some some judges (Kattis) require to login (defaults to nearest `.kattisrc`)",
    )
    parser.add_argument(
        "-f", "--force", action="store_true", help="Don't prompt before submission.",
    )
    parser.add_argument("-l", "--language")
    parser.add_argument("-m", "--main-class")
    parser.add_argument("url")
    parser.add_argument("files", nargs="+", type=pathlib.Path)

    try:
        args = parser.parse_args()

        logging.basicConfig(level=args.log_level)
        # stderr_handler = logging.StreamHandler(sys.stderr)
        # stderr_handler.setFormatter(logging.Formatter("[%(level)s] %(message)s"))
        # stderr_handler.setLevel(args.log_level)
        # root_logger.addHandler(stderr_handler)

        kwargs = vars(args)
        positive_replies = ["y", "yes"]
        problem = _utility.identify_problem(args.url)
        if args.force or input("Submit? [yN] ").lower() in positive_replies:
            verdict = problem.submit(**kwargs)
            print(verdict)
            webbrowser.open(verdict)
    except FileNotFoundError as err:
        raise
