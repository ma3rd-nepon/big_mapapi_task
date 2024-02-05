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
        self.show = False
        self.show_index = True
        self.addrs = None

        self.manager = pygame_gui.UIManager(size)
        self.layers_select = pygame_gui.elements.UIDropDownMenu(self.options, self.options[0],
                                                                pygame.Rect(10, 10, 200, 30),
                                                                self.manager)
        self.search_field = pygame_gui.elements.UITextEntryLine(pygame.Rect(175, 410, 300, 30), self.manager)
        self.error_field = pygame_gui.elements.UILabel(pygame.Rect(100, 380, 500, 30), '', self.manager)
        self.postal_btn = pygame_gui.elements.UIButton(pygame.Rect(550, 410, 100, 30), 'Скрыть индекс', self.manager)
        self.postal_btn.hide()
        self.clear_button = pygame_gui.elements.UIButton(pygame.Rect(450, 410, 100, 30), 'Сброс', self.manager)
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
            if e.key == pygame.K_f and pygame.key.get_mods() & pygame.KMOD_CTRL:
                self.show = not self.show
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
                self.search_pos()

            if e.key in [pygame.K_PAGEUP, pygame.K_PAGEDOWN, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN]:
                self.update_map()

        self.manager.process_events(e)

    def search_pos(self):
        if self.search_field.is_focused and self.search_field.text:
            try:
                toponym = get_toponym(geocode(self.search_field.text))
            except IndexError:
                self.error_field.set_text('Не найдено')
                self.clear_search()
                return

            self.ll = get_t_coords(toponym)
            self.addrs = get_toponym_address(toponym, self.show_index)
            self.error_field.set_text(f'{self.addrs[0]}, {self.addrs[1]}' if self.addrs[1] else f'{self.addrs[0]}')
            self.postal_btn.show()
            self.point = self.ll
            return

    def clear_search(self):
        self.point = None
        self.search_field.set_text('')
        self.postal_btn.hide()
        self.addrs = None
        self.update_map()

    def gui_event_handler(self, e):
        if e.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if e.ui_element == self.layers_select:
                self.layer = e.text
                self.update_map()

        if e.type == pygame_gui.UI_BUTTON_PRESSED:
            if e.ui_element == self.clear_button:
                self.clear_search()
            if e.ui_element == self.postal_btn:
                self.switch_postal()

    def switch_postal(self):
        self.show_index = not self.show_index
        self.postal_btn.set_text('Показать' if not self.show_index else 'Скрыть')
        if self.show_index:
            self.error_field.set_text(f'{self.addrs[1]}, {self.addrs[0]}' if self.addrs[1] else f'{self.addrs[0]}')

        else:
            self.error_field.set_text('')

    def draw(self, screen):
        screen.blit(self.image, (0, 0))
        self.manager.draw_ui(screen)

    def update_gui(self, delta):
        self.manager.update(time_delta=delta)
        uis = [self.search_field, self.error_field, self.clear_button, self.layers_select]
        for i in uis:
            if self.show:
                i.show()
            else:
                i.hide()


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
