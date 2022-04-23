class Item:
    weight: int
    value: int

    def __init__(self, weight: int, value: int):
        self.weight = weight
        self.value = value
    
    def __str__(self):
        return 'w%sv%s' % (self.weight, self.value)