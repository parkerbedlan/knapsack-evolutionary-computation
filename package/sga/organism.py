from random import randint
from package.constants import CAPACITY, ITEMS, MUTATION_OPERATOR, Bit


class Organism:
    chromosome: list[Bit]
    fitness: int    # always updated based on chromosome


    def __init__(self, chromosome: list[Bit]) -> None:
        self.chromosome = chromosome
        self.__update_fitness()
    

    def __str__(self):
        return ''.join([str(x) for x in self.chromosome]) + ' ' + str(self.fitness)
    

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Organism):
            return NotImplemented
        return self.fitness < other.fitness


    def __update_fitness(self) -> None:
        total_weight = 0
        total_value = 0    
        for i in range(len(ITEMS)):
            if self.chromosome[i] == 1:
                total_weight += ITEMS[i].weight
                total_value += ITEMS[i].value
        
        remaining_weight = CAPACITY - total_weight
        # experiment with whether to make this conditional
        if remaining_weight < 0:
            deduction = 5 * remaining_weight
        else:
            deduction = 0
        
        self.fitness = total_value + deduction


    def mutate(self) -> None:
        mutation_operators = {'bit flip': self.__bitflip}
        mutation_operators[MUTATION_OPERATOR]()
        self.__update_fitness()
    

    def __bitflip(self) -> None:
        index = randint(1, len(self.chromosome)) - 1
        self.chromosome[index] = (self.chromosome[index] + 1) % 2