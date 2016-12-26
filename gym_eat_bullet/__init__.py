from gym.envs.registration import register

register(
    id='eatbullet2d-v0',
    entry_point='gym_eat_bullet.envs:EatBulletEnv',
    timestep_limit=500,
)
