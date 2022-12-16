
 

import select_path
import another_way
from plot import plot as plt

def valution(way:str,show:str):
        gradient_times = 10 
        learn_rate = 0.0001
        T = 10 
        scale = 1
        coefficient =[[3,2], [4,1],[2,4],[6,0]]
        player_number = 20
        path_number = len(coefficient)

       

        if  "h" in  way:

                game =  select_path. congestion_game(coefficient, path_number, player_number)
                

        
                game.  play_a_game(T,gradient_times, learn_rate, scale)

                if show == "b":
                
                        plt.plot_select_path(game.all_play_total_path_select)
               
        

                
                if show == "l":

                        plt.plot_diff(T=T, real_diff=game.average_regret,line_name="average_regret")
                        plt.plot_diff(T=T, real_diff=game.potential_value,line_name="potential_value")

                 
        
        if  "s" in way :

                game =  another_way. congestion_game(coefficient, path_number, player_number)
                

        
                game.  play_a_game(T,gradient_times, learn_rate, scale)

                
                if "b" in show:
                
                        plt.plot_select_path(game.all_play_total_path_select)
               
        

                
                if  "l" in show:
                
                        plt.plot_diff(T=T, real_diff=game.social_cost_plt,line_name="social cost")
                        plt.plot_diff(T , real_diff=game.potential_value,line_name="potential_value")

                


        
if __name__ == '__main__' :
        way = input( "hindcost h social cost s both  hs ")
        show = input( " bar  b  line  l both bl ")
        valution(way,show)
     