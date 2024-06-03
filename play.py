import torch
import numpy as np
from snake_game import SnakeGameAI
from dqn import DQNAgent
import pygame

def play(render=True):
    game = SnakeGameAI()
    state_dim = game.get_state().shape[0]
    action_dim = 4  # Number of possible actions: up, down, left, right
    agent = DQNAgent(state_dim, action_dim)

    # Load the model's state dictionary
    agent.model.load_state_dict(torch.load('snake_dqn_weights_1.pth'))
    agent.model.eval()  # Set the model to evaluation mode
    print("Model weights loaded.")

    # Disable exploration by setting epsilon to 0
    agent.epsilon = 0

    state = game.reset()
    done = False
    step = 0

    while not done:
        action = agent.act(state)
        state, reward, done = game.step(action)

        if render:
            game.render()
        step += 1

    print(f"Game over! Total steps: {step}, Score: {game.score}")

if __name__ == "__main__":
    play(render=True)
