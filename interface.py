import pygame

BORDER_WIDTH = 2
BTN_COLOR = (32, 32, 32)
TEXT_COLOR = (32, 32, 32)
TEXT_SIZE = 32
ARROW_SIZES = 3, 21
LINES_SPACE = 7
NODE_SIZE = 20
NODE_COLOR = (255, 0, 0)
LINE_WIDTH = 3
LINE_COLOR = (0, 0, 255)


class Button:
    def __init__(self, text, target, x, y, dx, dy):
        self.x1 = x
        self.y1 = y
        self.x2 = x + dx
        self.y2 = y + dy
        self.text = text
        self.func = target

    def activate(self):
        self.func()

    def __contains__(self, coords):
        x, y = coords
        return self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2

    def draw(self, surface):
        r = pygame.Rect(self.x1, self.y1, self.x2 - self.x1, self.y2 - self.y1)
        pygame.draw.rect(surface, BTN_COLOR, r, BORDER_WIDTH)
        font = pygame.font.SysFont('couriernew', TEXT_SIZE)
        text = font.render(self.text, True, BTN_COLOR)
        surface.blit(text, (self.x1 + 10, self.y1 + 10))


def draw_arrow(surface, x1, y1, x2, y2, pos=-0.05):
    pygame.draw.line(surface, LINE_COLOR, (x1, y1), (x2, y2), LINE_WIDTH)

    l = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    a = x2 - (x2 - x1) * pos, y2 - (y2 - y1) * pos
    h = x2 - (x2 - x1) * (pos + ARROW_SIZES[1] / l), y2 - (y2 - y1) * (pos + ARROW_SIZES[1] / l)

    b = h[0] - (y2 - y1) * (ARROW_SIZES[0] / l * 2), h[1] + (x2 - x1) * (ARROW_SIZES[0] / l * 2)
    c = h[0] + (y2 - y1) * (ARROW_SIZES[0] / l * 2), h[1] - (x2 - x1) * (ARROW_SIZES[0] / l * 2)

    pygame.draw.polygon(surface, LINE_COLOR, (a, b, c))


def draw_self_lines(surface, x, y, r=NODE_SIZE, count=1):
    for k in range(1, count + 1):
        kk = 1 + k * 0.2
        pygame.draw.circle(surface, LINE_COLOR, (x - r * kk, y - r * kk), r * kk, LINE_WIDTH)


def draw_lines(surface, src, dst, count, arrows=False):
    dlt = LINES_SPACE * (count - 1)
    l = ((src[0] - dst[0]) ** 2 + (src[1] - dst[1]) ** 2) ** 0.5

    x1 = src[0] - (dst[1] - src[1]) * (dlt / l / 2)
    y1 = src[1] + (dst[0] - src[0]) * (dlt / l / 2)
    x2 = dst[0] - (dst[1] - src[1]) * (dlt / l / 2)
    y2 = dst[1] + (dst[0] - src[0]) * (dlt / l / 2)

    for _ in range(count):
        if arrows:
            draw_arrow(surface, x1, y1, x2, y2, NODE_SIZE / l)
        else:
            pygame.draw.line(surface, LINE_COLOR, (x1, y1), (x2, y2), LINE_WIDTH)
        x1 += (dst[1] - src[1]) * (LINES_SPACE / l)
        x2 += (dst[1] - src[1]) * (LINES_SPACE / l)
        y1 -= (dst[0] - src[0]) * (LINES_SPACE / l)
        y2 -= (dst[0] - src[0]) * (LINES_SPACE / l)


def draw_node(surface, x, y, name, selected=False):
    pygame.draw.circle(surface, NODE_COLOR, (x, y), NODE_SIZE)
    if selected:
        pygame.draw.circle(surface, TEXT_COLOR, (x, y), NODE_SIZE, BORDER_WIDTH)
    font = pygame.font.SysFont('couriernew', TEXT_SIZE)
    text = font.render(name, True, TEXT_COLOR)
    surface.blit(text, (x - (len(name) / 2 * NODE_SIZE), y - NODE_SIZE * 0.8))


def is_in_node(pos, node):
    return ((pos[0] - node[0]) ** 2 + (pos[1] - node[1]) ** 2) ** 0.5 <= NODE_SIZE
