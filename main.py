import torch # Import PyTorch
import select_path
import another_way
from plot import plot as plt
import env # To set the global device if that's the chosen mechanism

def valution(way:str, show:str, T=100, player_number=50, use_cuda_if_available=True):
    # Determine and set the device for PyTorch operations
    if use_cuda_if_available and torch.cuda.is_available():
        current_device = torch.device("cuda")
        print("CUDA is available. Using GPU.")
    else:
        current_device = torch.device("cpu")
        print("CUDA not available or not selected. Using CPU.")

    # Set the device globally in the env module (if this pattern is used)
    # This assumes env.py has a set_global_device function or similar.
    if hasattr(env, 'set_global_device'):
        env.set_global_device(current_device)
    else: # Fallback if env.py's device is module-level global directly (less flexible)
        env.device = current_device


    gradient_times = 10
    learn_rate = 0.0001
    scale = 1 # This parameter seems unused in the core logic of play_a_game

    # Coefficients for polynomial cost functions (e.g., [[c1, c0], ...])
    # For ax^2 + bx + c, it would be [a, b, c]. Original code implies ax+b, so [a,b]
    coefficient =[[3,2], [4,1],[2,4],[6,0]] # Example: path0_cost = 3*x + 2
    path_number = len(coefficient)

    game = None # Initialize game variable

    if "h" in way:
        print(f"\nRunning Hindsight-based game with device: {current_device}")
        # Pass the selected device to the game constructor
        game = select_path.congestion_game(coefficient, path_number, player_number, device_to_use=current_device)
        game.play_a_game(T, gradient_times, learn_rate, scale)

        if "b" in show:
            print("Plotting path selections for Hindsight game...")
            plt.plot_select_path(game.all_play_total_path_select) # Data should be CPU-based for plotting
        
        if "l" in show:
            print("Plotting line graphs for Hindsight game...")
            # Ensure data passed to plot is suitable (e.g. Python lists of numbers)
            plt.plot_diff(T=T, real_diff=game.average_regret, line_name="average_regret")
            plt.plot_diff(T=T, real_diff=game.potential_value, line_name="potential_value")

    if "s" in way:
        print(f"\nRunning Social Cost-based game (another_way) with device: {current_device}")
        # Pass the selected device to the game constructor
        game = another_way.congestion_game(coefficient, path_number, player_number, device_to_use=current_device)
        game.play_a_game(T, gradient_times, learn_rate, scale)

        if "b" in show:
            print("Plotting path selections for Social Cost game...")
            plt.plot_select_path(game.all_play_total_path_select) # Data should be CPU-based for plotting

        if "l" in show:
            print("Plotting line graphs for Social Cost game...")
            plt.plot_diff(T=T, real_diff=game.social_cost_plt, line_name="social_cost")
            plt.plot_diff(T=T, real_diff=game.potential_value, line_name="potential_value")
        
if __name__ == '__main__':
    arg = []
    try:
        with open("setting.txt", "r") as file: # Use with statement for file handling
            arg = [line.strip() for line in file.readlines()] # strip newlines
    except FileNotFoundError:
        print("Error: setting.txt not found. Using default values.")
        # Default values if file not found or parsing fails
        arg = ["hs", "bl", "100", "50"] # Default: run both, show both, T=100, players=50
    except Exception as e:
        print(f"Error reading or parsing setting.txt: {e}. Using default values.")
        arg = ["hs", "bl", "100", "50"]

    if len(arg) < 4:
        print("Warning: Not enough settings in setting.txt. Using some defaults.")
        # Pad with defaults if file is incomplete
        default_settings = ["hs", "bl", "100", "50"]
        for i in range(len(arg), 4):
            arg.append(default_settings[i])

    parsed_way = arg[0]
    parsed_show = arg[1]
    try:
        parsed_T = int(arg[2])
        parsed_players = int(arg[3])
    except ValueError:
        print("Error: Could not parse T or player number from settings. Using defaults T=100, players=50.")
        parsed_T = 100
        parsed_players = 50

    # print(f"Settings loaded: way='{parsed_way}', show='{parsed_show}', T={parsed_T}, players={parsed_players}")
    # print(f"Plot line graph for T? {'l' in parsed_show}") # Example of using parsed setting

    # Add a simple command line argument or setting to control CUDA usage for easier testing
    # For now, it's hardcoded to True, meaning it will use CUDA if available.
    valution(way=parsed_way, show=parsed_show, T=parsed_T, player_number=parsed_players, use_cuda_if_available=True)