#!/usr/bin/python2.5
import pyglet as p
import random
#import math


def main():
    random.seed('watermeloen')
    HexagonClient().run()


class Grid(object):
    def __init__(self):
        self._grid = {}

    def __getitem__(self, coord):
        x, y = coord
        if y not in self._grid:
            self._grid[y] = {}
        if x not in self._grid[y]:
            self._grid[y][x] = Tile(x=x, y=y)
        return self._grid[y][x]

    def tiles_in_range(self, bottomleft, topright):
        return [self[x, y]
                for x in range(bottomleft[0], topright[0])
                for y in range(bottomleft[1], topright[1])]

grid = Grid()


class Tile(object):
    def __init__(self, x=None, y=None):
        self._flags = 0  # 0b0000000
        self._x = x
        self._y = y
        self._type = None
        self._noise = None
        #self.gen_type()
        #self._type = random.randint(0, 4)

    @property
    def noise(self):
        if (self._noise is None):
            random.seed(self._x + self._y)
            self._noise = random.randint(0, 100)
            print 'noise: ', self._noise
        return self._noise

    @property
    def type(self):
        if (self._type is None):
            if (self._x % 10 == self._y % 10 == 0):
                tval = self.noise
            else:
                co = (self._x / 10, self._y / 10)
                v = [grid[(co[0] + dx, co[1] + dy)].noise
                     for dy in [0, 10]
                     for dx in [0, 10]]
                print 'v', v, 'co', co, 'selfxy', self._x, self._y
                v = [v[0] * (10 - self._x % 10) / 10 +
                     v[1] * (self._x % 10) / 10,
                     v[2] * (10 - self._x % 10) / 10 +
                     v[3] * (self._x % 10) / 10]
                print v
                tval = v[0] * (10 - self._y % 10) / 10 + \
                    v[1] * (self._y % 10) / 10
            print tval
            self._type = tval / 50
        return self._type

    def interpolate(v0, v, v1):
        return

    @property
    def coordinate(self):
        if self._x is not None:  # assumed _x & _y both/neither set
            return (self._x, self._y)
        else:
            None

    def __repr__(self):
        return "<%s x=%i y=%i>" % (self.__class__.__name__,
                                   self._x,
                                   self._y)


class HexagonClient(p.window.Window):
    def __init__(self):
        super(HexagonClient, self).__init__(1000, 1000)
        self.grid = Grid()
        self.tile_size = (75 + 1, 87 + 1)
        self.map_pos = (0, 0)  # map position to wich te screen is relarive
        self.screen_pos = (0, 0)  # screen postition relative to the map_pos
        self.hexagons = (
            p.resource.image("hexagon_water.png").get_texture(),
            p.resource.image("hexagon_grass.png").get_texture(),
            p.resource.image("hexagon_rock.png").get_texture(),
            p.resource.image("hexagon_field.png").get_texture(),
            p.resource.image("hexagon_forrest.png").get_texture(),
        )
        #for hexagon in self.hexagons:
        #    hexagon.anchor_x = hexagon.width / 2
        #    hexagon.anchor_y = hexagon.height / 2
        self.co_label = p.text.Label('test',
                                     anchor_x='center',
                                     anchor_y='center',
                                     color=(255, 0, 0, 255))

    @property
    def client_window_size(self):
        return (self.width, self.height)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.screen_pos = (
            self.screen_pos[0] - dx,
            self.screen_pos[1] - dy
        )

    def on_draw(self):
        p.gl.glEnable(p.gl.GL_BLEND)
        p.gl.glBlendFunc(p.gl.GL_SRC_ALPHA, p.gl.GL_ONE_MINUS_SRC_ALPHA)
        self.clear()
        for tile in self.grid.tiles_in_range(*self.visibleTileRange()):
            co = [(tile.coordinate[a] + self.map_pos[a]) *
                  self.tile_size[a] -
                  self.screen_pos[a] for a in range(2)]
            if tile.coordinate[0] % 2 == 1:
                co[1] -= self.tile_size[1] / 2
            self.hexagons[tile.type].blit(*co)

            #self.co_label.text = "%i, %i" % tile.coordinate
            #self.co_label.x = co[0]
            #self.co_label.y = co[1]
            #self.co_label.draw()

    def run(self):
        p.app.run()

    def visibleTileRange(self):
        """returns the bottomleft and topright visible tiles"""
        return (
            tuple((self.map_pos[a] +
                   (self.screen_pos[a]) /
                   self.tile_size[a] for a in range(2))),
            tuple((self.map_pos[a] +
                   (self.screen_pos[a] + self.client_window_size[a]) /
                   self.tile_size[a] for a in range(2)))
        )


if __name__ == "__main__":
    main()
