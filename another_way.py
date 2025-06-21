import torch
import numpy as np # For scipy minimize and potentially poly1d if not fully replaced
import select_path # Base class, should now be PyTorch-based
from scipy.optimize import minimize
# from env import device # Or get it from a central config / parent class

class congestion_game(select_path.congestion_game):
    def __init__(self, coefficient, path_num, player_num, device_to_use=None):
        # Pass device_to_use to the parent constructor
        super().__init__(coefficient, path_num, player_num, device_to_use=device_to_use)
        # self.device is inherited from select_path.congestion_game and set there
        self.social_cost_plt = []
        
        # Coefficients for h_cost, assuming path_num corresponds to their length
        # These are specific to this problem's h_cost definition.
        # It's better to derive these from the cost function coefficients if they are related
        # or pass them explicitly if they are independent.
        # For now, hardcoding based on the original h_cost structure for 4 paths:
        if path_num == 4: # Example, adjust if path_num can vary and h_cost structure changes
            self.h_cost_multipliers = torch.tensor([2, 2, 2, 2], dtype=torch.float32, device=self.device)
            # Original h_cost had: cost[0]*2-2, cost[1]*2-1, cost[2]*2-4, cost[3]*2-0
            # This implies specific constants related to each path's original cost function's constant term (c0).
            # If self.cost_func_coeffs stores [c1, c0] (linear: c1*x + c0)
            # then h_cost was like: path_cost * 2 - (original_c0_for_that_path * some_factor_or_constant)
            # This needs clarification or making it more general.
            # For now, I'll use the original constant subtractions directly.
            # These should match the order of paths.
            self.h_cost_const_subtract = torch.tensor([2, 1, 4, 0], dtype=torch.float32, device=self.device)
        else:
            # Default or error if path_num is not what h_cost expects
            print(f"Warning: h_cost is hardcoded for 4 paths. Received path_num={path_num}. Using placeholder constants.")
            self.h_cost_multipliers = torch.ones(path_num, dtype=torch.float32, device=self.device) * 2
            self.h_cost_const_subtract = torch.zeros(path_num, dtype=torch.float32, device=self.device)


    def h_cost_torch(self, cost_tensor):
        # cost_tensor is expected to be a 1D tensor of path costs
        # Ensure it's on the same device
        cost_tensor_dev = cost_tensor.to(self.device)
        if len(cost_tensor_dev) != len(self.h_cost_multipliers):
             raise ValueError(f"Length of cost_tensor ({len(cost_tensor_dev)}) does not match h_cost parameters ({len(self.h_cost_multipliers)}).")
        return cost_tensor_dev * self.h_cost_multipliers - self.h_cost_const_subtract

    @staticmethod
    def object_another_torch(strategy_tensor, last_strategy_tensor, cost_tensor, learn_rate, h_cost_func_torch):
        # strategy_tensor, last_strategy_tensor, cost_tensor are 1D tensors
        # h_cost_func_torch is a callable that computes h_costs from costs
        h_costs = h_cost_func_torch(cost_tensor) # This should return a tensor
        term1 = learn_rate * torch.dot(h_costs, strategy_tensor)
        diff_strategy = strategy_tensor - last_strategy_tensor
        term2 = torch.dot(diff_strategy, diff_strategy)
        return term1 + term2

    # This method overrides the static method in the parent.
    # To make it truly static and usable by scipy.minimize, we need to handle 'self' or pass h_cost_func explicitly
    # Or, make the scipy_obj_func a closure over 'self' if 'h_cost_torch' instance method is used.
    @staticmethod
    def refresh_strategy_minimize_another(last_strategy_tensor, cost_tensor, learn_rate, current_device, h_cost_func_torch_static_ref):
        last_strategy_np = last_strategy_tensor.detach().cpu().numpy().flatten()
        cost_np = cost_tensor.detach().cpu().numpy().flatten()

        def scipy_obj_func_another(strategy_np):
            strategy_t = torch.from_numpy(strategy_np).to(dtype=torch.float32, device=current_device)
            last_strategy_t = torch.from_numpy(last_strategy_np).to(dtype=torch.float32, device=current_device)
            cost_t = torch.from_numpy(cost_np).to(dtype=torch.float32, device=current_device)
            
            # Call the static object_another_torch, passing the h_cost_func reference
            return congestion_game.object_another_torch(strategy_t.squeeze(),
                                                        last_strategy_t.squeeze(),
                                                        cost_t.squeeze(),
                                                        learn_rate,
                                                        h_cost_func_torch_static_ref).item()

        x0_np = np.full(len(last_strategy_np), 1.0 / len(last_strategy_np))
        bounds_np = [(0, 1) for _ in range(len(last_strategy_np))]
        # Constraint function can be inherited or redefined if different; using parent's for now
        constraints_np = [{'type': 'eq', 'fun': select_path.congestion_game.constraint_numpy}]

        sol = minimize(fun=scipy_obj_func_another, x0=x0_np, method='SLSQP',
                       bounds=bounds_np, constraints=constraints_np, tol=1e-6)

        if sol.success:
            res_np = sol.x / np.sum(sol.x) # Normalize
            return torch.from_numpy(res_np).to(dtype=torch.float32, device=current_device)
        else:
            # print(f"Minimization failed in 'another_way': {sol.message}. Returning last strategy.")
            return last_strategy_tensor

    def update_strategy(self, times, learn_rate, scale): # scale seems unused
        for i in range(self.player_num):
            current_prob = self.players_strategy[i].probability
            # We need to pass a reference to a function that can compute h_cost.
            # If h_cost_torch is an instance method, we can create a lambda or partial.
            # For the static refresh_strategy_minimize_another, it needs a static/global h_cost_func.
            # Let's assume self.h_cost_torch is suitable to be passed (it takes cost_tensor and returns h_cost_tensor)
            
            # This is tricky because refresh_strategy_minimize_another is static.
            # One way is to make h_cost_torch static if it doesn't depend on instance state other than device (which can be passed)
            # Or, the objective function passed to scipy needs to be a closure.
            # For simplicity, let's assume refresh_strategy_minimize_another can take self.h_cost_torch
            
            new_prob = congestion_game.refresh_strategy_minimize_another(
                current_prob,
                self.path_cost.to(current_prob.device),
                learn_rate,
                current_device=self.device,
                h_cost_func_torch_static_ref=self.h_cost_torch # Pass instance method
            )
            self.players_strategy[i].probability = new_prob

    def update_estimate_strategy(self, times, learn_rate, scale): # scale seems unused
        for i in range(self.player_num):
            current_est_prob = self.players_strategy[i].estimate_probability
            new_est_prob = congestion_game.refresh_strategy_minimize_another(
                current_est_prob,
                self.path_cost.to(current_est_prob.device),
                learn_rate,
                current_device=self.device,
                h_cost_func_torch_static_ref=self.h_cost_torch # Pass instance method
            )
            self.players_strategy[i].estimate_probability = new_est_prob

    def social_cost(self):
        total_cost_tensor = torch.tensor(0.0, device=self.device, dtype=torch.float32)

        path_counts = torch.zeros(self.path_num, device=self.device, dtype=torch.int)
        for path_idx, drivers in self.total_path_select.items():
            path_counts[path_idx] = len(drivers)

        for path_idx in range(self.path_num):
            num_drivers_on_path = path_counts[path_idx]
            if num_drivers_on_path.item() > 0:
                # Cost for this path given num_drivers_on_path
                # self.get_path_cost_torch is inherited from parent
                cost_for_path = self.get_path_cost_torch(path_idx, num_drivers_on_path)
                total_cost_tensor += cost_for_path * num_drivers_on_path.float() # Cost * number of drivers on that path

        return total_cost_tensor.item() # Return Python float

    def play_a_game(self, T, gradient_times, learn_rate, scale):
        # hindsight_real_diff_cumulative = 0.0 # For average_regret, seems to be re-purposed for social cost in this version
        potential_value_cumulative = 0.0
        social_cost_cumulative = 0.0 # Renamed sc to be more descriptive

        # self.average_regret = [] # Inherited, but seems to store cumulative social cost / t_round here
        # self.potential_value = [] # Inherited

        for t_round in range(1, T + 1):
            print(f"T : {t_round}")

            self.update_estimate_strategy(gradient_times, learn_rate, scale)
            self.random_select_cost() # Updates self.path_cost
            self.update_strategy(gradient_times, learn_rate, scale)

            # self.hindsight() # Original hindsight is called, but its result isn't directly used for social_cost_plt
                            # The inherited self.average_regret list will be populated by parent's play_a_game if called via super,
                            # or by self.hindsight() if we want to keep that metric too.
                            # The current code for another_way.play_a_game OVERRIDES parent's play_a_game.
                            # It calculates social cost and stores its average in self.social_cost_plt.
                            # It also calculates something and stores it in self.average_regret.
                            # The original code had:
                            # self.hindsight()
                            # sc+=self.social_cost()
                            # temp_sc=sc/i
                            # self.social_cost_plt.append(temp_sc)
                            # hindsight_real_diff.append(sc) <--- This is confusing. It appends cumulative social cost to a local list.
                            # self.average_regret.append(sum(hindsight_real_diff)/i) <--- This becomes average of cumulative social costs.

            current_social_cost = self.social_cost() # Returns float
            social_cost_cumulative += current_social_cost
            self.social_cost_plt.append(social_cost_cumulative / t_round)

            # To match the original logic for `self.average_regret` in this specific `play_a_game` version:
            # The original `hindsight_real_diff` list here was accumulating the `sc` (cumulative social_cost).
            # This seems like a misnomer or a different metric.
            # If we want to keep the same behavior for `self.average_regret` as in the original `another_way.py`:
            # We need a list to store the `social_cost_cumulative` at each step `i`.
            if not hasattr(self, '_temp_cumulative_social_costs_for_avg_regret'):
                self._temp_cumulative_social_costs_for_avg_regret = []
            self._temp_cumulative_social_costs_for_avg_regret.append(social_cost_cumulative)
            
            # Calculate sum of (social_cost_cumulative_at_step_1, social_cost_cumulative_at_step_2, ..., social_cost_cumulative_at_step_t_round) / t_round
            avg_of_cumulative_sc = sum(self._temp_cumulative_social_costs_for_avg_regret) / t_round
            self.average_regret.append(avg_of_cumulative_sc)


            current_potential = self.potential_function() # Inherited, returns float
            potential_value_cumulative += current_potential
            self.potential_value.append(potential_value_cumulative / t_round)

        # Clean up temporary list if created
        if hasattr(self, '_temp_cumulative_social_costs_for_avg_regret'):
            del self._temp_cumulative_social_costs_for_avg_regret



