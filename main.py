import matplotlib.pyplot as plt
 

import select_path

def valution():
        
        coefficient =[[3,2], [4,1],[2,4],[6,0]]
        player_number = 100
        path_number = len(coefficient)
        game =  select_path. congestion_game(coefficient, path_number, player_number)
        

        gradient_times = 10 
        learn_rate = 0.0001
        T = 10 
        scale = 1
        game.  play_a_game(T,gradient_times, learn_rate, scale)
        
        diff_plot(T=T, real_diff=game.average_regret)

def diff_plot(T,real_diff ):        
        times=[i+1 for i in range(T)]
        plt.plot(times,real_diff,color=(255/255,100/255,100/255))
        plt.title("indicator") # title
        plt.ylabel("diff") # y label
        plt.xlabel("times") # x label
        plt.show()
if __name__ == '__main__' :
     valution()