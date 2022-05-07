from package.constants import ALPHA, BETA, FOOLISH_MODE, I_0, NO_CHANGE_THRESHOLD
from package.sga.organism import Organism
from package.sga.population import Population
import math
from random import random


def standard_deviation(arr: list[int]):
    mean = sum(arr) / len(arr)
    numerator = sum([(x-mean)**2 for x in arr])
    return math.sqrt(numerator/len(arr))


class Climber:
    initial_temperature: float
    current_organism: Organism
    best_organism_ever: Organism
    temperature: float
    iterations_per_session: int
    iterations_without_change: int
    total_iterations: int

    def __init__(self):
        self.current_organism = Population.gen_random_org()
        self.best_organism_ever = self.current_organism
        self.initial_temperature = Climber.__get_initial_temperature()
        self.temperature = self.initial_temperature
        self.iterations_per_session = I_0
        self.iterations_without_change = 0
        self.total_iterations = 0

    def run_session(self):
        for _ in range(self.iterations_per_session):
            self.total_iterations += 1
            new_organism = Organism(self.current_organism.chromosome)
            new_organism.mutate()
            new_is_better = new_organism > self.current_organism
            if new_is_better:
                self.best_organism_ever = new_organism

            if new_is_better or (not FOOLISH_MODE and random() < math.exp((new_organism.fitness - self.current_organism.fitness)/self.temperature)):
                if self.current_organism.fitness != new_organism.fitness:
                    self.iterations_without_change = 0
                else:
                    self.iterations_without_change += 1
                self.current_organism = new_organism
            else:
                self.iterations_without_change += 1

            if self.is_finished():
                break

        self.temperature *= ALPHA
        self.iterations_per_session = math.floor(
            self.iterations_per_session * BETA)

    def is_finished(self):
        return self.iterations_without_change >= NO_CHANGE_THRESHOLD

    @staticmethod
    def __get_initial_temperature():
        random_fitnesses = [
            Population.gen_random_org().fitness for _ in range(200)]
        output = standard_deviation(random_fitnesses)
        # print('INITIAL TEMPERATURE: ', output)
        return output
