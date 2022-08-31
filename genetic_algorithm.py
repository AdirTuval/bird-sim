import argparse
import os
from typing import Mapping, Callable, Tuple, Any, Dict

import pygad
import numpy as np

from simulator import BirdSim


class GeneticAlgo:
    """
    Train Bird to fly using genetic algorithm
    """
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
        GeneticAlgo.GUI = gui
        GeneticAlgo.SAVE_PROC = save_proc,
        GeneticAlgo.TO_VISUALIZE = to_visualize

    @staticmethod
    def fitness_func(solution: np.ndarray, solutions_index) -> float:
        """
        Given a policy returns the altitude of the bird after using that policy.
        """
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
        """
        Runs after every generation, visualizing and saving the current policy if defined
        """
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
