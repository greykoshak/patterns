from abc import ABC, abstractmethod

# 1. Объявим абстрактый класс фабрики
# Обявим методы, которые позволят создать персонажа, а также оружие и заклинание для него.

class HeroFactory(ABC):
    @abstractmethod
    def create_hero(self, name):
        pass

    @abstractmethod
    def create_weapon(self):
        pass

    @abstractmethod
    def create_spell(self): # Заклинание
        pass

# 2. Определим конкретные фабрики
# Оределим конкретные фабрики и необходимые классы, для каждого из классов персонажей

class WarriorFactory(HeroFactory):
    def create_hero(self, name):
        return Warrior(name)

    def create_weapon(self):
        return Claymore()

    def create_spell(self):
        return Power()


class Warrior:
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
        print(f"Warrior {self.name} hits with {self.weapon.hit()}")
        self.weapon.hit()

    def cast(self):
        print(f"Warrior {self.name} casts {self.spell.cast()}")
        self.spell.cast()


class Claymore:
    def hit(self):
        return "Claymore"


class Power:
    def cast(self):
        return "Power"


class MageFactory(HeroFactory):
    def create_hero(self, name):
        return Mage(name)

    def create_weapon(self):
        return Staff()

    def create_spell(self):
        return Fireball()


class Mage:
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
        print(f"Mage {self.name} hits with {self.weapon.hit()}")
        self.weapon.hit()

    def cast(self):
        print(f"Mage {self.name} casts {self.spell.cast()}")
        self.spell.cast()


class Staff:
    def hit(self):
        return "Staff"


class Fireball:
    def cast(self):
        return "Fireball"


class AssassinFactory(HeroFactory):
    def create_hero(self, name):
        return Assassin(name)

    def create_weapon(self):
        return Dagger()

    def create_spell(self):
        return Invisibility()


class Assassin:
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
        print(f"Assassin {self.name} hits with {self.weapon.hit()}")
        self.weapon.hit()

    def cast(self):
        print(f"Assassin {self.name} casts {self.spell.cast()}")


class Dagger:
    def hit(self):
        return "Dagger"


class Invisibility:
    def cast(self):
        return "Invisibility"

# 3. Определим функцию, создающую персонажей
# Определим функцию, зависящую от фабрики. Данная функция будет создавать прсонажа и его экипировку в зависимости
# от фабрики, которая будет передаваться в качестве аргумента.

def create_hero(factory):
    hero = factory.create_hero("Nagibator")

    weapon = factory.create_weapon()
    ability = factory.create_spell()

    hero.add_weapon(weapon)
    hero.add_spell(ability)

    return hero

# 4. Попробуем создать персонажей различных классов
# Попробуем создать персонажей различных классов, передавая функции назличные фабрики.

factory = AssassinFactory()
player = create_hero(factory)
player.cast()
player.hit()
print()

factory = MageFactory()
player = create_hero(factory)
player.cast()
player.hit()