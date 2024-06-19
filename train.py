from snake_game import SnakeGameAI
from dqn import DQNAgent
import numpy as np
import torch

def train(render=False, save_model=True):
    game = SnakeGameAI()
    state_dim = game.get_state().shape[0]
    action_dim = 4  # Number of possible actions: up, down, left, right
    agent = DQNAgent(state_dim, action_dim)

    episodes = 75
    render_every_step = 10  # Render every 10 steps within an episode

    for e in range(episodes):
        state = game.reset()
        total_reward = 0
        done = False
        step = 0

        while not done:
            action = agent.act(state)
            next_state, reward, done = game.step(action)
            total_reward += reward
            agent.remember(state, action, reward, next_state, done)
            state = next_state

            agent.replay()

            # Render the game every 'render_every_step' steps
            if render and step % render_every_step == 0:
                game.render()
            step += 1

        agent.update_target_model()
        print(f"Episode {e + 1}/{episodes}, Total Reward: {total_reward}")
    
    if save_model:
        torch.save(agent.model.state_dict(), 'snake_dqn_weights_2.pth')
        print("Model weights saved.")

if __name__ == "__main__":
      # Set render=True to see the game while training
      train(render=True)
