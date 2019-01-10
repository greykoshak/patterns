import pygame  # pip3 install pygame
import random
import math

"""
Реализовать класс 2-мерных векторов Vec2d — определить основные математические операции: 
   сумма Vec2d.__add__, 
   разность Vec2d.__sub__, 
   умножение на скаляр и 
   скалярное умножение (Vec2d.__mul__); 
   добавить возможность вычислять длину вектора a через len(a);
   добавить метод int_pair для получение пары (tuple) целых чисел.
Реализовать класс замкнутых ломаных Polyline, с возможностями: 
   добавление в ломаную точки (Vec2d) c её скоростью; 
   пересчёт координат точек (set_points); 
   отрисовка ломаной (draw_points),
Реализовать класс Knot — потомок класса Polyline — в котором 
   добавление и пересчёт координат инициируют вызов функции get_knot для расчёта 
   точек кривой по добавляемым опорным.

Все классы должны быть самостоятельными и не использовать внешние функции.

Дополнительные задачи (для получения "положительной" оценки не обязательны):

Реализовать возможность удаления точки из кривой.
Реализовать возможность удаления/добавления точек сразу для нескольких кривых.
Реализовать возможность ускорения/замедления движения кривых.
"""

SCREEN_DIM = (800, 600)


class ScreenSaver():
    """
    Ядро системы, выполняется в основном цикле.
    """

    def __init__(self, caption=""):
        pygame.init()
        pygame.font.init()
        self.gameDisplay = pygame.display.set_mode(SCREEN_DIM)
        pygame.display.set_caption(caption)

        self.steps = 35
        self.working = True
        self.points = []
        self.speeds = []
        self.show_help = False
        self.pause = True

        self.hue = 0
        self.color = pygame.Color(0)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.working = False
                if event.key == pygame.K_r:
                    self.points = []
                    self.speeds = []
                if event.key == pygame.K_p:
                    self.pause = not self.pause
                if event.key == pygame.K_KP_PLUS:
                    self.steps += 1
                if event.key == pygame.K_F1:
                    self.show_help = not self.show_help
                if event.key == pygame.K_KP_MINUS:
                    self.steps -= 1 if self.steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.points.append(event.pos)
                self.speeds.append((random.random() * 2, random.random() * 2))

    def run(self):

        hlp = Helper()
        pol = Polyline()
        knot = Knot("MyScreenSaver version 0.1")
        v2d = Vec2d()

        while self.working:
            self.handle_events()

            self.gameDisplay.fill((0, 0, 0))
            self.hue = (self.hue + 1) % 360
            self.color.hsla = (self.hue, 100, 50, 100)
            pol.draw_points(self.points)
            pol.draw_points(knot.get_knot(self.points, self.steps), "line", 3, self.color)

            if not self.pause:
                pol.set_points(self.points, self.speeds)
            if self.show_help:
                hlp.draw_help()

            pygame.display.flip()

        pygame.display.quit()
        pygame.quit()
        exit(0)


class Vec2d():
    """
    Обработка двумерных векторов.  Методы для работы с векторами.
    """

    def sub(self, x, y):  # разность двух векторов
        return x[0] - y[0], x[1] - y[1]

    def add(self, x, y):  # сумма двух векторов
        return x[0] + y[0], x[1] + y[1]

    def length(self, x):  # длина вектора
        return math.sqrt(x[0] * x[0] + x[1] * x[1])

    def mul(self, v, k):  # умножение вектора на число
        return v[0] * k, v[1] * k

    def scal_mul(self, v, k):  # скалярное умножение векторов
        return v[0] * k, v[1] * k

    def vec(self, x, y):  # создание вектора по началу (x) и концу (y) направленного отрезка
        return self.sub(y, x)

    def int_pair(self, x, y):
        return tuple([x, y])


class Polyline(ScreenSaver, Vec2d):
    """
    Класс замкнутых ломаных
    """

    # Персчитывание координат опорных точек
    def set_points(self, points, speeds):
        for p in range(len(points)):
            points[p] = self.add(points[p], speeds[p])
            if points[p][0] > SCREEN_DIM[0] or points[p][0] < 0:
                speeds[p] = (-speeds[p][0], speeds[p][1])
            if points[p][1] > SCREEN_DIM[1] or points[p][1] < 0:
                speeds[p] = (speeds[p][0], -speeds[p][1])

    # "Отрисовка" точек
    def draw_points(self, points, style="points", width=3, color=(255, 255, 255)):
        if style == "line":
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(self.gameDisplay, color, (int(points[p_n][0]), int(points[p_n][1])),
                                 (int(points[p_n + 1][0]), int(points[p_n + 1][1])), width)

        elif style == "points":
            for p in points:
                pygame.draw.circle(self.gameDisplay, color,
                                   (int(p[0]), int(p[1])), width)


class Knot(Polyline):
    """
    Расчёт точек кривой по добавляемым опорным точкам
    """

    # Сглаживание ломаной
    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return self.add(self.mul(points[deg], alpha), self.mul(self.get_point(points, alpha, deg - 1), 1 - alpha))

    def get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_knot(self, points, count):
        if len(points) < 3:
            return []
        res = []
        for i in range(-2, len(points) - 2):
            ptn = []
            ptn.append(self.mul(self.add(points[i], points[i + 1]), 0.5))
            ptn.append(points[i + 1])
            ptn.append(self.mul(self.add(points[i + 1], points[i + 2]), 0.5))

            res.extend(self.get_points(ptn, count))
        return res


class Helper(ScreenSaver):
    """
    Отрисовка справки
    """

    def draw_help(self):
        self.gameDisplay.fill((50, 50, 50))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        data = []
        data.append(["F1", "Show Help"])
        data.append(["R", "Restart"])
        data.append(["P", "Pause/Play"])
        data.append(["Num+", "More points"])
        data.append(["Num-", "Less points"])
        data.append(["", ""])
        data.append([str(self.steps), "Current points"])

        pygame.draw.lines(self.gameDisplay, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            self.gameDisplay.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            self.gameDisplay.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


# Основная программа
if __name__ == "__main__":
    saver = ScreenSaver("MyScreenSaver")
    saver.run()
