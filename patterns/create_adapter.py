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
    def __init__(self, adaptee):  # (18, 8)
        self.adaptee = adaptee
        self.adaptee.lights = [(8, 2), (18, 6)]
        self.adaptee.obstacles = [(7, 1), (7, 2), (7, 3), (7, 5), (7, 6), (7, 7), (7, 8), (8, 5), (9, 5),
                                  (11, 5), (12, 5), (13, 5), (14, 5), (14, 4), (14, 3)]

    def lighten(self, grid):
        self.adaptee.set_dim(grid)
        self.adaptee.set_lights(self.adaptee.lights)
        self.adaptee.set_obstacles(self.adaptee.obstacles)

        return self.adaptee.generate_lights()

system = System()
light = Light((18, 8))
adapter = MappingAdapter(light)
system.get_lightening(adapter)

# UPD: Все получилось. Моя ошибка была в порядке координат и лишнем коде.
class MappingAdapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def lighten(self, grid):
        dim = (len(grid[0]), len(grid))
        self.adaptee.set_dim(dim)

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] is 1:
                    self.adaptee.lights.append((i,j))
                elif grid[i][j] is -1:
                    self.adaptee.obstacles.append((i,j))

        for i in range(len(self.adaptee.grid)):
            for j in range(len(self.adaptee.grid[0])):
                for i, j in self.adaptee.lights:
                    self.adaptee.grid[i][j] = 1
                for i, j in self.adaptee.obstacles:
                    self.adaptee.grid[i][j] = -1

        return self.adaptee.generate_lights()