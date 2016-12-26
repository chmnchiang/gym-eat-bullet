import numpy as np
from enum import IntEnum
from typing import Tuple

try:
    from .point import Point
    from .web_gui_backend import WebGUIBackend
except SystemError:
    from point import Point
    from web_gui_backend import WebGUIBackend


class EatBulletEnv(WebGUIBackend):

    metatdata = {'render.modes': ['human']}

    BlockSize = 4
    ActionNames = [ 'stay', 'up', 'down', 'left', 'right', ]
    Action = IntEnum('Action', ActionNames, start=0)
    Movesets = {
        Action.up: Point(0, 1),
        Action.down: Point(0, -1),
        Action.right: Point(1, 0),
        Action.left: Point(-1, 0),
    }

    def __init__(self,
                 grid_size: Tuple[int, int] = (20, 20),
                 *,
                 food_n: int = 3,
                 max_step=500) -> None:
        (h, w) = self.grid_size = grid_size
        super().__init__((h*self.BlockSize, w*self.BlockSize),
                         len(self.ActionNames), max_step=max_step)

        self.player_pos = None # type: Point
        self.food_n = food_n
        self.foods_pos = [] # type: List[Point]

    def _init(self):
        self.foods_pos = []
        for i in range(4):
            self.foods_pos.append(self._rand_pos(set(self.foods_pos)))

        self.player_pos = self._rand_pos(set(self.foods_pos))

    def _rand_pos(self, skip=set()) -> Point:
        pos = Point(np.random.randint(x) for x in self.grid_size)
        while pos in skip:
            pos = Point(np.random.randint(x) for x in self.grid_size)
        return pos

    def _step_env(self, act) -> Tuple[float, bool]:
        if act is None:
            return 0., False
        rew = 0.
        if act == self.Action.stay:
            return 0., False

        if act in self.Movesets:
            self.player_pos += self.Movesets[act]

            self.player_pos.x = np.clip(self.player_pos.x, 0, self.grid_size[0]-1)
            self.player_pos.y = np.clip(self.player_pos.y, 0, self.grid_size[1]-1)

        rew += self._check_eaten()

        return rew, False

    def _check_eaten(self) -> float:
        if self.player_pos not in self.foods_pos:
            return 0.

        self.foods_pos.remove(self.player_pos)
        self.foods_pos.append(self._rand_pos(self.foods_pos))

        return 1.

    def _to_rect(self, pt: Point) -> Tuple[int, int, int, int]:
        '''
        Return (xmin, ymin, xmax, ymax)
        '''
        return tuple(
            t * self.BlockSize for t in (pt.x, pt.y, pt.x+1, pt.y+1)
        )

    def _draw(self):
        # clear canvas
        self.draw.rectangle((0, 0, *self.frame_size), fill='black')

        # draw player
        loc = self._to_rect(self.player_pos)
        self.draw.ellipse(loc, fill='blue')

        # draw foods
        for pos in self.foods_pos:
            loc = self._to_rect(pos)
            self.draw.rectangle(loc, fill='green')

if __name__ == '__main__':
    env = EatBulletEnv(food_n=10)
    env.reset()

    import time
    try:
        while True:
            time.sleep(0.05)
            env.step(np.random.randint(5))
    except KeyboardInterrupt:
        env.end()


