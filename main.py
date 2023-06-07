from shape import Astroid, Square, RoundStar, Shape, Symb, Circle
import pygame
from pygame import draw as py_draw
import pygame_textinput
# from testes import ex1, ex2, ex3
# string_test = ex3
string_test = ""


def write_number_line(number, size):
    font = pygame.font.SysFont("roboto", size)
    text = font.render(str(number)+'.', True, (200, 200, 200))
    w,h = text.get_width(),text.get_height()
    return text, w, h

def validator(word: str, compared):
    for letter in word:
        if letter not in compared + [' ', '\\']:
            return False
    return True

class Main:
    def __init__(self, height: int, width: int, languages: Shape):
        pygame.init()
        pygame.key.set_repeat(200, 25)
        self.height = height
        self.width = width
        
        self.runics: list[Shape] = languages
        self.runic_i: int = 0
        self.debbug = False
        self.scale = 70

        manager = pygame_textinput.TextInputManager(validator=lambda x: validator(x, languages[0].letters))
        manager.value = string_test
        self.input = pygame_textinput.TextInputVisualizer(manager=manager, font_object=pygame.font.SysFont("Consolas", 20))
        
        self.clock = pygame.time.Clock()
        self.window: pygame.Surface = pygame.display.set_mode((width,height),pygame.RESIZABLE, pygame.NOFRAME)

    @property
    def runic(self):
        return self.runics[self.runic_i]

    def __call__(self):
        while(1):
            self.window.fill((225, 225, 225))
            self.clock.tick(60)
            events = pygame.event.get()
            self.input.update(events)
            for e in events:
                if pygame.QUIT == e.type: ## Avoid freezing
                    pygame.quit()
                    break
                if pygame.KEYDOWN == e.type:
                    if pygame.K_TAB == e.key:
                        self.runic_i = (self.runic_i+1) % len(self.runics)
                    if pygame.K_CAPSLOCK == e.key:
                        self.debbug = not self.debbug
                    if pygame.K_EQUALS == e.key:
                        self.scale += 5
                    if pygame.K_MINUS == e.key:
                        self.scale -= 5
                        self.scale = max(5, self.scale)

            self.draw_symbols(self.input_to_symbs(self.input.manager.value),x=self.scale, y=self.scale, scale=self.scale, debbug=self.debbug)
            self.window.blit(self.input.surface, (2, self.height - 22))

            pygame.display.update()

    def input_to_symbs(self, i: str):
        i = i.strip("\n").strip(" ")
        if i == '':
            return []
        runes = [self.runic.word(x.split(' ')) for x in i.split('\\')]
        return runes

    def draw_symbols(self, runes_list: list[list[Symb]], x=0, y=0, scale=70, debbug=False, transcribe=False):
        ix = x
        counter = 1
        for runes in runes_list:
            n,ws,hs = write_number_line(counter, scale//3)
            self.window.blit(n, [x-1*scale, y])
            counter += 1
            for symb in runes:
                if debbug:
                    self.runic.debugger().draw(self.window, x, y, scale)
                symb.draw(self.window, x, y, scale, transcribe)
                x += scale+1
            y += scale+1
            x = ix


language1 = Circle([chr(x) for x in range(97,123)])
language3 = Square([chr(x) for x in range(97,123)])
m = Main(500, 1000, [language1,language3])
m()