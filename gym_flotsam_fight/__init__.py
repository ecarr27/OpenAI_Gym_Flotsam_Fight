from gym.envs.registration import register

register(
    id='flotsam_fight-v0',
    entry_point='gym_flotsam_fight.envs:FlotsamFightEnv',
)