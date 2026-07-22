import pygame
from stable_baselines3 import PPO

from gym_env import RL_Arena_Env


def main():
    env = RL_Arena_Env(grid_size=15)
    model = PPO.load("paper_io_agent")

    obs, _ = env.reset()
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    done = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        if done:
            obs, _ = env.reset()
            done = False
        else:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, _ = env.step(int(action))
            done = terminated or truncated

        rgb = env.render()
        surf = pygame.surfarray.make_surface(rgb.transpose(1, 0, 2))
        screen.blit(pygame.transform.scale(surf, (600, 600)), (0, 0))
        pygame.display.flip()
        clock.tick(10)


if __name__ == "__main__":
    main()
