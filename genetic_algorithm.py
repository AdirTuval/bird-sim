import pygad
import numpy as np
import pygame

from simulator import BirdSim
import bird


def callback_gen(ga_instance):
    print("Generation : ", ga_instance.generations_completed)
    print("Fitness of the best solution :", ga_instance.best_solution()[1])


def fitness_func(solution, solutions_index):
    bird_sim = BirdSim()
    altitude, _ = bird_sim.run_simulation_offline(solution)
    return altitude


params = {'num_generations': 300,
          'num_parents_mating': 50,
          'fitness_func': fitness_func,
          'sol_per_pop': 1000,
          'num_genes': 1200,
          'init_range_low': -1,
          'init_range_high': 1,
          'gene_space': range(-1, 2),
          'parent_selection_type': 'sss',
          'keep_parents': 1,
          'crossover_type': 'single_point',
          'mutation_type': 'random',
          'mutation_percent_genes': 10,
          'callback_generation': callback_gen}

ga_instance = pygad.GA(**params)
ga_instance.run()
ga_instance.plot_fitness()
solution = ga_instance.best_solution()[0]
with open('a.npy', 'wb') as f:
    np.save(f, solution)

# birdy = BirdSim(gui=True)
# while True:
#     birdy.run_simulation_offline(solution, gui=True)
#     pygame.quit()
