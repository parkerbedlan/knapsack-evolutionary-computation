from random import randint, random
from package.sga.organism import Organism
from package.constants import CROSSOVER_OPERATOR, CROSSOVER_RATE, ELITISM_AMOUNT, ITEMS, MUTATION_RATE, POPULATION_SIZE, SELECTION_OPERATOR, AsBit, Bit


class Population:
    generation_number: int
    organisms: list[Organism]  # always sorted in order of fitness
    best_organism_ever: Organism  # always updated

    def __init__(self):
        self.generation_number = 0
        self.organisms = [Population.gen_random_org()
                          for _ in range(POPULATION_SIZE)]
        self.organisms.sort()
        self.best_organism_ever = self.get_best_organism()

    def perform_generation(self) -> None:
        self.generation_number += 1

        mutated_children: list[Organism] = []

        elites = self.__get_elites()
        for elite in elites:
            mutated_children.append(elite)

        parents: list[Organism] = self.__select_parents()
        while len(mutated_children) < POPULATION_SIZE:
            parent1 = parents[randint(1, len(parents)) - 1]
            parent2 = parents[randint(1, len(parents)) - 1]
            if random() < CROSSOVER_RATE:
                child1, child2 = Population.__crossover(parent1, parent2)
                mutated_children.append(child1)
                mutated_children.append(child2)
            else:
                mutated_children.append(parent1)
                mutated_children.append(parent2)

        for child in mutated_children:
            if random() < MUTATION_RATE:
                child.mutate()

        self.organisms = mutated_children
        self.organisms.sort()

        self.best_organism_ever = max(
            self.best_organism_ever, self.get_best_organism())

    def is_finished(self):
        best_fitness = self.get_best_fitness()
        worst_fitness = self.get_worst_fitness()
        difference = abs(best_fitness - worst_fitness)
        less_than_1percent_difference = difference < .01 * \
            min(abs(best_fitness), abs(worst_fitness))
        return less_than_1percent_difference or self.generation_number >= 1000

    def get_best_organism(self) -> Organism:
        return self.organisms[-1]

    def get_best_fitness(self) -> int:
        return self.organisms[-1].fitness

    def get_worst_fitness(self) -> int:
        return self.organisms[0].fitness

    @staticmethod
    def __crossover(parent1: Organism, parent2: Organism) -> tuple[Organism, Organism]:
        def uniform(parent1: Organism, parent2: Organism) -> tuple[Organism, Organism]:
            mask = Population.__gen_random_bitstring(len(parent1.chromosome))
            chromosome1: list[Bit] = []
            chromosome2: list[Bit] = []
            for i in range(len(mask)):
                if mask[i] == 0:
                    chromosome1.append(parent1.chromosome[i])
                    chromosome2.append(parent2.chromosome[i])
                else:
                    chromosome1.append(parent2.chromosome[i])
                    chromosome2.append(parent1.chromosome[i])
            return Organism(chromosome1), Organism(chromosome2)

        crossover_operators = {'uniform': uniform}
        return crossover_operators[CROSSOVER_OPERATOR](parent1, parent2)

    def __get_elites(self) -> list[Organism]:
        elites: list[Organism] = []
        for i in range(1, ELITISM_AMOUNT+1):
            elites.append(self.organisms[-i])
        return elites

    def __select_parents(self) -> list[Organism]:
        def roulette(self: Population) -> list[Organism]:
            # add constant to all fitness values so they are all positive
            lowest_fitness = self.get_worst_fitness()
            shifter: int = 0
            if lowest_fitness <= 0:
                shifter = abs(lowest_fitness) + 1
            shifted_fitnesses = list(
                map(lambda x: x + shifter, [org.fitness for org in self.organisms]))
            total_fitness = sum(shifted_fitnesses)

            parents: list[Organism] = []
            for _ in range(POPULATION_SIZE - ELITISM_AMOUNT):
                spin = randint(1, total_fitness)
                for i in range(len(shifted_fitnesses)):
                    spin -= shifted_fitnesses[i]
                    if spin <= 0:
                        parents.append(self.organisms[i])
                        break
            return parents

        def rank(self: Population) -> list[Organism]:
            return NotImplemented

        def tournament(self: Population) -> list[Organism]:
            return NotImplemented

        selection_operators = {
            'roulette': roulette, 'rank': rank, 'tournament': tournament}  # type: ignore
        return selection_operators[SELECTION_OPERATOR](self)

    @staticmethod
    def gen_random_org() -> Organism:
        return Organism(Population.__gen_random_bitstring(len(ITEMS)))

    @staticmethod
    def __gen_random_bitstring(length: int) -> list[Bit]:
        return [AsBit(randint(0, 1)) for _ in range(length)]
