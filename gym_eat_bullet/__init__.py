from gym.envs.registration import register

register(
    id='eatbullet2d-v0',
    entry_point='gym_grid_world.envs:EatBulletEnv',
    timestep_limit=500,
)
