from io import BytesIO

from help.utils import get_response

import pygame


class BigMap:
    def __init__(self):
        self.image = None
        self.ll = [60.153191, 55.156353]
        self.layer = 'map'
        self.z = 17

        self.update_map()

    def update_map(self):
        map_params = {
            "l": self.layer,
            "ll": ",".join(map(str, self.ll)),
            "z": self.z,
            "size": "650,450"
        }

        image = BytesIO(get_response('content', 'static', **map_params))
        self.image = pygame.image.load(image)

    def e_handler(self, e):
        coff = 300  # coff = 10 ** -(self.z // 4)
        if e.type == pygame.KEYDOWN:
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

            self.update_map()

    def draw(self, screen):
        screen.blit(self.image, (0, 0))


pygame.init()
size = w, h = 650, 450
screen = pygame.display.set_mode(size)
app = BigMap()

run = False
while not not not not not run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = True
        app.e_handler(event)
    screen.fill('black')
    app.draw(screen)
    pygame.display.flip()
pygame.quit()