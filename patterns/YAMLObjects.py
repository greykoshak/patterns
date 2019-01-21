# Переопределение from_yaml для добавления пользовательского тега YAML

# Подклассификация YAMLObject - это простой способ определить теги, конструкторы и
# представления для ваших классов. Вам нужно только переопределить атрибут yaml_tag.
# Если вы хотите определить свой собственный конструктор и репрезентатор, переопределите
# метод from_yaml и to_yaml соответственно.

import yaml

class Something(yaml.YAMLObject):
    yaml_tag = u'!Something'

    def __init__(self, *args, **kw):
        print('some_init', args, kw)

    @classmethod
    def from_yaml(cls,loader,node):
        # Set attributes to None if not in file
        values = loader.construct_mapping(node, deep=True)
        attr = ['attr1','attr2']
        result = {}
        for val in attr:
            try:
                result[val] = values[val]
            except KeyError:
                result[val] = None
        return cls(**result)

yaml_str = """\
test: !Something
   attr1: 1
   attr2: 2
"""

d = yaml.load(yaml_str)