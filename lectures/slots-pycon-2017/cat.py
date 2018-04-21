# from memory_profiler import profile


class Cat(object):
    """A cat."""

    species = "Cat"

    def __init__(self, fur_color):
        self.fur_color = fur_color

    def hunt_for_mice(self):
        self.hunting = True  # a new attribute!


class FurCat(object):
    """A lighter cat."""

    __slots__ = ('fur_color',)
    species = "Cat"

    def __init__(self, fur_color):
        self.fur_color = fur_color

    def hunt_for_mice(self):
        self.hunting = True  # AttributeError


# @profile
def make_lots_of_cats():
    s = list()
    u = list()
    for i in range(10000):
        s.append(Cat("black"))
    for j in range(10000):
        u.append(FurCat("black"))


if __name__ == "__main__":
    make_lots_of_cats()
    princess = Cat("black")
    queen = FurCat("black")


