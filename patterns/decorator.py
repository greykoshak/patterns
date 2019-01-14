from abc import ABC, abstractmethod

class Creature(ABC):

    @abstractmethod
    def feed(self):
        pass

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def make_noise(self):
        pass

class Animal(Creature):
    def feed(self):
        print("I eat grass")

    def move(self):
        print("I walk forward")

    def make_noise(self):
        print("Wooooo!")

animal = Animal()
# animal.feed()

class AbstractDecorator(Creature):
    def __init__(self, base):
        self.base = base

    def feed(self):
        self.base.feed()

    def move(self):
        self.base.move()

    def make_noise(self):
        self.base.make_noise()

class Swimming(AbstractDecorator):
    def move(self):
        print("I'm swimming")

    def make_noise(self):
        print("...")

class Predator(AbstractDecorator):
    def feed(self):
        print("I eat other animals")

class Fast(AbstractDecorator):
    def move(self):
        self.base.move()
        print("Fast")

animal.feed()
animal.move()
animal.make_noise()
print()

swimming = Swimming(animal)
swimming.feed()
swimming.move()
swimming.make_noise()
print()

predator = Predator(swimming)
predator.feed()
predator.move()
predator.make_noise()
print()

fast = Fast(predator)
fast.move()
fast.feed()
fast.make_noise()

print("Faster")
faster = Fast(fast)
faster.move()

print(faster.base)
print(faster.base.base)

faster.base.base = faster.base.base.base
print(faster.base.base)
