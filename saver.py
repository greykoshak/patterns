import pygame  # pip3 install pygame
import random

SCREEN_DIM = (800, 600)


class Vec2d():
    """
    Handling two-dimensional vectors. Methods for working with vectors.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, vec):  # sum of two vectors
        return Vec2d(self.x + vec.x, self.y + vec.y)

    def __sub__(self, vec):  # subtraction of two vectors
        return Vec2d(self.x - vec.x, self.y - vec.y)

    def __mul__(self, multiplier):  # multiply vector by number or vector
        if isinstance(multiplier, Vec2d):
            return self.x * multiplier.x + self.y * multiplier.y
        else:
            return Vec2d(self.x * multiplier, self.y * multiplier)

    def int_pair(self):
        return tuple([int(self.x), int(self.y)])

    def __len__(self):
        # If you remove the conversion to int, an exception will be thrown
        return int((self.x * self.x + self.y * self.y) ** 0.5)


class Polyline():
    """
    Class of closed broken lines
    """

    def __init__(self, points=None, speeds=None):
        if points and speeds:
            if len(points) != len(speeds):
                raise ValueError
            self.points = list(points)
            self.speeds = list(speeds)
        else:
            self.points = []
            self.speeds = []

    def add_point(self, point: Vec2d, speed: Vec2d):
        self.points.append(point)
        self.speeds.append(speed)

    def remove_point(self, index: int):
        del self.points[index]
        del self.speeds[index]

    def clear(self):
        self.points = []
        self.speeds = []

    def __len__(self):
        return len(self.points)

    def update(self):
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p].x *= -1
            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p].y *= -1

    def increase_speed(self, k=2):
        for i in range(len(self.speeds)):
            self.speeds[i] = self.speeds[i] * k

    def decrease_speed(self, k=2):
        for i in range(len(self.speeds)):
            self.speeds[i] = self.speeds[i] * (1 / k)

    # Recalculation of GCP coordinates
    def draw_points(self, style="points", width=3,
                    color=(255, 255, 255)):

        if style == "line":
            for p_n in range(-1, len(self.points) - 1):
                pygame.draw.line(gameDisplay, color, self.points[p_n].int_pair(),
                                 self.points[p_n + 1].int_pair(), width)
        elif style == "points":
            for p in self.points:
                pygame.draw.circle(gameDisplay, color, p.int_pair(), width)


class Knot(Polyline):
    """
    Calculation of curve points by added reference points
    """

    @staticmethod
    def _get_point(base_points, alpha, deg=None):
        if deg is None:
            deg = len(base_points) - 1
        if deg == 0:
            return base_points[0]
        return base_points[deg] * alpha + Knot._get_point(base_points, alpha, deg - 1) * (1 - alpha)

    @staticmethod
    def _get_points(base_points, steps):
        alpha = 1 / steps
        res = []
        for i in range(steps):
            res.append(Knot._get_point(base_points, i * alpha))
        return res

    def get_knot_polyline(self, steps) -> Polyline:
        points = []

        if len(self.points) >= 3:
            for i in range(-2, len(self.points) - 2):
                ptn = []
                ptn.append(
                    (self.points[i] + self.points[i + 1]) * 0.5)
                ptn.append(self.points[i + 1])
                ptn.append(
                    (self.points[i + 1] + self.points[i + 2]) * 0.5)
                points.extend(self._get_points(ptn, steps))

        knot_poly = Polyline(points, [Vec2d(0, 0)] * len(points))

        return knot_poly


class Helper():
    """
    Drawing help
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
        data.append(["Up", "Speed up"])
        data.append(["Down", "Speed down"])
        data.append(['Delete', 'Delete a point'])
        data.append(["", ""])
        data.append([str(self.steps), "Current points"])

        pygame.draw.lines(self.gameDisplay, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            self.gameDisplay.blit(font1.render(text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            self.gameDisplay.blit(font2.render(text[1], True, (128, 128, 255)), (200, 100 + 30 * i))

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
    data.append(["Up", "Speed up"])
    data.append(["Down", "Speed down"])
    data.append(['Delete', 'Delete a point'])
    data.append(["", ""])
    data.append([str(steps), "Current points"])
    data.append([str(len(poly)), "Current knots"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


# Main program
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
                if event.key == pygame.K_UP:
                    poly.increase_speed()
                if event.key == pygame.K_DOWN:
                    poly.decrease_speed()

            if event.type == pygame.MOUSEBUTTONDOWN:
                poly.add_point(Vec2d(*event.pos), Vec2d(random.random(), random.random()) * 2)

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)

        poly.draw_points()
        poly.get_knot_polyline(steps).draw_points("line", 3, color)

        if not pause:
            poly.update()

        if show_help:
            draw_help()
            pass

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
