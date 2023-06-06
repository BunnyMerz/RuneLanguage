from shape import Astroid, Square, RoundStar, Shape, Symb, Circle
import pygame
from pygame import draw as py_draw
import pygame_textinput


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

        manager = pygame_textinput.TextInputManager(validator=lambda x: validator(x, languages[0].letters))
        manager.value = "lorem ipsum dolor sit amet"
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

            self.draw_symbols(self.input_to_symbs(self.input.manager.value), 70, 70, debbug=self.debbug)
            self.window.blit(self.input.surface, (2, self.height - 22))

            pygame.display.update()

    def input_to_symbs(self, i: str):
        i = i.strip("\n").strip(" ")
        if i == '':
            return []
        runes = [self.runic.word(x.split(' ')) for x in i.split('\\')]
        return runes

    def draw_symbols(self, runes_list: list[list[Symb]], x=0, y=0, ratio=70, debbug=False, transcribe=False):
        ix = x
        for runes in runes_list:
            for symb in runes:
                if debbug:
                    self.runic.debugger().draw(self.window, x, y, ratio)
                symb.draw(self.window, x, y, ratio, transcribe)
                x += ratio+1
            y += ratio+1
            x = ix


language1 = Circle([chr(x) for x in range(97,123)])
language2 = Astroid([chr(x) for x in range(97,123)])
language3 = Square([chr(x) for x in range(97,123)])
m = Main(500, 1000, [language1,language2,language3])
m()