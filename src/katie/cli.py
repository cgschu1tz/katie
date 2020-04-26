import argparse
import logging
import typing

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
