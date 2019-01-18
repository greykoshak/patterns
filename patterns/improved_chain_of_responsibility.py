# Паттерн "Абстрактная фабрика"
# 1. Объявим абстрактную фабрику
# Обявим методы, которые позволят создать персонажа. Используем механизм classmethod

class HeroFactory:
    @classmethod
    def create_hero(Class, name):
        return Class.Hero(name)

    @classmethod
    def create_weapon(Class):
        return Class.Weapon()

    @classmethod
    def create_spell(Class):
        return Class.Spell()

# 2. Определим конкретные фабрики
# В каждой конкретной фабрике объявим собственные классы героя, оружия и заклинаний,
# которые будут специфичны для класса персонажа

class WariorFactory(HeroFactory):
    class Hero:
        def __init__(self, name):
            self.name = name
            self.weapon = None
            self.armor = None
            self.spell = None

        def add_weapon(self, weapon):
            self.weapon = weapon

        def add_spell(self, spell):
            self.spell = spell

        def hit(self):
            print(f"Warior hits with {self.weapon.hit()}")
            self.weapon.hit()

        def cast(self):
            print(f"Warior casts {self.spell.cast()}")
            self.spell.cast()

    class Weapon:
        def hit(self):
            return "Claymore"

    class Spell:
        def cast(self):
            return "Power"


class MageFactory(HeroFactory):
    class Hero:
        def __init__(self, name):
            self.name = name
            self.weapon = None
            self.armor = None
            self.spell = None

        def add_weapon(self, weapon):
            self.weapon = weapon

        def add_spell(self, spell):
            self.spell = spell

        def hit(self):
            print(f"Mage hits with {self.weapon.hit()}")
            self.weapon.hit()

        def cast(self):
            print(f"Mage casts {self.spell.cast()}")
            self.spell.cast()

    class Weapon:
        def hit(self):
            return "Staff"

    class Spell:
        def cast(self):
            return "Fireball"


class AssassinFactory(HeroFactory):
    class Hero:
        def __init__(self, name):
            self.name = name
            self.weapon = None
            self.armor = None
            self.spell = None

        def add_weapon(self, weapon):
            self.weapon = weapon

        def add_spell(self, spell):
            self.spell = spell

        def hit(self):
            print(f"Assassin hits with {self.weapon.hit()}")
            self.weapon.hit()

        def cast(self):
            print(f"Assassin casts {self.spell.cast()}")

    class Weapon:
        def hit(self):
            return "Dagger"

    class Spell:
        def cast(self):
            return "Invisibility"

# 3. Определим функцию, создающую персонажей
# Она не отличается от базовой реализации

def create_hero(factory):
    hero = factory.create_hero("Nagibator")

    weapon = factory.create_weapon()
    spell = factory.create_spell()

    hero.add_weapon(weapon)
    hero.add_spell(spell)

    return hero

# 4. Попробуем создать персонажей различных классов
# Попробуем создать персонажей различных классов, передавая функции назличные фабрики.

player = create_hero(AssassinFactory)
player.cast()
player.hit()
print()

player = create_hero(MageFactory)
player.cast()
player.hit()
print()

player = create_hero(WariorFactory)
player.cast()
player.hit()