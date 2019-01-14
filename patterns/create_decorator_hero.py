from abc import ABC


class Hero:
    def __init__(self):
        self.positive_effects = []
        self.negative_effects = []

        self.stats = {
            "HP": 128,
            "MP": 42,
            "SP": 100,

            "Strength": 15,
            "Perception": 4,
            "Endurance": 8,
            "Charisma": 2,
            "Intelligence": 3,
            "Agility": 8,
            "Luck": 1
        }

    def get_positive_effects(self):
        return self.positive_effects.copy()

    def get_negative_effects(self):
        return self.negative_effects.copy()

    def get_stats(self):
        return self.stats.copy()


class AbstractEffect(Hero, ABC):
    def __init__(self, base):
        self.base = base

    def get_stats(self):  # Возвращает итоговые характеристики применения эффекта
        pass

    def get_positive_effects(self):
        pass

    def get_negative_effects(self):
        pass

class AbstarctPositive(AbstractEffect):
    pass

class Berserk(AbstarctPositive):
    pass

class Blassing(AbstarctPositive):  # Благословение
    pass

class AbstarctNegative(AbstractEffect):
    pass

class Weakness(AbstarctNegative):  # Слабость
    pass

class EvilEye(AbstarctNegative):   # Сглаз
    pass

class Curse(AbstarctNegative):     # Проклятие
    pass
