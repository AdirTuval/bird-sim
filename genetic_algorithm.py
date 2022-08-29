import argparse
import os
from typing import Mapping, Callable, Tuple, Any, Dict

import pygad
import numpy as np

from simulator import BirdSim


class GeneticAlgo():
    SOLUTION_CURR = 'out/ga_'
    GUI = False
    SAVE_PROC = False
    TO_VISUALIZE = 10

    def __init__(self, gui,
                 save_proc,
                 to_visualize,
                 num_generations,
                 num_parents_mating,
                 sol_per_pop,
                 fitness_func: Callable = None,
                 num_genes=120,
                 init_range_low=-1,
                 init_range_high=1,
                 gene_space=(-1, 0, 1),
                 parent_selection_type='sss',
                 keep_parents=-1,
                 crossover_type='single_point',
                 mutation_type='random',
                 mutation_percent_genes=10,
                 callback_generation: Callable = None,
                 parallel_processing: Tuple[str, int] = ('process', int(os.cpu_count() * 0.7))):
        self.params: Dict = {'num_generations': num_generations,
                             'num_parents_mating': num_parents_mating,
                             'fitness_func': fitness_func if fitness_func else self.fitness_func,
                             'sol_per_pop': sol_per_pop,
                             'num_genes': num_genes,
                             'init_range_low': init_range_low,
                             'init_range_high': init_range_high,
                             'gene_space': gene_space,
                             'parent_selection_type': parent_selection_type,
                             'keep_parents': keep_parents,
                             'crossover_type': crossover_type,
                             'mutation_type': mutation_type,
                             'mutation_percent_genes': mutation_percent_genes,
                             'callback_generation': callback_generation if callback_generation else self.callback_gen,
                             'parallel_processing': parallel_processing}
        self.GUI = gui
        self.SAVE_PROC = save_proc,
        self.TO_VISUALIZE = to_visualize

    @staticmethod
    def fitness_func(solution: np.ndarray, solutions_index) -> float:
        solution = solution.reshape((60, 2))
        solution = np.repeat(solution, 10, axis=0)
        solution = solution.reshape(1200)
        bird_sim = BirdSim()
        altitude, _ = bird_sim.run_simulation_offline(solution)
        return altitude

    @staticmethod
    def save_results(solution: np.ndarray, generation: int):
        np.save(f'{GeneticAlgo.SOLUTION_CURR}{generation}.npy', solution)

    @staticmethod
    def callback_gen(ga_instance: pygad.GA):
        print("Generation : ", ga_instance.generations_completed)
        print("Fitness of the best solution :", ga_instance.best_solution()[1])
        if ga_instance.generations_completed % GeneticAlgo.TO_VISUALIZE == 0:
            policy = ga_instance.best_solution()[0]
            if GeneticAlgo.SAVE_PROC:
                GeneticAlgo.save_results(policy, ga_instance.generations_completed)
            if GeneticAlgo.GUI:
                bird_sim = BirdSim(gui=True)
                bird_sim.run_simulation_offline(policy, gui=True)

    def run(self) -> Tuple[Any, None, Any]:
        ga_instance = pygad.GA(**self.params)
        ga_instance.run()
        ga_instance.plot_fitness()
        solution = ga_instance.best_solution()[0]
        GeneticAlgo.save_results(solution, ga_instance.num_generations)
        return ga_instance.best_solution()


def parse_args():
    parser = argparse.ArgumentParser(description='Run Genetic Algorithm and teach Birdy to fly')
    parser.add_argument('--gui', dest='gui', action='store_true', default=False,
                        help='activate gui')
    parser.add_argument('--save_proc', dest='save_proc', action='store_true', default=False,
                        help='save process')
    parser.add_argument('--to_visualize', metavar='-v', type=int, nargs='?', default=10,
                        help='visualize current policy every v iterations')
    parser.add_argument('--num_generations', metavar='-n', type=int, nargs='?', default=600,
                        help='how many generations the QLearner should run')
    parser.add_argument('--sol_per_pop', metavar='-s', type=int, nargs='?', default=2000,
                        help='size of the population in each generation')
    parser.add_argument('--num_parents_mating', metavar='-p', type=int, nargs='?', default=50,
                        help='num of parents mating in each generation')

    return parser


if __name__ == '__main__':
    parser = parse_args()
    args = parser.parse_args()
    bird_evolution = GeneticAlgo(gui=args.gui, save_proc=args.save_proc, to_visualize=args.to_visualize,
                                 num_generations=args.num_generations, num_parents_mating=args.num_parents_mating,
                                 sol_per_pop=args.sol_per_pop)
    bird_evolution.run()

