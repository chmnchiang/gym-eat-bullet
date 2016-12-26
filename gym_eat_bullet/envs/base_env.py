from typing import Tuple
from PIL import Image, ImageDraw
import numpy as np 

import gym
from gym import spaces
from gym.utils import seeding

class BaseEnv(gym.Env):
    '''
    GUI Backend for simple enviroments
    '''
    metatdata = {'render.modes': ['human']}

    def __init__(self, 
                 frame_size: Tuple[int, int],
                 action_n: int,
                 *,
                 max_step: int = 100) -> None:
        '''
        frame_size: The dimension of the canvas
        action_n: Size of action space
        max_step: Maximum step player could play
        '''
        self.frame_size = frame_size

        # The canvas image
        self.image = Image.new('RGB', self.frame_size, 'black')
        # The imageDraw of the image, use self.draw.ellipse ...
        self.draw = ImageDraw.Draw(self.image)

        self.action_space = spaces.Discrete(action_n)
        self.observation_space = spaces.Box(0., 255., (*self.frame_size, 3))
        self.max_step = max_step

    def get_bitmap(self):
        '''
        Get the current bitmap in numpy array
        '''
        arr = np.array(self.image.getdata()).reshape((*self.frame_size, 3))
        return arr.astype('float32')

    # should be implemented
    def _init(self) -> None:
        '''
        Things to do when initialize
        '''
        pass

    def _step_env(self, action) -> Tuple[float, bool]:
        '''
        Stepping the enviroments.
        Should return (reward, done)
        '''
        raise NotImplementedError

    def _draw(self) -> None:
        '''
        Redraw the bitmap
        '''
        raise NotImplementedError

    # Gym functions
    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _reset(self):
        self.step_cnt = 0
        self._init()
        self._draw()
        return self.get_bitmap()

    def _step(self, action):
        action = int(action)
        print('Action =', action)
        assert 0 <= action < self.action_space.n
        
        rew, done = self._step_env(action)
        self.step_cnt += 1
        print(self.step_cnt, self.max_step)
        if self.max_step > 0 and self.step_cnt > self.max_step:
            done = True
        self._draw()
        obs = self.get_bitmap()
        info = None

        return obs, rew, done, info

    def _render(self, mode='human', close=False):
        pass
