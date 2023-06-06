from math import sin,cos,pi
from pygame import draw as py_draw
import pygame

pygame.init()
font = pygame.font.SysFont("roboto", 20)
def write(text) -> tuple[pygame.Surface, int, int]:
    text = font.render(text, True, (200, 200, 200))
    w,h = text.get_width(),text.get_height()
    return text, w, h

def square(t):
    t*=8
    if int(t) < 2:
        return (1 - t, 1)
    elif int(t) < 4:
        t-=2
        return (-1, 1 - t)
    elif int(t) < 6:
        t-=4
        return (-1 + t, -1)
    elif int(t) <= 8:
        t-=6
        return (1,-1 + t)
    
def circle(t):
    t *= 2*pi
    x = cos(t)
    y = sin(t)
    return (x,y)

def astroid(t):
    t*= 2*pi
    return (cos(t)**3,sin(t)**3)

def round_star(t):
    t*= 2*pi
    return (2*cos(t) + 5*cos(2*t/3), 2*sin(t) - 5*sin(2*t/3))

def distance(t1: tuple[int, int], t2: tuple[int, int]):
    return (t1[0] - t2[0])**2 + (t1[1] - t2[1])**2

def closest(self: "Shape", previous_letter: str, next_letters_indexes: list[int]):
    next_letters_coords = [self.index_coords(x) for x in next_letters_indexes]
    pv_coord = self.letter_coord(previous_letter)
    next_letters_distances = [distance(x, pv_coord) for x in next_letters_coords]
    return next_letters_indexes[next_letters_distances.index(min(next_letters_distances))]

def indexes(self: list, _item):
    return [i for i in range(len(self)) if self[i] == _item]


class Symb:
    def __init__(self, word, points, color=(100,130,100)):
        self.word = word
        self.points = points
        self.color = color

    def draw(self, surface, dx, dy, scale, transcription=False):
        if len(self.points) == 0:
            return
        if len(self.points) == 1:
            x,y = self.points[0]
            py_draw.circle(surface, self.color, (x*scale/2+dx,y*scale/2+dy), 2, 2)
        else:
            points = [(x*scale/2 + dx, y*scale/2 + dy) for x,y in self.points]
            py_draw.lines(surface, self.color, False, points, 2)
        if transcription:
            self.transcription(surface, dx, dy+scale)

    def transcription(self, surface, dx, dy):
        ts, w,h = write(self.word)
        surface.blit(ts, (dx, dy+h))

class Shape:
    def __init__(self, letters: list[str], parametric_fn: callable, choice_fn: callable) -> None:
        self._fn = parametric_fn
        self.letters = letters
        self.choice_fn = choice_fn

    def debugger(self):
        s = self.syllable(''.join(self.letters))
        s.color = (20,20,200)
        return s

    def index_coords(self, index) -> tuple[int, int]:
        return self._fn(index/(len(self.letters)))

    def letter_coord(self, next__previous, __next=None) -> tuple[int, int]:
        if __next == None:
            next_letter = next__previous
        else:
            previous_letter = next__previous
            next_letter = __next
            n_i = indexes(self.letters, next_letter)
            if len(n_i) != 1:
                return self.index_coords(self.choice_fn(self, previous_letter, n_i))
        
        return self.index_coords(self.letters.index(next_letter))
    
    def syllable(self, sequence: str) -> Symb:
        if len(sequence) == 0:
            return Symb("", [])
        previous = sequence[0]
        resp = [self.letter_coord(previous)]
        for l in range(1,len(sequence)):
            resp.append(self.letter_coord(previous, sequence[l]))
        return Symb(sequence, resp)
    
    def word(self, sequences: list[str]):
        return [self.syllable(x) for x in sequences]

class Astroid(Shape):
    def __init__(self, letters: list[str]):
        super().__init__(letters, astroid, closest)

class RoundStar(Shape):
    def __init__(self, letters: list[str]):
        super().__init__(letters, round_star, closest)

class Square(Shape):
    def __init__(self, letters: list[str]):
        super().__init__(letters, square, closest)

class Circle(Shape):
    def __init__(self, letters: list[str]):
        super().__init__(letters, circle, closest)