import torch
import numpy as np # Still used for initial array creation if needed, and by other libs

# It's good practice to define the device globally or pass it around.
# For now, let's assume it might be defined in main.py and passed or imported.
# As a placeholder for now, modified during integration with main.py:
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class player:
    def __init__(self, path_num, device_to_use=None):
        global device # Allow updating if a device is passed
        if device_to_use:
            device = device_to_use

        self.path_num = path_num
        # Initialize as PyTorch tensors on the specified device
        self.probability = torch.ones(path_num, device=device) / path_num
        self.estimate_probability = torch.ones(path_num, device=device) / path_num
        # self.probability = self.create_random() # If create_random is implemented, it should return a tensor

    def get_probability(self): # [prob1, prob2, prob3]
        return self.probability

class all_player:
    def __init__(self, player_num, path_num, device_to_use=None):
        global device # Allow updating if a device is passed
        if device_to_use:
            device = device_to_use

        self.players_strategy = list()
        self.path_num = path_num
        self.player_num = player_num
        for i in range(player_num):
            # Pass the device to each player instance
            self.players_strategy.append(player(path_num, device_to_use=device))
        # self.players_strategy = np.asarray(self.players_strategy) # This would create an array of objects.
        # If batch operations on all probabilities are needed, consider stacking them into a single tensor:
        # Example: self.all_probs_tensor = torch.stack([p.probability for p in self.players_strategy])
        # For now, keeping it as a list of player objects.

    def all_player_probability(self):
        for i in range(self.player_num):
            # .cpu().numpy() might be needed if printing tensors directly is too verbose or for formatting
            print(f"Player {i}: {self.players_strategy[i].get_probability().cpu().numpy()}")

# Example of how device might be set from outside (e.g. main.py)
def set_global_device(dev):
    global device
    device = dev
