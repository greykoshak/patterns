# Использование yaml
import yaml  # pip3 install pyyaml
import pprint

# Опишем конфигурацию, описывающую создание персонажа

hero_yaml = '''
--- !Character
factory:
  !factory mage
name:
  77NaGiBaToR77
'''

# Используем абстрактную фабрику, использование которой будем конфигурировать

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


class WarriorFactory(HeroFactory):
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
            print(f"Warrior {self.name} hits with {self.weapon.hit()}")
            self.weapon.hit()

        def cast(self):
            print(f"Warrior {self.name} casts {self.spell.cast()}")
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
            print(f"Mage {self.name} hits with {self.weapon.hit()}")
            self.weapon.hit()

        def cast(self):
            print(f"Mage {self.name} casts {self.spell.cast()}")
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
            print(f"Assassin {self.name} hits with {self.weapon.hit()}")
            self.weapon.hit()

        def cast(self):
            print(f"Assassin {self.name} casts {self.spell.cast()}")

    class Weapon:
        def hit(self):
            return "Dagger"

    class Spell:
        def cast(self):
            return "Invisibility"

# Опишем конструктор, который сможет обрабатывать узел !factory. Он будет возвращать соответствующую фабрику.
#
# Конструктор должен принимать 2 аргумента: loader и node. Объект loader — это загрузчик YAML, node — узел файла.
# Поскольку структура YAML-файла древовидная, то при первичном проходе обработчиком всё содержимое файла помещается
# в древовидную структуру, содержащую информацию файла в текстовом виде. node является узлом именно такого
# текстового дерева, а loader — загрузчик умеющий обрабатывать node. По итогу, ниже следующий конструктор
# factory_constructor будет являться частью loader и будет вызываться им по необходимости.
#
# Для описанного выше YAML-файла: loader — загрузчик, «знакомый» с данным конструктором;
# node — хранит текст assassin (информация, хранящаяся за именем пользовательского типом !factory) и различную
# дополнительную информацию. Поскольку assassin — простой скаляр, то для его получения (без дополнительной информации)
# необходимо воспользоваться методом construct_scalar. Если бы после !factory располагался список, то необходимо
# было бы воспользоваться методом construct_sequenc и т.д.

def factory_constructor(loader, node):
    data = loader.construct_scalar(node)
    print(node, data)

    if data == "mage":
        return MageFactory
    elif data == "warrior":
        return WarriorFactory
    else:
        return AssassinFactory

# Опишем класс Character, в который будут загружаться данные из yaml. Определим у него метод create_hero,
# позволяющий создать персонажа в соответствии с конфигурацией.

class Character(yaml.YAMLObject):
    yaml_tag = "!Character"

    def create_hero(self):
        hero = self.factory.create_hero(self.name)

        weapon = self.factory.create_weapon()
        spell = self.factory.create_spell()

        hero.add_weapon(weapon)
        hero.add_spell(spell)

        return hero

# Присоединим конструктор и создадим персонажа в соответствии с yaml-конфигурацией.
# yaml.add_constructor(u'!code', code_constructor)
# value = loader.construct_mapping(node)

loader = yaml.Loader
loader.add_constructor("!factory", factory_constructor)

character = yaml.load(hero_yaml)

print("\nLoad class Character")
pp = pprint.PrettyPrinter(indent=40)
pp.pprint(character)
print(character.factory)
print(character.name)
print()

hero = yaml.load(hero_yaml).create_hero()
hero.hit()
hero.cast()

print("------------------------------------\n")
"""
1. loader = yaml.Loader                                    # define loader YAML-document
2. loader.add_constructor("!factory", factory_constructor) # add constructor for tag "!factory"
3. character = yaml.load(hero_yaml)                        # create class Character (include yaml_tag = "!Character"
4. hero = yaml.load(hero_yaml).create_hero()               # call method create.hero() of class Character
5. hero.hit(), hero.cast()                                 # add properties
"""