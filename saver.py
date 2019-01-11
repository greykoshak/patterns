import pygame  # pip3 install pygame
import random
import math

SCREEN_DIM = (800, 600)


class ScreenSaver():
    """
    The core of the system is executed in the main loop.
    """

    def __init__(self, caption=None):
        pygame.init()
        pygame.font.init()
        self.gameDisplay = pygame.display.set_mode(SCREEN_DIM)
        if caption is not None:
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
                if event.key == pygame.K_UP:
                    # knot.speed_up(2)
                    pass
                if event.key == pygame.K_DOWN:
                    # knot.speed_up(0.5)
                    pass

                if event.key == pygame.K_DELETE:
                    # if len(knot.points) > 3:
                    #     knot.delete_point_by_index(-1)
                    pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.points.append(event.pos)
                self.speeds.append((random.random() * 2, random.random() * 2))

    def run(self):

        pol = Polyline("MyScreenSaver version 0.1")
        knot = Knot()
        hlp = Helper()

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
    Handling two-dimensional vectors. Methods for working with vectors.
    """

    def __add__(self, x, y):  # sum of two vectors
        return x[0] + y[0], x[1] + y[1]

    def __sub__(self, x, y):  # subtraction of two vectors
        return x[0] - y[0], x[1] - y[1]

    def __mul__(self, vec, multiplier):  # multiply vector by number or vector
        if isinstance(multiplier, int) or isinstance(multiplier, float):
            return vec[0] * multiplier, vec[1] * multiplier
        else:
            return vec[0] * multiplier[0], vec[1] * multiplier[1]

    def int_pair(self, x, y):
        return tuple([int(x), int(y)])

    def len(self, v):
        return int((v[0] * v[0] + v[1] * v[1]) ** 0.5)


class Polyline(ScreenSaver, Vec2d):
    """
    Class of closed broken lines
    """

    # Recalculation of GCP coordinates
    def set_points(self, points, speeds):
        for p in range(len(points)):
            points[p] = self.__add__(points[p], speeds[p])
            if points[p][0] > SCREEN_DIM[0] or points[p][0] < 0:
                speeds[p] = (-speeds[p][0], speeds[p][1])
            if points[p][1] > SCREEN_DIM[1] or points[p][1] < 0:
                speeds[p] = (speeds[p][0], -speeds[p][1])

    # "Draw" points
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
    Calculation of curve points by added reference points
    """

    # Сглаживание ломаной
    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return self.__add__(self.__mul__(points[deg], alpha), self.__mul__(self.get_point(points, alpha, deg - 1), 1 - alpha))

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
            ptn.append(self.__mul__(self.__add__(points[i], points[i + 1]), 0.5))
            ptn.append(points[i + 1])
            ptn.append(self.__mul__(self.__add__(points[i + 1], points[i + 2]), 0.5))

            res.extend(self.get_points(ptn, count))
        return res


class Helper(ScreenSaver):
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
        data.append(['Del', 'Delete a point'])
        data.append(["", ""])
        data.append([str(self.steps), "Current points"])

        pygame.draw.lines(self.gameDisplay, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            self.gameDisplay.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            self.gameDisplay.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


# Main program
if __name__ == "__main__":
    saver = ScreenSaver("MyScreenSaver")
    saver.run()
