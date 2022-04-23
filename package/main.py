from package.constants import *
from package.sga.population import Population


def run_test() -> int:
    population = Population()
    while not population.is_finished():
        if PRINT_BEST_FITNESS_RATE != 0 and population.generation_number % PRINT_BEST_FITNESS_RATE == 0:
            print('best fitness of generation %d: %d' % (population.generation_number, population.get_best_fitness()))
        population.perform_generation()
    winner = population.get_best_organism()
    print(str(winner))
    return winner.fitness


def run_tests(num_tests: int) -> None:
    tests = [run_test() for _ in range(num_tests)]
    best = max(tests)
    worst = min(tests)
    average = sum(tests) / num_tests
    best_frequency = sum([1 for test in tests if test == best]) / num_tests * 100
    print('%s\n%d tests performed. Results:\nBest fitness: %d\nWorst fitness: %d\nAverage fitness: %d\nFrequency of best: %.2f%%\n%s' % ('-'*50, num_tests, best, worst, average, best_frequency, '-'*50))


def main():
    run_tests(100)