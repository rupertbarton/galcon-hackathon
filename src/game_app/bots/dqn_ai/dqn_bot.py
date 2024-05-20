from bots.abstract_bot import AbstractBot
from bots.dqn_ai.util import get_actions_in_state, get_observations_in_state
from game.galaxy import Galaxy
from game.player import Player

import random

# BATCH_SIZE is the number of transitions sampled from the replay buffer
# GAMMA is the discount factor as mentioned in the previous section
# EPS_START is the starting value of epsilon
# EPS_END is the final value of epsilon
# EPS_DECAY controls the rate of exponential decay of epsilon, higher means a slower decay
# TAU is the update rate of the target network
# LR is the learning rate of the ``AdamW`` optimizer
from bots.dqn_ai.dqn import DQN
from bots.dqn_ai.replay_memory import ReplayMemory, Transition

import math
import random
from collections import namedtuple, deque
from itertools import count
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F


class DQNBot(AbstractBot):
    
    def __init__(self, initial_map, file_to_load=None):
        super().__init__()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print("USING", self.device)
        
        self.BATCH_SIZE = 128
        self.GAMMA = 0.99
        self.EPS_START = 0.9
        self.EPS_END = 0.05
        self.EPS_DECAY = 20000
        self.TAU = 0.005
        self.LR = 1e-4
        
        # Get number of actions from gym action space
        self.n_actions = len(get_actions_in_state(initial_map))
        # Get the number of state observations
        self.n_observations = len(get_observations_in_state(Player("REPLACE_ME", "white", lambda: None), initial_map))
        
        self.policy_net = DQN(self.n_observations, self.n_actions).to(self.device)
        self.target_net = DQN(self.n_observations, self.n_actions).to(self.device)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        
        if file_to_load:
            self.load(file_to_load)
        
        self.optimizer = optim.AdamW(self.policy_net.parameters(), lr=self.LR, amsgrad=True)
        self.memory = ReplayMemory(100000)
        
        
        self.steps_done = 0
        
        self.last_action = None
        self.last_observations = None
        self.last_reward = None
        self.number_of_valid_moves_made = 0
        
    def reset(self):
        super().__init__()
        self.last_action = None
        self.last_observations = None
        self.last_reward = None
        
    def save(self, name):
        torch.save(self.policy_net.state_dict(), f"{name}_policy_net.pt")
        torch.save(self.target_net.state_dict(), f"{name}_target_net.pt")
        
    def load(self, name):
        self.policy_net.load_state_dict(torch.load(f"{name}_policy_net.pt"))
        self.policy_net.eval()
        self.target_net.load_state_dict(torch.load(f"{name}_target_net.pt"))
        self.target_net.eval()
    

    @property
    def possible_actions(self):
        return get_actions_in_state(self.current_state)
    
    @property
    def observations(self):
        return torch.tensor(get_observations_in_state(self.current_player, self.current_state), dtype=torch.float32, device=self.device).unsqueeze(0) if self.current_player else None

    def select_action(self, current_player: Player, current_state: Galaxy):
        super().create_orders(current_player, current_state)
        sample = random.random()
        eps_threshold = self.EPS_END + (self.EPS_START - self.EPS_END) * \
            math.exp(-1. * self.steps_done / self.EPS_DECAY)
        self.steps_done += 1
        if sample > eps_threshold:
            with torch.no_grad():
                # t.max(1) will return the largest column value of each row.
                # second column on max result is index of where max element was
                # found, so we pick action with the larger expected reward.
                return self.policy_net(self.observations).max(1).indices.view(1, 1)
        else:
            return torch.tensor([[random.randint(0, len(self.possible_actions) - 1)]], device=self.device, dtype=torch.long)


    def optimize_model(self):
        if len(self.memory) < self.BATCH_SIZE:
            return
        transitions = self.memory.sample(self.BATCH_SIZE)
        # Transpose the batch (see https://stackoverflow.com/a/19343/3343043 for
        # detailed explanation). This converts batch-array of Transitions
        # to Transition of batch-arrays.
        batch = Transition(*zip(*transitions))

        # Compute a mask of non-final states and concatenate the batch elements
        # (a final state would've been the one after which simulation ended)
        non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
                                            batch.next_state)), device=self.device, dtype=torch.bool)
        non_final_next_states = torch.cat([s for s in batch.next_state
                                                    if s is not None])
        state_batch = torch.cat(batch.state)
        action_batch = torch.cat(batch.action)
        reward_batch = torch.cat(batch.reward)

        # Compute Q(s_t, a) - the model computes Q(s_t), then we select the
        # columns of actions taken. These are the actions which would've been taken
        # for each batch state according to policy_net
        state_action_values = self.policy_net(state_batch).gather(1, action_batch)

        # Compute V(s_{t+1}) for all next states.
        # Expected values of actions for non_final_next_states are computed based
        # on the "older" target_net; selecting their best reward with max(1).values
        # This is merged based on the mask, such that we'll have either the expected
        # state value or 0 in case the state was final.
        next_state_values = torch.zeros(self.BATCH_SIZE, device=self.device)
        with torch.no_grad():
            next_state_values[non_final_mask] = self.target_net(non_final_next_states).max(1).values
        # Compute the expected Q values
        expected_state_action_values = (next_state_values * self.GAMMA) + reward_batch

        # Compute Huber loss
        criterion = nn.SmoothL1Loss()
        loss = criterion(state_action_values, expected_state_action_values.unsqueeze(1))

        # Optimize the model
        self.optimizer.zero_grad()
        loss.backward()
        # In-place gradient clipping
        torch.nn.utils.clip_grad_value_(self.policy_net.parameters(), 100)
        self.optimizer.step()
        
    def calculate_reward(self, orders):
        reward = -1
        
        for order in orders:
            source_planet = next(p for p in self.all_planets if p.id == order["source"])
            if (not source_planet.owner) or source_planet.owner.id != self.current_player.id:
                reward -= 5
            else:
                self.number_of_valid_moves_made += 1
                print("VALID MOVE MADE!!!")
        return reward
        
    def handle_iteration(self, current_player: Player, current_state: Galaxy, game_win: bool = None):
        done = not game_win is None
        current_observations = torch.tensor(get_observations_in_state(current_player, current_state), dtype=torch.float32, device=self.device).unsqueeze(0)
        
        if self.last_action:
            # Store the transition in memory
            if done:
                reward = self.last_reward + 1000 if game_win else self.last_reward - 100
            else:
                reward = self.last_reward
            self.memory.push(self.last_observations, self.last_action, current_observations, reward)
            
            

        # Perform one step of the optimization (on the policy network)
        self.optimize_model()

        # Soft update of the target network's weights
        # θ′ ← τ θ + (1 −τ )θ′
        target_net_state_dict = self.target_net.state_dict()
        policy_net_state_dict = self.policy_net.state_dict()
        for key in policy_net_state_dict:
            target_net_state_dict[key] = policy_net_state_dict[key]*self.TAU + target_net_state_dict[key]*(1-self.TAU)
        self.target_net.load_state_dict(target_net_state_dict)

        if not done:
            
            current_action = self.select_action(current_player, current_state)
            
            current_orders = self.possible_actions[current_action.item()]
            self.last_observations = current_observations
            self.last_reward = torch.tensor([self.calculate_reward(current_orders)], device=self.device)
            self.last_action = current_action
            return current_orders
