import pygame
import random
import math

SCREEN_DIM = (800, 600)


class Vec2d:
    """
    Represents 2d vector
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):

        if not isinstance(other, Vec2d):
            raise TypeError
        return Vec2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other):

        if not isinstance(other, Vec2d):
            raise TypeError
        return Vec2d(self.x - other.x, self.y - other.y)

    def __mul__(self, other):

        if isinstance(other, Vec2d):
            return self.x * other.x + self.y * other.y
        else:
            return Vec2d(self.x * other, self.y * other)

    def __len__(self):
        """
        Ð•ÑÐ»Ð¸ ÑƒÐ±Ñ€Ð°Ñ‚ÑŒ Ð¿Ñ€ÐµÐ¾Ð±Ñ€Ð°Ð·Ð¾Ð²Ð°Ð½Ð¸Ðµ Ðº int, Ð±ÑƒÐ´ÐµÑ‚ Ð²Ñ‹Ð·Ð²Ð°Ð½Ð¾ Ð¸ÑÐºÐ»ÑŽÑ‡ÐµÐ½Ð¸Ðµ \_(Ð¾_Ð¾)_/
        """

        return int(math.sqrt(self.x * self.x + self.y * self.y))

    def int_pair(self):

        return int(self.x), int(self.y)


class PolylineStyle:

    LINE, POINTS = 0, 1


class Polyline:

    """
    Represents polyline with speed vector assigned to each point
    """

    def __init__(self, points=None, speeds=None):

            if points and speeds:
                if len(points) != len(speeds):
                    raise ValueError

                self._points = list(points)
                self._speeds = list(speeds)

            else:
                self._points = []
                self._speeds = []

    def add_point(self, point: Vec2d, speed: Vec2d):

        self._points.append(point)
        self._speeds.append(speed)

    def remove_point(self, index=None):

        self._points.pop(index)
        self._speeds.pop(index)

    def __len__(self):

        return len(self._points)

    def update(self, time_shift=1.0):

        for p in range(len(self._points)):

            self._points[p] = self._points[p] + self._speeds[p] * time_shift
            if self._points[p].x > SCREEN_DIM[0] or self._points[p].x < 0:
                self._speeds[p].x *= -1
            if self._points[p].y > SCREEN_DIM[1] or self._points[p].y < 0:
                self._speeds[p].y *= -1

    def draw_points(self, style=PolylineStyle.POINTS, width=3,
                    color=(255, 255, 255)):

        if style == PolylineStyle.LINE:

            for p_n in range(-1, len(self._points) - 1):

                pygame.draw.line(
                    gameDisplay, color,
                    self._points[p_n].int_pair(),
                    self._points[p_n + 1].int_pair(),
                    width)

        elif style == PolylineStyle.POINTS:
            for p in self._points:
                pygame.draw.circle(gameDisplay, color,
                                   p.int_pair(), width)


class Knot(Polyline):

    """
    Extends base class Polyline with method get_knot_polyline
    """

    @staticmethod
    def _get_point(base_points, alpha, deg=None):
        if deg is None:
            deg = len(base_points) - 1
        if deg == 0:
            return base_points[0]
        return base_points[deg] * alpha + \
               Knot._get_point(base_points, alpha, deg - 1) * (1 - alpha)

    @staticmethod
    def _get_points(base_points, steps):
        alpha = 1 / steps
        res = []
        for i in range(steps):
            res.append(Knot._get_point(base_points, i * alpha))
        return res

    def get_knot_polyline(self, steps) -> Polyline:

        points = []

        if len(self._points) >= 3:

            for i in range(-2, len(self._points) - 2):
                ptn = []

                ptn.append(
                    (self._points[i] + self._points[i + 1]) * 0.5)

                ptn.append(self._points[i + 1])

                ptn.append(
                    (self._points[i + 1] + self._points[i + 2]) * 0.5)

                points.extend(self._get_points(ptn, steps))

        knot_poly = Polyline(points, [Vec2d(0, 0)] * len(points))
        return knot_poly


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
    data.append(["Z", "Increase speed"])
    data.append(["X", "Decrease speed"])
    data.append(["Delete", "Delete last point"])
    data.append(["", ""])
    data.append([str(steps), "Current points"])
    data.append([f"{velocity:.1f}", "Current velocity scale"])

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

    working = True
    show_help = False
    pause = True
    hue = 0
    color = pygame.Color(0)
    steps = 35
    velocity = 1.0

    poly = Knot()

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    poly = Knot()
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps = max(1, steps - 1)
                if event.key == pygame.K_DELETE:
                    if len(poly) > 0:
                        poly.remove_point(len(poly) - 1)
                if event.key == pygame.K_z:
                    velocity = max(0.1, velocity - 0.1)
                if event.key == pygame.K_x:
                    velocity = min(4.0, velocity + 0.1)

            if event.type == pygame.MOUSEBUTTONDOWN:

                poly.add_point(Vec2d(*event.pos),
                               Vec2d(random.random(), random.random()) * 2)

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)

        poly.draw_points()
        poly.get_knot_polyline(steps).draw_points(PolylineStyle.LINE, 3, color)

        if not pause:
            poly.update(time_shift=velocity)

        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)