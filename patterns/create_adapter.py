class Light:
    def __init__(self, dim):
        self.dim = dim
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]
        self.lights = []
        self.obstacles = []

    def set_dim(self, dim):
        self.dim = dim
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]

    def set_lights(self, lights):
        self.lights = lights
        self.generate_lights()

    def set_obstacles(self, obstacles):
        self.obstacles = obstacles
        self.generate_lights()

    def generate_lights(self):
        return self.grid.copy()


class System:
    def __init__(self):
        self.map = self.grid = [[0 for i in range(30)] for _ in range(20)]
        self.map[5][7] = 1  # Источники света
        self.map[5][2] = -1  # Стены

    def get_lightening(self, light_mapper):
        self.lightmap = light_mapper.lighten(self.map)


class MappingAdapter:

    def __init__(self, adaptee):
        self.adaptee = adaptee

    def _get_objects_by_grid(self, descriptor, grid):
        result = []
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == descriptor:
                    result.append(tuple([j, i]))
        return result

    def get_lights(self, grid):
        return self._get_objects_by_grid(1, grid)

    def get_obstacles(self, grid):
        return self._get_objects_by_grid(-1, grid)

    def lighten(self, grid):
        # set map's size
        dim = (len(grid[0]), len(grid))
        self.adaptee.set_dim(dim)

        # get lists of lights and obstacles
        lights = self.get_lights(grid)
        obstacles = self.get_obstacles(grid)

        # set lights and obstacles
        self.adaptee.set_obstacles(obstacles)
        self.adaptee.set_lights(lights)

        # get map of lighten
        return self.adaptee.generate_lights()


system = System()
light = Light((len(system.map[0]), len(system.map)))
print(len(system.map[0]), len(system.map))

adapter = MappingAdapter(light)
system.get_lightening(adapter)

# UPD: Все получилось. Моя ошибка была в порядке координат и лишнем коде.
# class MappingAdapter:
#     def __init__(self, adaptee):
#         self.adaptee = adaptee
#
#     def lighten(self, grid):
#         dim = (len(grid[0]), len(grid))
#         self.adaptee.set_dim(dim)
#
#         for i in range(len(grid)):
#             for j in range(len(grid[0])):
#                 if grid[i][j] is 1:
#                     self.adaptee.lights.append((i,j))
#                 elif grid[i][j] is -1:
#                     self.adaptee.obstacles.append((i,j))
#
#         for i in range(len(self.adaptee.grid)):
#             for j in range(len(self.adaptee.grid[0])):
#                 for i, j in self.adaptee.lights:
#                     self.adaptee.grid[i][j] = 1
#                 for i, j in self.adaptee.obstacles:
#                     self.adaptee.grid[i][j] = -1
#
#         return self.adaptee.generate_lights()
#
#
# class MappingAdapter():
#     def __init__(self, adaptee):
#         self.adaptee = adaptee
#
#     '''Создаю список препятствий или источников света. Если 1 - источники света если -1 - препятствия. Если значение в точке с некоторыми координатами равно заданому, добавляю в список эти координаты (в виде кортежа). Метод возвращает список кортежей.'''
#
#     def obj_map(self, grid, lights=True):
#         if lights:
#             key = 1  # источники света
#         else:
#             key = -1  # препятствия
#         the_list = []
#
#         # Если значение в точке с некоторыми координатами равно заданому, добавляю в список эти координаты.
#         for i in range(len(grid)):
#             for j in range(len(grid[0])):
#                 if grid[i][j] == key:
#                     the_list.append(i, j)
#         return the_list
#
#     def lighten(self, grid):
#
#         # устанавливаю размер карты
#         dim = (len(grid[0]), len(grid))
#         self.adaptee.set_dim(dim)
#
#         # получаю списки препятствий и источников света
#         obsts = self.obj_map(grid, False)
#         lts = self.obj_map(grid, True)
#
#         # передаю списки препятствий и объектов адаптируемому классу Light
#         self.adaptee.set_obstacles(obsts)
#         self.adaptee.set_lights(lts)
#
#         # получаю карту освещённости от Light
#         return self.adaptee.generate_lights()
#
# # Боровенский Николай Васильевич
# # разделение логики с понятными названиями уже сделает лучше с точки зрения чистого кода:
# def _get_objects_by_grid(self, descriptor, grid):
#     result = []
#     for i in range(len(grid)):
#         for j in range(len(grid[0])):
#             if grid[i][j] == descriptor:
#                 result.append(i, i)
#     return result
#
# def get_lights(self, grid):
#     return self._get_objects_by_grid(1, grid)
#
# def get_obstacles(self, grid):
#     return self._get_objects_by_grid(-1, grid)
#
# Можно применить каррирование, в питоне это легко. Можно Enum для 1 и -1. Добавить typing и т.д.
# Ну и, во-вторых, ошибка у Вас на строчке 17.
# С append так нельзя как у Вас в коде (возможно это описка). Передавайте кортеж.
# Обратите внимание на условие задачи:
# В каждом элементе кортежа хранятся 2 значения: elem[0] -- координата по ширине карты и elem[1] -- координата по высоте соответственно
# Здесь разгадка 🙂

# UPD. Не, всё фигня. Оказалось, что нужно тщательнее следить за порядком координат.
# Да, ошибка (была) действительно именно в той строчке, о которой Вы написали.
# Выходит, что здесь: "В каждом элементе кортежа...". Написано неверно.
# Судя по всему, имелось в виду "В каждом кортеже (элементе списка)...".
