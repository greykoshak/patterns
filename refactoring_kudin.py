import random
import math

import pygame


SCREEN_DIM = (800, 600)


class Vec2d:
    # Ð¢Ð¾Ñ‡Ð½Ð¾ÑÑ‚ÑŒ ÑÑ€Ð°Ð²Ð½ÐµÐ½Ð¸Ñ Ð²ÐµÐºÑ‚Ð¾Ñ€Ð¾Ð².
    EPS = 3

    # Ð˜Ð½Ð¸Ñ†Ð¸Ð°Ð»Ð¸Ð·Ð°Ñ†Ð¸Ñ Ð²ÐµÐºÑ‚Ð¾Ñ€Ð° Ð¿Ð¾ ÐµÐ³Ð¾ Ð½Ð°Ñ‡Ð°Ð»Ñƒ (x) Ð¸ ÐºÐ¾Ð½Ñ†Ñƒ (y) Ð¸Ð»Ð¸ Ð¿Ð¾ ÐµÐ³Ð¾ ÐºÐ¾Ð¾Ñ€Ð´Ð¸Ð½Ð°Ñ‚Ð°Ð¼.
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Ð¡Ð»Ð¾Ð¶ÐµÐ½Ð¸Ðµ Ñ Ð´Ñ€ÑƒÐ³Ð¸Ð¼ Ð²ÐµÐºÑ‚Ð¾Ñ€Ð¾Ð¼.
    def __add__(self, other):
        return Vec2d(self.x + other.x, self.y + other.y)

    # Ð’Ñ‹Ñ‡Ð¸Ñ‚Ð°Ð½Ð¸Ðµ Ð´Ñ€ÑƒÐ³Ð¾Ð³Ð¾ Ð²ÐµÐºÑ‚Ð¾Ñ€Ð°.
    def __sub__(self, other):
        return Vec2d(self.x - other.x, self.y - other.y)

    # Ð¡ÐºÐ°Ð»ÑÑ€Ð½Ð¾Ðµ Ð¿Ñ€Ð¾Ð¸Ð·Ð²ÐµÐ´ÐµÐ½Ð¸Ðµ Ð²ÐµÐºÑ‚Ð¾Ñ€Ð¾Ð² Ð¸Ð»Ð¸ ÑƒÐ¼Ð½Ð¾Ð¶ÐµÐ½Ð¸Ðµ Ð½Ð° Ñ‡Ð¸ÑÐ»Ð¾.
    def __mul__(self, other):
        # ÐŸÑ€Ð¾Ð±ÑƒÐµÐ¼ ÑÐºÐ°Ð»ÑÐ½Ð¾Ðµ ÑƒÐ¼Ð½Ð¾Ð¶ÐµÐ½Ð¸Ðµ Ð²ÐµÐºÑ‚Ð¾Ñ€Ð¾Ð². Ð•ÑÐ»Ð¸ Ð±ÑƒÐ´ÐµÑ‚ Ð²Ñ‹Ð±Ñ€Ð¾ÑˆÐµÐ½Ð¾ Ð¸ÑÐºÐ»ÑŽÑ‡ÐµÐ½Ð¸Ðµ - Ð¿Ñ€Ð¾Ð±ÑƒÐµÐ¼ ÑƒÐ¼Ð½Ð¾Ð¶ÐµÐ½Ð¸Ðµ Ð½Ð° Ñ‡Ð¸ÑÐ»Ð¾.
        try:
            return self.x * other.x + self.y * other.y
        except AttributeError:
            pass
        return Vec2d(self.x * other, self.y * other)

    # Ð¡Ñ€Ð°Ð²Ð½ÐµÐ½Ð¸Ðµ Ð½Ð° Ñ€Ð°Ð²ÐµÐ½ÑÑ‚Ð²Ð¾ Ñ Ð´Ñ€ÑƒÐ³Ð¸Ð¼ Ð²ÐµÐºÑ‚Ð¾Ñ€Ð¾Ð¼. Ð•ÑÐ»Ð¸ Ð¾ÐºÑ€ÑƒÐ³Ð»Ñ‘Ð½Ð½Ñ‹Ðµ Ð´Ð¾ Ñ†ÐµÐ»Ñ‹Ñ… ÐºÐ¾Ð¾Ñ€Ð´Ð¸Ð½Ð°Ñ‚Ñ‹ Ñ€Ð°Ð²Ð½Ñ‹, Ñ‚Ð¾ Ð¸ Ð²ÐµÐºÑ‚Ð¾Ñ€Ñ‹ Ñ€Ð°Ð²Ð½Ñ‹.
    def __eq__(self, other):
        if math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2) < self.EPS:
            return True

        return False

    # Ð’Ñ‹Ñ‡Ð¸ÑÐ»ÐµÐ½Ð¸Ðµ Ð´Ð»Ð¸Ð½Ñ‹ Ð²ÐµÐºÑ‚Ð¾Ñ€Ð° Ñ‡ÐµÑ€ÐµÐ· len.
    # Ð’ÐÐ˜ÐœÐÐÐ˜Ð•: Ñ„ÑƒÐ½ÐºÑ†Ð¸Ñ Ð´Ð¾Ð»Ð¶Ð½Ð° Ð²Ð¾Ð·Ð²Ñ€Ð°Ñ‰Ð°Ñ‚ÑŒ int, Ð¸Ð½Ð°Ñ‡Ðµ Ð±ÑƒÐ´ÐµÑ‚ Ð¿Ñ€Ð¾Ð¸ÑÑ…Ð¾Ð´Ð¸Ñ‚ÑŒ Ð¿Ð°Ð´ÐµÐ½Ð¸Ðµ, Ð¿Ð¾ÑÑ‚Ð¾Ð¼Ñƒ Ð¿Ñ€Ð¾Ð¸ÑÑ…Ð¾Ð´Ð¸Ñ‚ Ð¾ÐºÑ€ÑƒÐ³Ð»ÐµÐ½Ð¸Ðµ Ð´Ð¾ Ñ†ÐµÐ»Ð¾Ð³Ð¾.
    def __len__(self):
        return int(math.sqrt(self.x ** 2 + self.y ** 2))

    # Ð’Ð¾Ð·Ð²Ñ€Ð°Ñ‰Ð°ÐµÑ‚ Ð¿Ð°Ñ€Ñƒ ÐºÐ¾Ð¾Ñ€Ð´Ð¸Ð½Ð°Ñ‚, Ð¾ÐºÑ€ÑƒÐ³Ð»Ñ‘Ð½Ð½Ñ‹Ñ… Ð´Ð¾ Ñ†ÐµÐ»Ñ‹Ñ….
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

    # ÐŸÑ€Ð¾Ð²ÐµÑ€ÐºÐ° Ð½Ð° Ð½Ð°Ð»Ð¸Ñ‡Ð¸Ðµ Ñ‚Ð¾Ñ‡ÐºÐ¸. None ÐµÑÐ»Ð¸ Ñ‚Ð¾Ñ‡ÐºÐ¸ Ð½ÐµÑ‚, Ð¸Ð½Ð°Ñ‡Ðµ Ð²Ð¾Ð·Ñ€Ð°Ñ‰Ð°ÐµÑ‚ ÐµÑ‘ Ð½Ð¾Ð¼ÐµÑ€.
    def contains(self, point):
        tmp_point = Vec2d(point[0], point[1])
        for point_num in range(len(self._points)):
            if self._points[point_num]["point"] == tmp_point:
                return point_num

        return None

    # Ð”Ð¾Ð±Ð°Ð²Ð»ÐµÐ½Ð¸Ðµ Ñ‚Ð¾Ñ‡ÐºÐ¸ Ð²Ð¼ÐµÑÑ‚Ðµ ÑÐ¾ ÑÐºÐ¾Ñ€Ð¾ÑÑ‚ÑŒÑŽ.
    def append_point(self, point, speed):
        self._points.append({
            "point": Vec2d(point[0], point[1]),
            "speed": Vec2d(speed[0], speed[1])
        })

        self._curve_points = self._curve_points_preprocessor()

    def remove_point(self, point_num):
        del self._points[point_num]

        self._curve_points = self._curve_points_preprocessor()

    # ÐŸÐµÑ€ÐµÑÑ‡Ð¸Ñ‚Ñ‹Ð²Ð°Ð½Ð¸Ðµ ÐºÐ¾Ð¾Ñ€Ð´Ð¸Ð½Ð°Ñ‚ Ð¾Ð¿Ð¾Ñ€Ð½Ñ‹Ñ… Ñ‚Ð¾Ñ‡ÐµÐº.
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

    # ÐžÑ‚Ñ€Ð¸ÑÐ¾Ð²ÐºÐ° Ð»Ð¾Ð¼Ð°Ð½Ð½Ð½Ð¾Ð¹.
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


# get_knot Ð’Ð«Ð—Ð«Ð’ÐÐ•Ð¢Ð¡Ð¯ ÐºÐ°Ðº Ð¿Ñ€ÐµÐ¿Ñ€Ð¾Ñ†ÐµÑÑÐ¾Ñ€ self._curved_points!
# Ð­Ñ‚Ð¾ Ð¿Ð¾Ð·Ð²Ð¾Ð»Ð¸Ð»Ð¾ Ð¿Ñ€Ð¾ÑÑ‚Ð¾ Ñ€Ð°ÑÑˆÐ¸Ñ€Ð¸Ñ‚ÑŒ ÐºÐ»Ð°ÑÑ Polyline Ñ Ð¿ÐµÑ€ÐµÐ³Ñ€ÑƒÐ·ÐºÐ¾Ð¹ Ð¼ÐµÑ‚Ð¾Ð´Ð° _curve_points_preprocessor.
class Knot(Polyline):
    def __init__(self, display):
        super().__init__(display)

    # Ð¢ÐµÐ¿ÐµÑ€ÑŒ Ñ‚Ð¾Ñ‡ÐºÐ¸ ÐºÑ€Ð¸Ð²Ð¾Ð¹ Ñ„Ð¾Ñ€Ð¼Ð¸Ñ€ÑƒÐµÑ‚ get_knot!
    # Ð­Ñ‚Ð¾Ñ‚ Ð¼ÐµÑ‚Ð¾Ð´ Ð²Ñ‹Ð·Ñ‹Ð²Ð°ÐµÑ‚ÑÑ Ð¿Ñ€Ð¸ Ð´Ð¾Ð±Ð°Ð²Ð»ÐµÐ½Ð¸Ð¸ Ñ‚Ð¾Ñ‡ÐµÐº Ð¸ Ð¿ÐµÑ€ÐµÑÑ‡Ð¸Ñ‚Ñ‹Ð²Ð°Ð½Ð¸Ð¸ ÐºÐ¾Ð¾Ñ€Ð´Ð¸Ð½Ð°Ñ‚ Ð¾Ð¿Ð¾Ñ€Ð½Ñ‹Ñ…, ÐºÐ°Ðº Ð¸ Ð² Ñ€Ð¾Ð´Ð¸Ñ‚ÐµÐ»Ðµ Polyline.
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

    # Ð¡Ð³Ð»Ð°Ð¶Ð¸Ð²Ð°Ð½Ð¸Ðµ Ð»Ð¾Ð¼Ð°Ð½Ð¾Ð¹
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


# ÐžÑ‚Ñ€Ð¸ÑÐ¾Ð²ÐºÐ° ÑÐ¿Ñ€Ð°Ð²ÐºÐ¸.
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


# Ð£Ð´Ð°Ð»ÐµÐ½Ð¸Ðµ Ñ‚Ð¾Ñ‡ÐºÐ¸ Ñ€ÐµÐ°Ð»Ð¸Ð·Ð¾Ð²Ð°Ð½Ð¾ Ñ‡ÐµÑ€ÐµÐ· Ð¿Ð¾Ð²Ñ‚Ð¾Ñ€Ð½Ñ‹Ð¹ ÐºÐ»Ð¸Ðº Ð½Ð° Ð½ÐµÑ‘.
# ÐÐ¾Ð²Ð°Ñ ÐºÑ€Ð¸Ð²Ð°Ñ ÑÐ¾Ð·Ð´Ð°Ñ‘Ñ‚ÑÑ Ð¿Ð¾ ÐºÐ»Ð°Ð²Ð¸ÑˆÐµ N. Ð”Ð»Ñ Ð½ÐµÑ‘ Ñ‚Ð°Ðº Ð¶Ðµ Ñ€Ð°Ð±Ð¾Ñ‚Ð°ÐµÑ‚ ÑƒÐ´Ð°Ð»ÐµÐ½Ð¸Ðµ/ Ð´Ð¾Ð±Ð°Ð²Ð»ÐµÐ½Ð¸Ðµ Ñ‚Ð¾Ñ‡ÐµÐº.
# Ð£Ð´Ð°Ð»ÐµÐ½Ð¸Ðµ Ñ‚Ð¾Ñ‡ÐµÐº Ñ€Ð°Ð±Ð¾Ñ‚Ð°ÐµÑ‚ Ð´Ð»Ñ Ð²ÑÐµÑ… ÐºÑ€Ð¸Ð²Ñ‹Ñ… Ð½Ð° Ð¿Ð¾Ð»Ð¾Ñ‚Ð½Ðµ.
# Ð£ÑÐºÐ¾Ñ€ÐµÐ½Ð¸Ðµ Ð¸ Ð·Ð°Ð¼ÐµÐ´Ð½ÐµÐ½Ð¸Ðµ Ð´ÐµÐ»Ð°ÑŽÑ‚ÑÑ ÐºÐ»Ð°Ð²Ð¸ÑˆÐ°Ð¼Ð¸ U Ð¸ D.
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
                # Ð•ÑÐ»Ð¸ ÐºÐ»Ð¸Ðº Ð±Ñ‹Ð» Ñ€ÑÐ´Ð¾Ð¼ Ñ ÑÑƒÑ‰ÐµÑÑ‚Ð²ÑƒÑŽÑ‰ÐµÐ¹ Ñ‚Ð¾Ñ‡ÐºÐ¾Ð¹, ÑƒÐ´Ð°Ð»Ð¸Ð¼ ÐµÑ‘.
                # Ð•ÑÐ»Ð¸ Ð¿Ñ€Ð¾Ð¸Ð·Ð¾ÑˆÐ»Ð¾ ÑƒÐ´Ð°Ð»ÐµÐ½Ð¸Ðµ Ñ‚Ð¾Ñ‡ÐºÐ¸, Ñ‚Ð¾ Ð´Ð¾Ð±Ð°Ð²Ð»ÑÑ‚ÑŒ Ð² Ð°ÐºÑ‚ÑƒÐ°Ð»ÑŒÐ½ÑƒÑŽ ÐºÑ€Ð¸Ð²ÑƒÑŽ Ð² Ð»ÑŽÐ±Ð¾Ð¼ ÑÐ»ÑƒÑ‡Ð°Ðµ Ð½Ðµ Ð±ÑƒÐ´ÐµÐ¼.
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