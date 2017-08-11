import cocos
import cocos.layer
import cocos.collision_model as cm
import cocos.euclid as eu

from collections import defaultdict
from pyglet.window import key


class Actor(cocos.sprite.Sprite):
    def __init__(self, image, x, y):
        super(Actor, self).__init__(image)
        self.position = eu.Vector2(x, y)
        self.cshape = cm.AARectShape(self.position,
                                     self.width * 0.5,
                                     self.height * 0.5)


    def move(self, offset):
        self.position += offset
        self.cshape.center += offset


    def update(self, elapsed):
        pass


    def collide(self, other):
        pass

class PlayerCannon(Actor):
    KEYS_PRESSED = defaultdict(int)

    def __init__(self, x, y):
        super(PlayerCannon, self).__init__('img/cannon.png', x, y)
        self.speed = eu.Vector2(200, 0)

    def update(self, elapsed):
        pressed = PlayerCannon.KEYS_PRESSED
        movement = pressed[key.RIGHT] - pressed[key.LEFT]
        w = self.width * 0.5
        if movement != 0 and w <= self.x <= self.parent.width - w:
            self.move(self.speed * movement * elapsed)

    def collide(self, other):
        other.kill()
        self.kill()


class GameLayer(cocos.layer.Layer):
    is_event_handler = True

    def on_key_press(self, k, _):
        PlayerCannon.KEYS_PRESSED[k] = 1

    def on_key_release(self, k, _):
        PlayerCannon.KEYS_PRESSED[k] = 0

    def __init__(self):
        super(GameLayer, self).__init__()
        w, h = cocos.director.director.get_window_size()
        self.width = w
        self.height = h
        self.lives = 3
        self.score = 0
        self.update_score()
        self.create_player()
        self.create_alien_group(100, 300)
        cell = 1.25 * 50
        self.collman = cm.CollisionManagerGrid(0, w, 0, h,
                                               cell, cell)
        self.schedule(self.update)

    def create_player(self):
        self.player = PlayerCannon(self.width * 0.5, 50)
        self.add(self.player)

    def update_score(self, score=0):
        self.score += score


if __name__ == '__main__':
    cocos.director.director.init(caption='Hello, Cocos')
    layer = MainLayer()
    scene = cocos.scene.Scene(layer)
    cocos.director.director.run(scene)