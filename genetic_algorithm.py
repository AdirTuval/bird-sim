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


num_generations = 300
num_parents_mating = 8

fitness_function = fitness_func
sol_per_pop = 100
num_genes = 1200

init_range_low = -1
init_range_high = 1

gen_space = range(-1, 2)
parent_selection_type = 'sss'
keep_parents = 1
crossover_type = 'single_point'
mutation_type = 'random'
mutation_percent_genes = 10
params = {'num_generations': num_generations,
          'num_parents_mating': num_parents_mating,
          'fitness_func': fitness_func,
          'sol_per_pop': sol_per_pop,
          'num_genes': num_genes,
          'init_range_low': init_range_low,
          'init_range_high': init_range_high,
          'gene_space': gen_space,
          'parent_selection_type': parent_selection_type,
          'keep_parents': keep_parents,
          'crossover_type': crossover_type,
          'mutation_type': mutation_type,
          'mutation_percent_genes': mutation_percent_genes,
          'callback_generation': callback_gen}

ga_instance = pygad.GA(**params)
ga_instance.run()
ga_instance.plot_fitness()
solution = ga_instance.best_solution()[0]
print(solution)

birdy = BirdSim(gui=True)
while True:
    birdy.run_simulation_offline(solution, gui=True)
    pygame.quit()
