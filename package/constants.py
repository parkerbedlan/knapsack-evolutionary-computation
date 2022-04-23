from typing import Literal
from package.item import Item


class NotYetImplementedException(Exception):
    def __init__(self) -> None:
        super().__init__('Not yet implemented')


Bit = Literal[0,1]

def AsBit(before: int) -> Bit:
    return 0 if before == 0 else 1


DATASET_NAME: str = 'p08.dat'
SELECTION_OPERATOR: Literal['tournament', 'roulette', 'rank']  = 'roulette'
MUTATION_OPERATOR: Literal['bit flip', 'bit flip best of 3', 'PE', 'C3', 'SM'] = 'bit flip'
MUTATION_RATE: float = .05
CROSSOVER_OPERATOR: Literal['uniform', 'single point', 'double point'] = 'uniform'
CROSSOVER_RATE: float = 1
POPULATION_SIZE: int = 400
PRINT_BEST_FITNESS_RATE: int = 0        # 0 means never
ELITISM_AMOUNT = 2


def _parse_dataset() -> tuple[int, list[Item]]:
    items: list[Item] = []
    with open('package/datasets/%s' % DATASET_NAME, 'r') as file:
        CAPACITY = int(file.readline())
        for line in file.readlines():
            weight, value = [int(x) for x in line.split()]
            items.append(Item(weight, value))
    ITEMS = items
    return CAPACITY, ITEMS

CAPACITY, ITEMS = _parse_dataset()