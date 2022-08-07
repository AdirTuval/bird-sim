#!/usr/bin/env python3

import argparse
import os
import shlex
import sys
import logging
from pathlib import Path
from typing import Tuple

from simulator import BirdSim

logger = logging.getLogger(__name__)

PROGRAM_NAME = "bird-sim"
VERSION = "1.0.0"
DESCRIPTION = """Bird-Sim is a program that simulates a bird flight"""

EPILOG = """For more information, visit the project page on:
https://github.com/AdirTuval/bird-sim"""

TITLE = """
______ _         _   _____ _           
| ___ (_)       | | /  ___(_)          
| |_/ /_ _ __ __| | \ `--. _ _ __ ___  
| ___ \ | '__/ _` |  `--. \ | '_ ` _ \ 
| |_/ / | | | (_| | /\__/ / | | | | | |
\____/|_|_|  \__,_| \____/|_|_| |_| |_|
"""

def main_play(args: argparse.Namespace) -> None:
    BirdSim(gui=True).run_simulation()

def main_train(args: argparse.Namespace) -> None:
    if not _is_valid_output(args.output):
        raise NotADirectoryError(f"Failed to locate the directory for output file: '{args.output}'")

def main_policy(args: argparse.Namespace) -> None:
    if not _is_valid_file(args.input_file):
        raise FileNotFoundError(f"Failed to locate policy file: '{args.input_file}'")

def _is_valid_file(file_path: str) -> bool:
    """
    Check whether the file path is an existing file.

    Args:
        file_path: file path to check

    Returns:
        True if exists, False otherwise
    """
    return Path(file_path).is_file()


def _is_valid_output(output_file_path: str) -> bool:
    """
    Check whether the file path can be created. i.e it's contained directory exists.

    Args:
        output_file_path: file path to check

    Returns:
        True if can be created, False otherwise
    """
    return Path(output_file_path).parent.is_dir()


def arguments_parser() -> argparse.Namespace:
    """
    Parse command line arguments and apply the given commands.
    """
    parser = argparse.ArgumentParser(prog=PROGRAM_NAME, description=TITLE + '\n' + DESCRIPTION, epilog=EPILOG,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-v', '--version', action="version", version=f'{PROGRAM_NAME.title()} {VERSION}')
    parser.add_argument('-l', '--loglevel', type=str, action="store", help="set logging level")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # parser for training the bird agent
    parser_train = subparsers.add_parser('train', help="train the bird")
    parser_train.set_defaults(func=main_train)
    parser_train.add_argument('-o', '--output', type=str, action='store', help='write output policy to <file> path',
                                      metavar='<file>', required=True)

    # parser for GUI
    parser_play = subparsers.add_parser('play', help="play an interactive game")
    parser_play.set_defaults(func=main_play)

    # parser for 'policy'
    parser_policy = subparsers.add_parser('policy', help="show policy")
    parser_policy.set_defaults(func=main_policy)
    parser_policy.add_argument('input_file', type=str, action='store', help="path to .policy input file",
                             metavar='<policy file>')

    return parser.parse_args(sys.argv[1:])


def main():
    """
    Client side to use ``bird-sim`` core api from CLI.
    Run bird-sim program with the given command line arguments.
    """
    args = arguments_parser()
    print(TITLE)
    logger.debug(args)

    return args.func(args)  # call the subcommand method


if __name__ == "__main__":
    sys.exit(main())
