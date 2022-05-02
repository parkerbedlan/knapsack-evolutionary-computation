from typing import Callable
from package.constants import *
from package.sga.population import Population
from package.climbing.climber import Climber
import time


def run_test() -> dict[str, int]:
    def ga_test():
        # print('running ga test')
        population = Population()
        while not population.is_finished():
            if PRINT_BEST_FITNESS_RATE != -1 and population.generation_number % PRINT_BEST_FITNESS_RATE == 0:
                print('best fitness of generation %d: %d' %
                      (population.generation_number, population.get_best_fitness()))
            population.perform_generation()
        winner = population.best_organism_ever
        print(str(winner))
        return {'fitness': winner.fitness, 'generations': population.generation_number}

    def climbing_test():
        print('running climbing test')
        climber = Climber()
        last_iteration_quotient = 0
        while not climber.is_finished():
            new_iteration_quotient = climber.total_iterations // PRINT_BEST_FITNESS_RATE
            if PRINT_BEST_FITNESS_RATE != -1 and new_iteration_quotient > last_iteration_quotient:
                print('fitness of iteration %d: %d' % (
                    climber.total_iterations, climber.current_organism.fitness))
            last_iteration_quotient = new_iteration_quotient

            climber.run_session()
        winner = climber.best_organism_ever
        print(str(winner))
        return {'fitness': winner.fitness, 'generations': climber.total_iterations}

    tests = {'GA': ga_test, 'Climbing': climbing_test}
    return tests[MODE]()


def run_tests(num_tests: int) -> None:
    tests = [run_test() for _ in range(num_tests)]
    # type:ignore
    comparator: Callable[[dict[str, int]],
                         int] = lambda test: test['fitness']*1000 - test['generations']
    best = max(tests, key=comparator)  # type:ignore
    worst = min(tests, key=comparator)  # type:ignore
    average_fitness = sum([t['fitness'] for t in tests]) / num_tests
    average_generations = sum([t['generations'] for t in tests]) / num_tests
    best_frequency = sum(
        [1 for test in tests if test['fitness'] == best['fitness']]) / num_tests * 100
    best_closeness_to_optimal = best['fitness'] / OPTIMAL * 100
    average_closeness_to_optimal = average_fitness / OPTIMAL * 100
    print("""%s
%d tests performed. Results:
Best fitness: %s
Best closeness to optimal: %.2f%%
Frequency of best: %.2f%%
Worst fitness: %s
Average fitness: %d
Average number of generations: %d
Average closeness to optimal: %.2f%%
%s"""
          % (
              '-'*50, num_tests, str(best), best_closeness_to_optimal, best_frequency, str(worst), average_fitness, average_generations, average_closeness_to_optimal, '-'*50))


def main():
    start_time = time.time()
    if MODE == 'GA':
        settings = 'GA: %s, selection=%s, k=%s, mutation=%s %.2f, crossover=%s %.2f, population size=%d, generation threshold=%d, elitism=%d' % (
            DATASET_NAME, SELECTION_OPERATOR, TOURNAMENT_K, MUTATION_OPERATOR, MUTATION_RATE, CROSSOVER_OPERATOR, CROSSOVER_RATE, POPULATION_SIZE, GENERATION_THRESHOLD, ELITISM_AMOUNT)
    elif FOOLISH_MODE:
        settings = 'running FHC: %s, no change threshold=%d' % (
            DATASET_NAME, NO_CHANGE_THRESHOLD)
    else:
        settings = 'running SA: %s, alpha=%f, i_0=%d, beta=%f, no change threshold=%d' % (
            DATASET_NAME, ALPHA, I_0, BETA, NO_CHANGE_THRESHOLD)
    print(settings)
    run_tests(5)
    print(settings)
    print(CROSSOVER_OPERATOR)
    print('finished in %.2f seconds' % (time.time() - start_time))
