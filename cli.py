#!/usr/bin/env python3

import argparse
import os
import shlex
import sys
import logging
import time
from pathlib import Path
from typing import Tuple

import numpy as np

from simulator import BirdSim
from genetic_algorithm import GeneticAlgo
from qlearning import BirdQLearner

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
    BirdSim(gui=True).run_simulation_interactive()


def main_train(args: argparse.Namespace) -> None:
    if args.algorithm == 'GA':
        ga_runner = GeneticAlgo(gui=args.gui, save_proc=args.save_proc, to_visualize=args.to_visualize,
                                num_generations=args.num_generations, num_parents_mating=args.num_parents_mating,
                                sol_per_pop=args.sol_per_pop)
        ga_runner.run()

    elif args.algorithm == 'QL':
        ql_runner = BirdQLearner(args.gui, args.save_proc, args.num_iterations, args.to_visualize)
        ql_runner.run_bird_learner()


def main_policy(args: argparse.Namespace) -> None:
    if not _is_valid_file(args.input_file):
        raise FileNotFoundError(f"Failed to locate policy file: '{args.input_file}'")

    bird_sim = BirdSim(gui=True)

    policy = np.load(args.input_file)

    bird_sim.run_simulation_offline(policy, gui=True)


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
    parser.add_argument('--version', action="version", version=f'{PROGRAM_NAME.title()} {VERSION}')
    parser.add_argument('--loglevel', type=str, action="store", default='info', help="set logging level")
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_train = subparsers.add_parser('train', help="train the bird")

    parser_train.add_argument('--gui', '-g', action='store_true', default=False,
                              help='activate gui {default=False}')
    parser_train.add_argument('--save_proc', '-o', action='store_true', default=False,
                              help='save process {default=False}')
    parser_train.add_argument('--to_visualize', '-v', type=int, nargs='?', default=10,
                              help='visualize current policy every v iterations {default=10}')

    train_subparsers = parser_train.add_subparsers(dest='algorithm', required=True)

    genetic_parser = train_subparsers.add_parser('GA', help='train using Genetic Algorithm')
    genetic_parser.add_argument('--num_generations', '-n', type=int, nargs='?', default=600,
                                help='how many generations the QLearner should run {default=600}')
    genetic_parser.add_argument('--sol_per_pop', '-s', type=int, nargs='?', default=2000,
                                help='size of the population in each generation {default=2000}')
    genetic_parser.add_argument('--num_parents_mating', '-p', type=int, nargs='?', default=50,
                                help='num of parents mating in each generation {default=50}')
    qlearning_parser = train_subparsers.add_parser('QL', help='train using QLearning algorithm')
    qlearning_parser.add_argument('--num_iterations', '-i', type=int, nargs='?', default=2000,
                                  help='how many iteration the QLearner should run {default=2000}')
    parser_train.set_defaults(func=main_train)

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
    numeric_level = getattr(logging, args.loglevel.upper(), None)
    logging.basicConfig(level=numeric_level)
    logger.debug(args)

    return args.func(args)  # call the subcommand method


if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    elapsed = round((time.perf_counter() - start_time) / 60, 2)  # minutes
    logger.info(f"Elapsed time: {elapsed} minuets")
