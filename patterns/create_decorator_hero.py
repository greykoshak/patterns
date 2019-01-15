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
        self.base.get_stats()

    def get_positive_effects(self):
        self.base.get_positive_effects()

    def get_negative_effects(self):
        self.base.get_negative_effects()


class AbstractPositive(AbstractEffect):
    pass


# Берсерк — Увеличивает параметры Сила, Выносливость, Ловкость, Удача на 7;
# уменьшает параметры Восприятие, Харизма, Интеллект на 3.
# Количество единиц здоровья увеличивается на 50.

class Berserk(AbstractPositive):

    def get_stats(self):
        stats = self.base.get_stats()
        params = ["Strength", "Endurance", "Agility", "Luck"]

        for param in params:
            stats[param] += 7

        params = ["Perception", "Charisma", "Intelligence"]

        for param in params:
            stats[param] -= 3
            stats[param] = 0 if stats[param] < 0 else stats[param]

        stats["HP"] += 50

        return stats.copy()

    def get_positive_effects(self):
        positive_effects = self.base.get_positive_effects()
        positive_effects.append("Berserk")

        return positive_effects


# Благословение — Увеличивает все основные характеристики на 2.

class Blassing(AbstractPositive):  # Благословение
    def get_stats(self):
        stats = self.base.get_stats()
        params = ["Strength", "Perception", "Endurance", "Charisma", "Intelligence", "Agility", "Luck"]

        for param in params:
            stats[param] += 2

        return stats.copy()

    def get_positive_effects(self):
        positive_effects = self.base.get_positive_effects()
        positive_effects.append("Blassing")

        return positive_effects


class AbstarctNegative(AbstractEffect):
    pass


# Слабость — Уменьшает параметры Сила, Выносливость, Ловкость на 4.

class Weakness(AbstarctNegative):  # Слабость
    def get_stats(self):
        stats = self.base.get_stats()
        params = ["Strength", "Endurance", "Agility"]

        for param in params:
            stats[param] -= 4
            stats[param] = 0 if stats[param] < 0 else stats[param]

        return stats.copy()

    def get_negative_effects(self):
        negative_effects = self.base.get_negative_effects()
        negative_effects.append("Weakness")

        return negative_effects


# Сглаз — Уменьшает параметр Удача на 10.

class EvilEye(AbstarctNegative):  # Сглаз
    def get_stats(self):
        stats = self.base.get_stats()
        params = ["Luck"]

        for param in params:
            stats[param] -= 10
            stats[param] = 0 if stats[param] < 0 else stats[param]

        return stats.copy()

    def get_negative_effects(self):
        negative_effects = self.base.get_negative_effects()
        negative_effects.append("EvilEye")

        return negative_effects


# Проклятье — Уменьшает все основные характеристики на 2.

class Curse(AbstarctNegative):  # Проклятие
    def get_stats(self):
        stats = self.base.get_stats()
        params = ["Strength", "Perception", "Endurance", "Charisma", "Intelligence", "Agility", "Luck"]

        for param in params:
            stats[param] -= 2
            stats[param] = 0 if stats[param] < 0 else stats[param]

        return stats.copy()

    def get_negative_effects(self):
        negative_effects = self.base.get_negative_effects()
        negative_effects.append("Curse")

        return negative_effects


hero = Hero()
print(hero.stats)

berserk = Berserk(hero)
print(berserk.get_stats())
print(berserk.get_positive_effects())

blassing = Blassing(berserk)
print(blassing.get_stats())
print(blassing.get_positive_effects())
