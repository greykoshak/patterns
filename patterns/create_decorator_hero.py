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


class AbstractNegative(AbstractEffect, ABC):

    def get_negative_effects(self):
        negative_effects = self.base.get_negative_effects()
        if type(self).__name__ in ["Weakness", "EvilEye", "Curse"]:
            negative_effects.append(type(self).__name__)

        return negative_effects

    def get_positive_effects(self):
        positive_effects = self.base.get_positive_effects()
        if type(self).__name__ in ["Berserk", "Blessing"]:
            positive_effects.append(type(self).__name__)

        return positive_effects


class AbstractPositive(AbstractEffect, ABC):

    def get_positive_effects(self):
        positive_effects = self.base.get_positive_effects()
        if type(self).__name__ in ["Berserk", "Blessing"]:
            positive_effects.append(type(self).__name__)

        return positive_effects

    def get_negative_effects(self):
        negative_effects = self.base.get_negative_effects()
        if type(self).__name__ in ["Weakness", "EvilEye", "Curse"]:
            negative_effects.append(type(self).__name__)

        return negative_effects


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

        stats["HP"] += 50

        return stats


# Благословение — Увеличивает все основные характеристики на 2.

class Blessing(AbstractPositive):  # Благословение
    def get_stats(self):
        stats = self.base.get_stats()
        params = ["Strength", "Perception", "Endurance", "Charisma", "Intelligence", "Agility", "Luck"]

        for param in params:
            stats[param] += 2

        return stats


# Слабость — Уменьшает параметры Сила, Выносливость, Ловкость на 4.

class Weakness(AbstractNegative):  # Слабость
    def get_stats(self):
        stats = self.base.get_stats()
        params = ["Strength", "Endurance", "Agility"]

        for param in params:
            stats[param] -= 4

        return stats


# Сглаз — Уменьшает параметр Удача на 10.

class EvilEye(AbstractNegative):  # Сглаз
    def get_stats(self):
        stats = self.base.get_stats()
        params = ["Luck"]

        for param in params:
            stats[param] -= 10

        return stats


# Проклятье — Уменьшает все основные характеристики на 2.

class Curse(AbstractNegative):  # Проклятие
    def get_stats(self):
        stats = self.base.get_stats()
        params = ["Strength", "Perception", "Endurance", "Charisma", "Intelligence", "Agility", "Luck"]

        for param in params:
            stats[param] -= 2

        return stats


hero = Hero()
# print(hero.stats)
# print(hero.get_positive_effects())
# print(hero.get_negative_effects())
#
berserk = Berserk(hero)
# print(berserk.get_stats())
# print(berserk.get_positive_effects())
#
blessing = Blessing(berserk)
# print(blessing.get_stats())
print(blessing.get_positive_effects())
curse = Curse(blessing)
# print(curse.get_stats())
# print(curse.get_negative_effects())
# curse = curse.base
print("=============================")
print("N", curse.get_negative_effects())
print("P", curse.get_positive_effects())
print(curse.get_stats())
