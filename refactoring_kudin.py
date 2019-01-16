import random
import math

import pygame


SCREEN_DIM = (800, 600)


class Vec2d:
    # Точность сравнения векторов
    EPS = 3

    # Инициализация вектора по его началу (x) и концу (y) или по его координатам
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Сложение с другим вектором
    def __add__(self, other):
        return Vec2d(self.x + other.x, self.y + other.y)

    # Вычитание другого вектора
    def __sub__(self, other):
        return Vec2d(self.x - other.x, self.y - other.y)

    # Скалярное произведение векторов или умножение на число
    def __mul__(self, other):
        # Пробуем скалярное умножение векторов.
        # Если будет выброшено исключение - пробуем умножение на число
        try:
            return self.x * other.x + self.y * other.y
        except AttributeError:
            pass
        return Vec2d(self.x * other, self.y * other)

    # Сравнение на равенство с другим вектором.
    # Если округлённые до целых координаты равны, то и векторы равны
    def __eq__(self, other):
        if math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2) < self.EPS:
            return True

        return False

        # Вычисление длины вектора через len.
        # ВНИМАНИЕ: функция должна возвращать int, иначе будет происходить падение,
        # поэтому происходит округление до целого.
    def __len__(self):
        return int(math.sqrt(self.x ** 2 + self.y ** 2))

    # Возвращает пару координат, округлённых до целых
    def int_pair(self):
        return int(self.x), int(self.y)


class Polyline:
    def __init__(self, display):
        self._display = display
        self._points = []
        self._steps = 35
        self._curve_points = []

    @property
    def steps(self):
        return self._steps

    @steps.setter
    def steps(self, value):
        if value >= 1:
            self._steps = value

    # Проверка на наличие точки. None если точки нет, иначе возвращает её номер
    def contains(self, point):
        tmp_point = Vec2d(point[0], point[1])
        for point_num in range(len(self._points)):
            if self._points[point_num]["point"] == tmp_point:
                return point_num

        return None

    # Добавление точки вместе со скоростью
    def append_point(self, point, speed):
        self._points.append({
            "point": Vec2d(point[0], point[1]),
            "speed": Vec2d(speed[0], speed[1])
        })

        self._curve_points = self._curve_points_preprocessor()

    def remove_point(self, point_num):
        del self._points[point_num]

        self._curve_points = self._curve_points_preprocessor()

    # Пересчитывание координат опорных точек
    def set_points(self):
        for point_num in range(len(self._points)):
            point = self._points[point_num]["point"]
            speed = self._points[point_num]["speed"]

            new_point = point + speed
            new_speed = speed

            if new_point.x > SCREEN_DIM[0] or new_point.x < 0:
                new_speed = Vec2d(-new_speed.x, new_speed.y)
            if new_point.y > SCREEN_DIM[1] or new_point.y < 0:
                new_speed = Vec2d(new_speed.x, -new_speed.y)

            self._points[point_num] = {
                "point": new_point,
                "speed": new_speed
            }

        self._curve_points = self._curve_points_preprocessor()

    def speed_up(self):
        for point_num in range(len(self._points)):
            speed = self._points[point_num]["speed"]
            speed.x = self._speed_up_coord(speed.x)
            speed.y = self._speed_up_coord(speed.y)
            self._points[point_num]["speed"] = speed

    def speed_down(self):
        for point_num in range(len(self._points)):
            speed = self._points[point_num]["speed"]
            speed.x = self._speed_down_coord(speed.x)
            speed.y = self._speed_down_coord(speed.y)
            self._points[point_num]["speed"] = speed

    # Прорисовка ломаной
    def draw_points(self, style="points", width=3, color=(255, 255, 255)):
        if style == "points":
            for point in self._points:
                pygame.draw.circle(self._display, color, point["point"].int_pair(), width)
        elif style == "line":
            for point_num in range(-1, len(self._curve_points) - 1):
                pygame.draw.line(self._display, color, self._curve_points[point_num].int_pair(),
                                 self._curve_points[point_num + 1].int_pair(), width)

    def _curve_points_preprocessor(self):
        result = list()
        for point in self._points:
            result.append(point["point"])

        return result

    def _speed_up_coord(self, value):
        if value < 0:
            return value - 1.0

        return value + 1.0

    def _speed_down_coord(self, value):
        if value < 0:
            return value + 1.0

        return value - 1.0


# get_knot ВЫЗЫВАЕТСЯ как препроцессор self._curved_points!
# Э­то позволило просто расширить класс Polyline с перегрузкой метода _curve_points_preprocessor
class Knot(Polyline):
    def __init__(self, display):
        super().__init__(display)

    # Теперь точки кривой формирует get_knot!
    # Этот метод вызывается при добавлении точек и пересчитывание координат опорных, как и в родителе Polyline
    def _curve_points_preprocessor(self):
        if len(self._points) < 3:
            return []

        result = []
        for point_num in range(-2, len(self._points) - 2):
            points = list()
            points.append((self._points[point_num]["point"] + self._points[point_num + 1]["point"]) * 0.5)
            points.append(self._points[point_num + 1]["point"])
            points.append((self._points[point_num + 1]["point"] + self._points[point_num + 2]["point"]) * 0.5)

            result.extend(self._get_points(points))
        return result

    # Сглаживание ломаной
    def _get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]

        return (points[deg] * alpha) + (self._get_point(points, alpha, deg - 1) * (1 - alpha))

    def _get_points(self, base_points):
        alpha = 1 / self._steps
        res = []
        for i in range(self._steps):
            res.append(self._get_point(base_points, i * alpha))
        return res


# Отрисовка справки
def draw_help(display, steps):
    display.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = list()
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["Mouse click", "Add point/remove point"])
    data.append(["N", "Add new curve"])
    data.append(["U", "speed up"])
    data.append(["D", "speed d"])
    data.append(["", ""])
    data.append([str(steps), "Current points"])

    pygame.draw.lines(display, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        display.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        display.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


# Удаление точки реализовано через повторный клик на неё
# Новая кривая создаётся по клавише N. Для неё так же работает удаление/ добавление точек
# Удаление точек работает для всех кривых на полотне
# Ускорение и замедление делаются клавишами U и D
def game():
    pygame.init()
    game_display = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    curve_object = Knot

    working = True
    current_curve = curve_object(game_display)
    curves = [current_curve]
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    current_curve = curve_object(game_display)
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_n:
                    current_curve = curve_object(game_display)
                    curves.append(current_curve)
                if event.key == pygame.K_u:
                    for curve in curves:
                        curve.speed_up()
                if event.key == pygame.K_d:
                    for curve in curves:
                        curve.speed_down()
                if event.key == pygame.K_KP_PLUS:
                    current_curve.steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    current_curve.steps -= 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Если клик был рядом с существующей точкой, удалим её
                # Если произошло удаление точки, то добавлять в актуальную кривую в любом случае не будем
                point_removed = False
                for curve in curves:
                    point_num = curve.contains(event.pos)
                    if point_num is not None:
                        curve.remove_point(point_num)
                        point_removed = True

                if not point_removed:
                    current_curve.append_point(point=event.pos, speed=(random.random() * 2, random.random() * 2))

        game_display.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        for curve in curves:
            hue = (hue + 1) % 360
            color.hsla = (hue, 100, 50, 100)

            curve.draw_points(style="points")
            curve.draw_points(style="line", width=3, color=color)

            if not pause:
                curve.set_points()

        if show_help:
            draw_help(game_display, current_curve.steps)

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)


def main():
    game()


if __name__ == "__main__":
    main()