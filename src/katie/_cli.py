import argparse
import configparser
import importlib
import logging
import pathlib
import sys
import textwrap
import typing
import webbrowser

from . import _utility


def main():
    common_options = argparse.ArgumentParser(add_help=False)
    common_options.add_argument(
        "-d",
        "--debug",
        action="store_const",
        const=logging.DEBUG,
        default=logging.INFO,
        dest="log_level",
        help="Print debugging information to stderr.",
    )
    parser = argparse.ArgumentParser(
        description="Interact with competitive programming problems."
    )
    subcmds = parser.add_subparsers()

    download_cmd = subcmds.add_parser(
        "download",
        aliases=["d"],
        parents=[common_options],
        description="Download tests from `url`.",
    )
    download_cmd.add_argument(
        "-o",
        "--dest",
        default=pathlib.Path.cwd(),
        type=pathlib.Path,
        help="destination folder (defaults to current working directory)",
    )
    download_cmd.add_argument("url")

    def download(url, dest):
        problem = _utility.identify_problem(url)
        problem.download_tests().extractall(dest)

    download_cmd.set_defaults(callback=download)

    submit_cmd = subcmds.add_parser(
        "submit",
        aliases=["s"],
        description="Submit `files` to `url`.",
        parents=[common_options],
    )
    submit_cmd.add_argument(
        "-c",
        "--certificate",
        default=_utility.nearest(".kattisrc"),
        help="a file that some some judges (Kattis) require to login (defaults to nearest `.kattisrc`)",
    )
    submit_cmd.add_argument(
        "-f", "--force", action="store_true", help="Don't prompt before submission.",
    )
    submit_cmd.add_argument("-l", "--language")
    submit_cmd.add_argument("-m", "--main-class")
    submit_cmd.add_argument("url")
    submit_cmd.add_argument("files", nargs="+", type=pathlib.Path)

    def submit(url, force, **kwargs):
        positive_replies = ["y", "yes"]
        problem = _utility.identify_problem(url)
        if force or input("Submit? [yN] ").lower() in positive_replies:
            verdict = problem.submit(**kwargs)
            print(verdict)
            webbrowser.open(verdict)

    submit_cmd.set_defaults(callback=submit)

    try:
        args = parser.parse_args()
        kwargs = vars(args)

        logging.basicConfig(level=args.log_level)
        # stderr_handler = logging.StreamHandler(sys.stderr)
        # stderr_handler.setFormatter(logging.Formatter("[%(level)s] %(message)s"))
        # stderr_handler.setLevel(args.log_level)
        # root_logger.addHandler(stderr_handler)
        args.callback(**kwargs)
    except AttributeError:
        pass
