from typing import Literal
from package.item import Item

# general settings
DATASET_NAME: str = 'toy.dat'
MUTATION_OPERATOR: Literal['bit flip',
                           'bit flip best of 3', 'PE'] = 'PE'
MODE: Literal['GA', 'Climbing'] = 'GA'


# GA settings
SELECTION_OPERATOR: Literal['tournament', 'roulette'] = 'roulette'
TOURNAMENT_K: float = .85   # only used if SELECTION_OPERATOR is 'tournament'
MUTATION_RATE: float = .15
CROSSOVER_OPERATOR: Literal['uniform',
                            'single point', 'double point'] = 'single point'
CROSSOVER_RATE: float = 1
PRINT_BEST_FITNESS_RATE: int = -1    # -1 means never
ELITISM_AMOUNT = 2
# -1 means no generation threshold (could lead to infinite loop)
# 2*(POPULATION_SIZE**2) seems to be pretty good
POPULATION_SIZE: int = 100  # 20 for testing, 100 for real deal
GENERATION_THRESHOLD: int = 20000  # 800 for testing, 20000 for real deal

# SA / FHC settings
FOOLISH_MODE: bool = True
ALPHA: float = .98  # cooling coefficient
I_0: int = 10     # initial amount of iterations between each cooling
BETA: float = 1.02  # multiplier for amount of iterations between cooling
# threshold for how many iterations in a row lead to no change before quitting
NO_CHANGE_THRESHOLD: int = 20000
# threshold for temperature to quit simulated annealing
# TEMPERATURE_THRESHOLD: int = 1


# misc constants (not settings)
class NotYetImplementedException(Exception):
    def __init__(self) -> None:
        super().__init__('Not yet implemented')


Bit = Literal[0, 1]


def AsBit(before: int) -> Bit:
    return 0 if before == 0 else 1


def _parse_dataset() -> tuple[int, list[Item], int]:
    items: list[Item] = []
    with open('package/datasets/%s' % DATASET_NAME, 'r') as file:
        CAPACITY = int(file.readline())
        OPTIMAL = int(file.readline())
        for line in file.readlines():
            weight, value = [int(x) for x in line.split()]
            items.append(Item(weight, value))
    ITEMS = items
    return CAPACITY, ITEMS, OPTIMAL


CAPACITY, ITEMS, OPTIMAL = _parse_dataset()
