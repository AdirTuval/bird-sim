import os
from typing import Mapping, Callable, Tuple, Any, Dict

import pygad
import numpy as np

from simulator import BirdSim


class GeneticAlgo():
    SOLUTION_CURR = 'out/ga.npy'

    def __init__(self, num_generations=300,
                 num_parents_mating=50,
                 fitness_func: Callable = None,
                 sol_per_pop=1000,
                 num_genes=1200,
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

    @staticmethod
    def fitness_func(solution: np.ndarray, solutions_index) -> float:
        bird_sim = BirdSim()
        altitude, _ = bird_sim.run_simulation_offline(solution)
        return altitude

    @staticmethod
    def save_results(solution: np.ndarray):
        np.save(GeneticAlgo.SOLUTION_CURR, solution)

    @staticmethod
    def callback_gen(ga_instance: pygad.GA):
        print("Generation : ", ga_instance.generations_completed)
        print("Fitness of the best solution :", ga_instance.best_solution()[1])
        if ga_instance.generations_completed % 10 == 0:
            GeneticAlgo.save_results(ga_instance.best_solution()[0])

    def run(self) -> Tuple[Any, None, Any]:
        ga_instance = pygad.GA(**self.params)
        ga_instance.run()
        ga_instance.plot_fitness()
        solution = ga_instance.best_solution()[0]
        GeneticAlgo.save_results(solution)
        return ga_instance.best_solution()


if __name__ == '__main__':
    GeneticAlgo().run()
