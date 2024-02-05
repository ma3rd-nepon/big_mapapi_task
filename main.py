from io import BytesIO

from help.utils import *

import pygame
import pygame_gui


class BigMap:
    def __init__(self):
        self.image = None
        self.options = ['map', 'sat', 'sat,skl']
        self.ll = [60.153191, 55.156353]
        self.ll = get_t_coords(get_toponym(geocode('Миасс улица Макеева')))
        self.layer = 'map'
        self.z = 17
        self.point = None

        self.manager = pygame_gui.UIManager(size)
        self.layers_select = pygame_gui.elements.UIDropDownMenu(self.options, self.options[0],
                                                                pygame.Rect(10, 10, 200, 30),
                                                                self.manager)
        self.search_field = pygame_gui.elements.UITextEntryLine(pygame.Rect(175, 410, 300, 30), self.manager)
        self.error_field = pygame_gui.elements.UILabel(pygame.Rect(100, 380, 500, 30), '', self.manager)
        self.update_map()

    def update_map(self):
        map_params = {
            "l": self.layer,
            "ll": ",".join(map(str, self.ll)),
            "z": self.z,
            "size": "650,450"
        }
        if self.point is not None:
            map_params["pt"] = ','.join(map(str, self.ll)) + ',flag'
        nuka = get_static(**map_params)
        image = BytesIO(nuka)
        self.image = pygame.image.load(image)

    def e_handler(self, e):
        if e.type == pygame.KEYDOWN:
            print(e.key)
            if e.key == pygame.K_PAGEUP:
                self.z = min(self.z + 1, 21)
            if e.key == pygame.K_PAGEDOWN:
                self.z = max(self.z - 1, 0)

            if e.key == pygame.K_UP:
                self.ll[1] = min((self.ll[1] + 70 * 2 ** (-self.z)), 88)
            if e.key == pygame.K_DOWN:
                self.ll[1] = max((self.ll[1] - 70 * 2 ** (-self.z)), -88)
            if e.key == pygame.K_LEFT:
                self.ll[0] = (self.ll[0] + 180 - (200 * (2 ** (-self.z)))) % 360 - 180
            if e.key == pygame.K_RIGHT:
                self.ll[0] = (self.ll[0] + 180 + (200 * (2 ** (-self.z)))) % 360 - 180

            if e.key == pygame.K_RETURN:
                if self.search_field.is_focused and self.search_field.text:
                    try:
                        self.ll = get_t_coords(get_toponym(geocode(self.search_field.text)))
                        self.error_field.set_text('')
                        self.point = self.ll
                    except IndexError:
                        self.error_field.set_text('Не найдено')

            if e.key in [pygame.K_PAGEUP, pygame.K_PAGEDOWN, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN]:
                self.update_map()

        self.manager.process_events(e)

    def gui_event_handler(self, e):
        if e.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if e.ui_element == self.layers_select:
                self.layer = e.text
                self.update_map()

    def draw(self, screen):
        screen.blit(self.image, (0, 0))
        self.manager.draw_ui(screen)

    def update_gui(self, delta):
        self.manager.update(time_delta=delta)


pygame.init()
size = w, h = 650, 450
screen = pygame.display.set_mode(size)
app = BigMap()
clock = pygame.time.Clock()

run = False
while not not not not not run:
    delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = True
        app.e_handler(event)
        app.gui_event_handler(event)
    screen.fill('black')
    app.update_gui(delta)
    app.draw(screen)
    pygame.display.update()
pygame.quit()
