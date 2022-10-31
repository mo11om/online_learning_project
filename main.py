import matplotlib.pyplot as plt
 
import env
def valution():
        coefficient =[[3,2], [4,1],[2,4],[6,0]]
        player_number = 100
        path_number = len(coefficient)
        gradient_times = 100
        learn_rate = 10
        T = 20
        scale = 1
        hindsight_real_diff = []
        everage_regret = []
        potential_value = []
        game = env. congestion_game(coefficient, path_number, player_number)
        for i in range(1, T+1) :
            print("T : ", i) 

            game.update_estimate_strategy(gradient_times, learn_rate, scale)
            game.random_select_cost()
            game.update_strategy(gradient_times, learn_rate, scale)
            hight = game.hindsight()
            hindsight_real_diff.append(hight)
            everage_regret.append(sum(hindsight_real_diff)/i)#30rounds 1~30
            # potential_value.append()##
        # print(hindsight_real_diff)
        print(everage_regret)
        # print(select_path.potential_function())
        times=[i+1 for i in range(T)]
        plt.plot(times,hindsight_real_diff,color=(255/255,100/255,100/255))
        plt.title("indicator") # title
        plt.ylabel("diff") # y label
        plt.xlabel("times") # x label
        plt.show()
if __name__ == '__main__' :
     valution()