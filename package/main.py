from package.constants import *
from package.sga.population import Population


def main():
    population = Population()
    while not population.is_finished():
        if population.generation_number % PRINT_BEST_FITNESS_RATE == 0:
            print('best fitness of generation %d: %d' % (population.generation_number, population.get_best_fitness()))
        population.perform_generation()
    winner = population.get_best_organism()
    print(str(winner))