from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env

from gym_env import RL_Arena_Env


def main():
    env = RL_Arena_Env(grid_size=15)
    check_env(env)

    model = PPO(
        "MlpPolicy",
        env,
        verbose=1,
        n_steps=2048,
        batch_size=64,
        ent_coef=0.01,
    )
    model.learn(total_timesteps=300_000)
    model.save("paper_io_agent")


if __name__ == "__main__":
    main()
