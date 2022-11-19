
 

import select_path
import another_way
from plot import plot as plt

def valution():
        gradient_times = 10 
        learn_rate = 0.0001
        T = 10 
        scale = 1
        coefficient =[[3,2], [4,1],[2,4],[6,0]]
        player_number = 10
        path_number = len(coefficient)


        game =  select_path. congestion_game(coefficient, path_number, player_number)
        

       
        game.  play_a_game(T,gradient_times, learn_rate, scale)

        #print(game.all_play_total_path_select)
        
         
        plt.plot_select_path(game.all_play_total_path_select)
        plt.show()
     

       
       
        plt.plot_diff(T=T, real_diff=game.average_regret)
        plt.plot_diff(T=T, real_diff=game.potential_value)

        plt.show()


        
if __name__ == '__main__' :
     valution()
     