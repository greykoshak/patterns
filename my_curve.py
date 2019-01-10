# coding: utf-8

# In[1]:

import pygame
import random
import math

SCREEN_DIM = (800, 600)


# ÐœÐµÑ‚Ð¾Ð´Ñ‹ Ð´Ð»Ñ Ñ€Ð°Ð±Ð¾Ñ‚Ñ‹ Ñ Ð²ÐµÐºÑ‚Ð¾Ñ€Ð°Ð¼Ð¸

class Vec2d():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, vec):  # Ñ€Ð°Ð·Ð½Ð¾ÑÑ‚ÑŒ Ð´Ð²ÑƒÑ… Ð²ÐµÐºÑ‚Ð¾Ñ€Ð¾Ð²
        if not isinstance(vec, Vec2d):
            raise TypeError('Vector can be added to vector only')
        else:
            return Vec2d(self.x - vec.x, self.y - vec.y)

    def __add__(self, vec):  # ÑÑƒÐ¼Ð¼Ð° Ð´Ð²ÑƒÑ… Ð²ÐµÐºÑ‚Ð¾Ñ€Ð¾Ð²
        if not isinstance(vec, Vec2d):
            raise TypeError('Vector can be added to vector only')
        else:
            return Vec2d(self.x + vec.x, self.y + vec.y)

    def __len__(self, obj=None):  # Ð´Ð»Ð¸Ð½Ð½Ð° Ð²ÐµÐºÑ‚Ð¾Ñ€Ð°
        if obj is not None and isinstance(obj, Vec2d):
            return (obj.x * obj.x + obj.y * obj.y) ** 0.5
        else:
            return (self.x * self.x + self.y * self.y) ** 0.5

    def __mul__(self, obj):  # ÑƒÐ¼Ð½Ð¾Ð¶ÐµÐ½Ð¸Ðµ Ð²ÐµÐºÑ‚Ð¾Ñ€Ð° Ð½Ð° Ñ‡Ð¸ÑÐ»Ð¾
        if isinstance(obj, Vec2d):
            return self.x * obj.x + self.y * obj.y
        elif type(obj) is int or type(obj) is float:
            return Vec2d(self.x * obj, self.y * obj)
        else:
            raise TypeError('Vector can be multiplied on a number or another vector only!')

    def int_pair(self):
        return (int(self.x), int(self.y))


class Polyline():
    def __init__(self):
        self.points = []
        self.speeds = []

    def add_point(self, point, speed):
        self.points.append(point)
        self.speeds.append(speed)

    # ÐŸÐµÑ€ÑÑ‡Ð¸Ñ‚Ñ‹Ð²Ð°Ð½Ð¸Ðµ ÐºÐ¾Ð¾Ñ€Ð´Ð¸Ð½Ð°Ñ‚ Ð¾Ð¿Ð¾Ñ€Ð½Ñ‹Ñ… Ñ‚Ð¾Ñ‡ÐµÐº
    def set_points(self):
        for p in range(len(self.points)):
            self.points[p] += self.speeds[p]
            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p] = Vec2d(-self.speeds[p].x, self.speeds[p].y)
            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p] = Vec2d(self.speeds[p].x, -self.speeds[p].y)

    # "ÐžÑ‚Ñ€Ð¸ÑÐ¾Ð²ÐºÐ°" Ñ‚Ð¾Ñ‡ÐµÐº
    def draw_points(self, points=None, style="points", width=3, color=(255, 255, 255)):
        if points is None:
            points = self.points
        if style == "line":
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(gameDisplay, color, points[p_n].int_pair(),
                                 points[p_n + 1].int_pair(), width)

        elif style == "points":
            for p in self.points:
                pygame.draw.circle(gameDisplay, color,
                                   p.int_pair(), width)

    # ÑƒÑÐºÐ¾Ñ€ÐµÐ½Ð¸Ðµ/Ð·Ð°Ð¼ÐµÐ´Ð»ÐµÐ½Ð¸Ðµ Ð² n Ñ€Ð°Ð·
    def speed_up(self, n):
        for s in range(len(self.speeds)):
            self.speeds[s] *= n

    # ÑƒÐ´Ð°Ð»ÐµÐ½Ð¸Ðµ Ñ‚Ð¾Ñ‡ÐºÐ¸
    def delete_point_by_item(self, point):
        index = self.points.index(point)
        self.delete_point_by_index(index)

    def delete_point_by_index(self, index):
        self.points.pop(index)
        self.speeds.pop(index)


class Knot(Polyline):
    def __init__(self, count):
        super().__init__()
        self.count = count

    def add_point(self, point, speed):
        super().add_point(point, speed)
        return self.get_knot()

    def set_points(self):
        super().set_points()
        return self.get_knot()

    @staticmethod
    def get_point(points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return (points[deg] * alpha) + (Knot.get_point(points, alpha, deg - 1) * (1 - alpha))

    @staticmethod
    def get_points(count, base_points):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(Knot.get_point(base_points, i * alpha))
        return res

    def get_knot(self):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)

            res.extend(Knot.get_points(self.count, ptn))
        return res


# ÐžÑ‚Ñ€Ð¸ÑÐ¾Ð²ÐºÐ° ÑÐ¿Ñ€Ð°Ð²ÐºÐ¸
def draw_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["Arrow UP", "Speed up in 2 times"])
    data.append(["Arrow DOWN", "Slow down in 2 times"])
    data.append(['Delete', 'Delete last point'])
    data.append(["", ""])
    data.append([str(steps), "Current points"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


# ÐžÑÐ½Ð¾Ð²Ð½Ð°Ñ Ð¿Ñ€Ð¾Ð³Ñ€Ð°Ð¼Ð¼Ð°
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    points = []
    speeds = []
    knot = Knot(steps)
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
                    knot = Knot(steps)
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0
                if event.key == pygame.K_UP:
                    knot.speed_up(2)
                if event.key == pygame.K_DOWN:
                    knot.speed_up(0.5)
                if event.key == pygame.K_DELETE:
                    if len(knot.points) > 3:
                        knot.delete_point_by_index(-1)

            if event.type == pygame.MOUSEBUTTONDOWN:
                knot.add_point(Vec2d(*event.pos), Vec2d(random.random() * 2, random.random() * 2))
        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        knot.draw_points()
        knot.draw_points(knot.get_knot(), "line", 3, color)
        if not pause:
            knot.set_points()
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)