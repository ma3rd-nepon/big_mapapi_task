from io import BytesIO

from help.utils import get_response

import pygame


class BigMap:
    def __init__(self):
        self.image = None
        self.ll = 60.153191, 55.156353
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
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_w:
                self.ll[1] += 0.001

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