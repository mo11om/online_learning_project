import torch
import numpy as np # Retain numpy for scipy and poly1d if not fully replaced
import env # Should now use the PyTorch version of env
import copy
from scipy.optimize import minimize

# Assuming device is set globally in env.py or passed explicitly
# from env import device # Or get it from a central config

# Helper function for polynomial evaluation with PyTorch tensors
def torch_polyval(p_coeffs_tensor, x_tensor):
    """
    Evaluates a polynomial at x_tensor.
    p_coeffs_tensor: 1D tensor of polynomial coefficients (highest power first).
    x_tensor: scalar or tensor of points to evaluate the polynomial at.
    """
    val = torch.zeros_like(x_tensor, dtype=torch.float32, device=x_tensor.device)
    for i, coeff in enumerate(p_coeffs_tensor):
        val += coeff * (x_tensor ** (len(p_coeffs_tensor) - 1 - i))
    return val

class congestion_game(env.all_player):
    def __init__(self, coefficient, path_num, player_num, device_to_use=None):
        super().__init__(player_num=player_num, path_num=path_num, device_to_use=device_to_use)
        self.device = device_to_use if device_to_use else env.device # Use the globally set device from env

        self.cost_func_coeffs = [] # Store coefficients as tensors
        for i_coeffs in coefficient:
            # Store coefficients as tensors on the correct device
            self.cost_func_coeffs.append(torch.tensor(i_coeffs, dtype=torch.float32, device=self.device))

        # self.cost_func = list() # Original np.poly1d objects, can be kept for non-tensor use or removed
        # for i in coefficient :
        #      self.cost_func.append(np.poly1d(i))


        self.path_cost = torch.zeros(path_num, device=self.device, dtype=torch.float32)
        self.total_path_select = dict() # record all player's final choice for each round
        self.hindsight_real_diff = 0.0 # Should be float
        self.average_regret = []
        self.potential_value = []
        self.all_play_total_path_select = []


    # def get_cost_func(self): # This would return poly1d objects
    #     return self.cost_func

    def get_path_cost_torch(self, path_idx, num_drivers_on_path):
        """Calculates cost for a path using torch tensors."""
        if isinstance(num_drivers_on_path, int):
            num_drivers_on_path = torch.tensor(float(num_drivers_on_path), device=self.device)
        elif isinstance(num_drivers_on_path, torch.Tensor):
            num_drivers_on_path = num_drivers_on_path.to(self.device).float()

        coeffs = self.cost_func_coeffs[path_idx]
        return torch_polyval(coeffs, num_drivers_on_path)

    def random_select_cost(self):
        self.total_path_select = {new_list: [] for new_list in range(self.path_num)}

        # Collect all estimate probabilities into a tensor for batch processing if possible
        # For now, individual selection:
        for i in range(self.player_num):
            # Ensure probability is on CPU for numpy conversion if torch.multinomial needs it,
            # or use torch.multinomial directly which handles device tensors.
            # Probabilities must be 1D for torch.multinomial
            player_probs = self.players_strategy[i].estimate_probability.squeeze()
            if player_probs.sum() == 0: # Avoid error with all zero probabilities
                # Uniform selection if all probs are zero, or handle error
                choice_path_tensor = torch.randint(0, self.path_num, (1,), device=self.device)
            else:
                choice_path_tensor = torch.multinomial(player_probs, 1)
            
            self.total_path_select[choice_path_tensor.item()].append(i)

        path_sum_dict = {} # For self.all_play_total_path_select

        # Calculate path costs using PyTorch tensors
        path_counts = torch.zeros(self.path_num, device=self.device, dtype=torch.float32)
        for path_idx, drivers in self.total_path_select.items():
            path_counts[path_idx] = len(drivers)
            path_sum_dict[path_idx] = len(drivers)

        for path_idx in range(self.path_num):
            self.path_cost[path_idx] = self.get_path_cost_torch(path_idx, path_counts[path_idx])

        self.all_play_total_path_select.append(path_sum_dict)
        return self.path_cost # Returns a torch tensor

    @staticmethod
    def object_torch(strategy_tensor, last_strategy_tensor, cost_tensor, learn_rate):
        # Ensure all inputs are torch tensors on the same device
        # strategy_tensor, last_strategy_tensor, cost_tensor should be 1D
        term1 = torch.dot(cost_tensor, strategy_tensor)
        diff_strategy = strategy_tensor - last_strategy_tensor
        term2 = (1.0 / learn_rate) * torch.dot(diff_strategy, diff_strategy)
        return term1 + term2

    @staticmethod
    def constraint_numpy(strategy_numpy): # For SciPy
        return np.sum(strategy_numpy) - 1.0

    @staticmethod
    def refresh_strategy_minimize(last_strategy_tensor, cost_tensor, learn_rate, current_device):
        # Convert inputs to NumPy for SciPy, ensure they are on CPU
        last_strategy_np = last_strategy_tensor.detach().cpu().numpy().flatten()
        cost_np = cost_tensor.detach().cpu().numpy().flatten()

        # Objective function for SciPy - must take NumPy array and return scalar
        def scipy_obj_func(strategy_np):
            strategy_t = torch.from_numpy(strategy_np).to(dtype=torch.float32, device=current_device)
            last_strategy_t = torch.from_numpy(last_strategy_np).to(dtype=torch.float32, device=current_device)
            cost_t = torch.from_numpy(cost_np).to(dtype=torch.float32, device=current_device)
            # Ensure tensors are 1D for dot product
            return congestion_game.object_torch(strategy_t.squeeze(), last_strategy_t.squeeze(), cost_t.squeeze(), learn_rate).item()

        x0_np = np.full(len(last_strategy_np), 1.0 / len(last_strategy_np))

        bounds_np = [(0, 1) for _ in range(len(last_strategy_np))]
        constraints_np = [{'type': 'eq', 'fun': congestion_game.constraint_numpy}]

        sol = minimize(fun=scipy_obj_func, x0=x0_np, method='SLSQP',
                       bounds=bounds_np, constraints=constraints_np, tol=1e-6) # Added tol for robustness

        if sol.success:
            # Normalize to ensure it sums to 1 due to potential floating point inaccuracies
            res_np = sol.x / np.sum(sol.x)
            return torch.from_numpy(res_np).to(dtype=torch.float32, device=current_device)
        else:
            # print(f"Minimization failed: {sol.message}. Returning last strategy.")
            # Fallback or error handling
            return last_strategy_tensor # Return the original tensor if optimization fails

    def update_strategy(self, times, learn_rate, scale): # scale seems unused
        for i in range(self.player_num):
            current_prob = self.players_strategy[i].probability
            # Ensure path_cost is on the same device as probabilities
            new_prob = congestion_game.refresh_strategy_minimize(
                current_prob,
                self.path_cost.to(current_prob.device), # Ensure device consistency
                learn_rate,
                current_device=self.device
            )
            self.players_strategy[i].probability = new_prob

    def update_estimate_strategy(self, times, learn_rate, scale): # scale seems unused
        for i in range(self.player_num):
            current_est_prob = self.players_strategy[i].estimate_probability # Corrected attribute
            new_est_prob = congestion_game.refresh_strategy_minimize(
                current_est_prob, # Use estimate_probability here
                self.path_cost.to(current_est_prob.device), # Ensure device consistency
                learn_rate,
                current_device=self.device
            )
            self.players_strategy[i].estimate_probability = new_est_prob

    def get_key(self, val, total_path_select_dict):
        for key, value_list in total_path_select_dict.items():
            if val in value_list:
                return key
        return None # Should not happen if val is always a player index present

    def hindsight(self):
        self.hindsight_real_diff = 0.0 # Ensure it's a float
        
        # path_cost should be a tensor on self.device
        current_path_costs_tensor = self.path_cost

        for player_idx in range(self.player_num):
            real_path_idx = self.get_key(player_idx, self.total_path_select)
            if real_path_idx is None: continue # Should not happen

            real_cost = current_path_costs_tensor[real_path_idx]

            min_hindsight_cost = torch.tensor(float('inf'), device=self.device)

            # Create a temporary path counts tensor for this player's hindsight calculation
            temp_path_counts = torch.zeros(self.path_num, device=self.device, dtype=torch.float32)
            for p_idx, drivers in self.total_path_select.items():
                temp_path_counts[p_idx] = len(drivers)
            
            # Simulate removing this player from their actual path
            temp_path_counts[real_path_idx] -= 1

            for h_path_idx in range(self.path_num):
                # Cost if this player chose h_path_idx instead
                num_drivers_on_h_path = temp_path_counts[h_path_idx] + 1
                h_cost = self.get_path_cost_torch(h_path_idx, num_drivers_on_h_path)
                if h_cost < min_hindsight_cost:
                    min_hindsight_cost = h_cost
            
            self.hindsight_real_diff += (real_cost - min_hindsight_cost).item() # .item() to get Python float

    def potential_function(self):
        potential_value_tensor = torch.tensor(0.0, device=self.device, dtype=torch.float32)

        path_counts = torch.zeros(self.path_num, device=self.device, dtype=torch.int)
        for path_idx, drivers in self.total_path_select.items():
            path_counts[path_idx] = len(drivers)

        for path_idx in range(self.path_num):
            num_drivers_on_path = path_counts[path_idx]
            # Sum of costs from 1 to num_drivers_on_path (inclusive)
            # Path cost function expects a number (or tensor of numbers) of drivers
            for k_drivers in range(1, num_drivers_on_path.item() + 1): # k_drivers is int
                potential_value_tensor += self.get_path_cost_torch(path_idx, k_drivers)
        return potential_value_tensor.item() # Return Python float

    def play_a_game(self, T, gradient_times, learn_rate, scale):
        # For storing cumulative sums for averages
        cumulative_hindsight_diff = 0.0
        cumulative_potential_value = 0.0

        # For storing per-iteration values if needed for plotting raw data
        # self.raw_hindsight_diffs = []
        # self.raw_potential_values = []

        for t_round in range(1, T + 1):
            print(f"T : {t_round}")

            self.update_estimate_strategy(gradient_times, learn_rate, scale)
            self.random_select_cost() # This updates self.path_cost (tensor)
            self.update_strategy(gradient_times, learn_rate, scale)
            
            self.hindsight() # This updates self.hindsight_real_diff (float)
            # self.raw_hindsight_diffs.append(self.hindsight_real_diff)
            cumulative_hindsight_diff += self.hindsight_real_diff
            self.average_regret.append(cumulative_hindsight_diff / t_round)
            
            current_potential = self.potential_function() # Returns float
            # self.raw_potential_values.append(current_potential)
            cumulative_potential_value += current_potential
            self.potential_value.append(cumulative_potential_value / t_round)


