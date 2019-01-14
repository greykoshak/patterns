import pygame
import random
import math

SCREEN_DIM = (800, 600)


# ÐœÐµÑ‚Ð¾Ð´Ñ‹ Ð´Ð»Ñ Ñ€Ð°Ð±Ð¾Ñ‚Ñ‹ Ñ Ð²ÐµÐºÑ‚Ð¾Ñ€Ð°Ð¼Ð¸

class Vec2d:
    def __init__(self, coords):
        self.coords = coords

    def __sub__(self, other):  # Ñ€Ð°Ð·Ð½Ð¾ÑÑ‚ÑŒ Ð´Ð²ÑƒÑ… Ð²ÐµÐºÑ‚Ð¾Ñ€Ð¾Ð²
        return Vec2d((self.coords[0] - other.coords[0], self.coords[1] - other.coords[1]))


    def __add__(self, other):  # ÑÑƒÐ¼Ð¼Ð° Ð´Ð²ÑƒÑ… Ð²ÐµÐºÑ‚Ð¾Ñ€Ð¾Ð²
        return Vec2d((self.coords[0] + other.coords[0], self.coords[1] + other.coords[1]))

    def __len__(self):  # Ð´Ð»Ð¸Ð½Ð½Ð° Ð²ÐµÐºÑ‚Ð¾Ñ€Ð°
        return math.sqrt(self.coords[0]**2 + self.coords[1]**2)


    def __mul__(self, obj):  # ÑƒÐ¼Ð½Ð¾Ð¶ÐµÐ½Ð¸Ðµ Ð²ÐµÐºÑ‚Ð¾Ñ€Ð° Ð½Ð° Ñ‡Ð¸ÑÐ»Ð¾ Ð¸ ÑÐºÐ°Ð»ÑÑ€Ð½Ð¾Ðµ Ð¿Ñ€Ð¾Ð¸Ð·Ð²ÐµÐ´ÐµÐ½Ð¸Ðµ
        if isinstance(obj, Vec2d):
            return self.coords[0] * obj.coords[0] + self.coords[1] * obj.coords[1]
        else:
            return Vec2d((self.coords[0] * obj, self.coords[1] * obj))

    def int_pair(self):
        return (int(self.coords[0]), int(self.coords[1]))

    def __getitem__(self, ind):
        return self.coords[ind]

    def __eq__(self, coords):
        self.coords = coords

class Polyline:
    def __init__(self, screen_dim = (800, 600)):
        self.points = []
        self.speeds = []
        self.screen_dim = screen_dim

    def add_point(self, point, speed):
        self.points.append(point)
        self.speeds.append(speed)

    def remove_point(self, ind):
        del self.points[ind]
        del self.speeds[ind]

    def clear(self):
        self.points = []
        self.speeds = []

    def __len__(self):
        return len(self.points)

    def increase_speed(self, k):
        for i in range(len(self.speeds)):
            self.speeds[i] = self.speeds[i] * k


    def decrease_speed(self, k):
        for i in range(len(self.speeds)):
            self.speeds[i] = self.speeds[i] * (1 / k)

    # ÐŸÐµÑ€ÑÑ‡Ð¸Ñ‚Ñ‹Ð²Ð°Ð½Ð¸Ðµ ÐºÐ¾Ð¾Ñ€Ð´Ð¸Ð½Ð°Ñ‚ Ð¾Ð¿Ð¾Ñ€Ð½Ñ‹Ñ… Ñ‚Ð¾Ñ‡ÐµÐº
    def set_points(self):
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p][0] > self.screen_dim[0] or self.points[p][0] < 0:
                self.speeds[p] = Vec2d((- self.speeds[p][0], self.speeds[p][1]))
            if self.points[p][1] > self.screen_dim[1] or self.points[p][1] < 0:
                self.speeds[p] = Vec2d((self.speeds[p][0], -self.speeds[p][1]))


    def draw_points(self, game, style="points", width=3, color=(255, 255, 255)):
        self.draw_points_base(self.points, game, style, width, color)

    # "ÐžÑ‚Ñ€Ð¸ÑÐ¾Ð²ÐºÐ°" Ñ‚Ð¾Ñ‡ÐµÐº
    @staticmethod
    def draw_points_base(points, game, style="points", width=3, color=(255, 255, 255)):
        if style == "line":
            for p_n in range(-1, len(points) - 1):
                game.draw.line(gameDisplay, color, points[p_n].int_pair(),
                                 points[p_n + 1].int_pair(), width)

        elif style == "points":
            for p in points:
                game.draw.circle(gameDisplay, color,
                                   p.int_pair(), width)

class Knot(Polyline):

    def __init__(self, steps = 35, screen_dim = (800, 600)):
        super().__init__(screen_dim)
        self.curve_points = []
        self.steps = steps

    def add_point(self, point, speed):
        super().add_point(point, speed)
        return self.get_knot()

    def remove_point(self, ind):
        super().remove_point(ind)
        return self.get_knot()

    def set_points(self):
        super().set_points()
        return self.get_knot()

    def clear(self):
        super().clear()
        self.curve_points = []

    def set_steps(self, steps):
        self.steps = steps

    # Сглаживание ломаной

    @staticmethod
    def get_point(points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + Knot.get_point(points, alpha, deg - 1) * (1 - alpha)

    @staticmethod
    def get_points(base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(Knot.get_point(base_points, i * alpha))
        return res


    def get_knot(self):
        self.curve_points = []
        if len(self.points) < 3:
            return []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)

            self.curve_points.extend(Knot.get_points(ptn, self.steps))
        return self.curve_points

    def draw_points(self, game, style="points", width=3, color=(255, 255, 255)):
        self.draw_points_base(self.curve_points, game, style, width, color)

    def draw_support_points(self, game, style="points", width=3, color=(255, 255, 255)):
        self.draw_points_base(self.points, game, style, width, color)

class Manager:

    def __init__(self, screen_dim = (800, 600)):
        self.screen_dim = screen_dim
        self.knots = [Knot(screen_dim = self.screen_dim)]
        self.current_knot = 0
        self.current_point = 0

    def clear(self):
        self.knots = [Knot(screen_dim = self.screen_dim)]
        self.current_knot = 0
        self.current_point = 0

    def add_knot(self):
        self.knots.append(Knot(screen_dim = self.screen_dim))
        self.current_knot = len(self.knots) - 1

    def remove_knot(self):
        del self.knots[self.current_knot]

        if self.current_knot > 0 and self.current_knot == len(self.knots):
            self.current_knot -= 1

        if len(self.knots) == 0:
            self.knots.append(Knot(screen_dim = self.screen_dim))

    def prev_knot(self):
        self.current_knot = self.current_knot - 1 if self.current_knot > 0 \
        else len(self.knots) - 1

        self.current_point = 0

    def next_knot(self):
        self.current_knot = (self.current_knot + 1) % len(self.knots)
        self.current_point = 0

    def add_point(self, point, speed):
        self.knots[self.current_knot].add_point(point, speed)

    def prev_point(self):
        knots_count = len(self.knots[self.current_knot])
        if knots_count > 0:
            self.current_point = (self.current_point - 1) \
            if self.current_point > 0 \
            else knots_count - 1

    def next_point(self):
        knots_count = len(self.knots[self.current_knot])
        if knots_count > 0:
            self.current_point = (self.current_point + 1) % knots_count

    def remove_point(self):
        try:
            self.knots[self.current_knot].remove_point(self.current_point)
        except IndexError:
            pass

        if self.current_point == len(self.knots[self.current_knot]) and self.current_point > 0:
            self.current_point -= 1

    def set_points(self):
        for knot in self.knots:
            knot.set_points()

    def set_steps(self, steps):
        for knot in self.knots:
            knot.set_steps(steps)

    def draw_points(self, game, style="points", width=3, color=(255, 255, 255)):
        for knot in self.knots:
            knot.draw_points(game, style, width, color)

    def draw_support_points(self, game, style="points", width=3, color=(255, 255, 255)):
        for knot in self.knots:
            knot.draw_support_points(game, style, width, color)

    def increase_speed(self, k = 2):
        self.knots[self.current_knot].increase_speed(k)

    def decrease_speed(self, k = 2):
        self.knots[self.current_knot].decrease_speed(k)

# ÐžÑ‚Ñ€Ð¸ÑÐ¾Ð²ÐºÐ° ÑÐ¿Ñ€Ð°Ð²ÐºÐ¸
def draw_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More steps"])
    data.append(["Num-", "Less steps"])
    data.append(["Up", "Next curve"])
    data.append(["Down", "Prev curve"])
    data.append(["Right", "Next point"])
    data.append(["Left", "Prev point"])
    data.append(["A", "Add new curve"])
    data.append(["X", "Remove entire current curve and all its points"])
    data.append(["E", "Remove current point of current curve"])
    data.append(["I", "Increase current curve speed"])
    data.append(["D", "Decrease current curve speed"])
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
    show_help = False
    pause = True

#    knot = Knot()

    manager = Manager(SCREEN_DIM)

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
                    manager.clear()
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                    manager.set_steps(steps)
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0
                    manager.set_steps(steps)
                if event.key == pygame.K_DOWN:
                    manager.prev_knot()
                if event.key == pygame.K_UP:
                    manager.next_knot()
                if event.key == pygame.K_LEFT:
                    manager.prev_point()
                if event.key == pygame.K_RIGHT:
                    manager.next_point()
                if event.key == pygame.K_a:
                    manager.add_knot()
                if event.key == pygame.K_x:
                    manager.remove_knot()
                if event.key == pygame.K_e:
                    manager.remove_point()
                if event.key == pygame.K_i:
                    manager.increase_speed()
                if event.key == pygame.K_d:
                    manager.decrease_speed()

            if event.type == pygame.MOUSEBUTTONDOWN:
                manager.add_point(Vec2d(event.pos), Vec2d((random.random() * 2,
                               random.random() * 2)))

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        manager.draw_support_points(pygame)
        manager.draw_points(pygame, "line", 3, color)
        if not pause:
            manager.set_points()
        if show_help:
            draw_help()

        font1 = pygame.font.SysFont("courier", 24)
        gameDisplay.blit(font1.render(
                    f"Current curve: {manager.current_knot}",
                    True, (128, 128, 255)), (10, 10))

        gameDisplay.blit(font1.render(
                    f"Current point: {manager.current_point}",
                    True, (128, 128, 255)), (10, 40))
        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
