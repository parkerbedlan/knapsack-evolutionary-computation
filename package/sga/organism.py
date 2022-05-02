from random import randint
from package.constants import CAPACITY, ITEMS, MUTATION_OPERATOR, AsBit, Bit


class Organism:
    chromosome: list[Bit]
    fitness: int    # always updated based on chromosome

    def __init__(self, chromosome: list[Bit]) -> None:
        self.chromosome = chromosome
        self.__update_fitness()

    def mutate(self) -> None:
        def bitflip(self: Organism) -> None:
            index = randint(1, len(self.chromosome)) - 1
            self.chromosome[index] = (self.chromosome[index] + 1) % 2

        def bitflip_bo3(self: Organism) -> None:
            chromosomes = [self.chromosome.copy() for _ in range(3)]
            organisms: list[Organism] = []
            for i in range(3):
                index = randint(1, len(self.chromosome)) - 1
                chromosomes[i][index] = AsBit((self.chromosome[index] + 1) % 2)
                organisms.append(Organism(chromosomes[i]))
            self.chromosome = max(organisms).chromosome

        def pairwise_exchange(self: Organism) -> None:
            index1 = randint(0, len(self.chromosome) - 1)
            index2 = randint(0, len(self.chromosome) - 1)
            while index2 == index1:
                index2 = randint(0, len(self.chromosome) - 1)
            temp = self.chromosome[index1]
            self.chromosome[index1] = self.chromosome[index2]
            self.chromosome[index2] = temp

        mutation_operators = {'bit flip': bitflip,
                              'bit flip best of 3': bitflip_bo3, 'PE': pairwise_exchange}
        mutation_operators[MUTATION_OPERATOR](self)
        self.__update_fitness()

    def get_total_value(self) -> int:
        total_weight, total_value = self.__get_total_weight_and_value()
        if total_weight > CAPACITY:
            return 0
        return total_value

    def __str__(self):
        return ''.join([str(x) for x in self.chromosome]) + ' ' + str(self.fitness)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Organism):
            return NotImplemented
        return self.fitness < other.fitness

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Organism):
            return NotImplemented
        return self.fitness > other.fitness

    def __update_fitness(self) -> None:
        total_weight, total_value = self.__get_total_weight_and_value()

        remaining_weight = CAPACITY - total_weight
        # experiment with the deduction multiplier, 4 may be better than 5
        if remaining_weight < 0:
            deduction = 5 * remaining_weight
        else:
            deduction = 0

        self.fitness = total_value + deduction

    def __get_total_weight_and_value(self) -> tuple[int, int]:
        total_weight = 0
        total_value = 0
        for i in range(len(ITEMS)):
            if self.chromosome[i] == 1:
                total_weight += ITEMS[i].weight
                total_value += ITEMS[i].value

        return total_weight, total_value
