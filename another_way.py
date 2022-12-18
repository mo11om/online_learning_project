import select_path
import numpy as np 
from scipy.optimize import minimize
class congestion_game(select_path.congestion_game):
    def __init__(self, coefficient, path_num, player_num):
        super().__init__(coefficient, path_num, player_num)
         
        self.social_cost_plt=[]
        
    def h_cost( cost):
        hcost=np.zeros(4)
        hcost[0]=cost[0]*2-2
        hcost[1]=cost[1]*2-1
        hcost[2]=cost[2]*2-4
        hcost[3]=cost[3]*2-0
         
        return hcost
 
    def object(strategy, last_strategy, cost, learn_rate) :
        return learn_rate*congestion_game.h_cost(cost).dot(strategy.T) + (strategy - last_strategy).dot((strategy - last_strategy).T)

    def refresh_strategy_minimize(last_strategy, cost, learn_rate) :
          x0 = np.full((1, len(last_strategy)), 1/len(last_strategy))
          b = (0, 1)
          buds = []
          for i in range(len(last_strategy)) :
               buds.append(b)
          cons = [{'type' : 'eq', 'fun' : congestion_game.constraint}]
          sol = minimize(fun=congestion_game.object, x0=x0, args=(np.array(last_strategy),
                         np.array(cost), learn_rate), method='SLSQP', bounds=buds,
                         constraints=cons)
          return sol.x

    def update_strategy(self, times, learn_rate, scale ) :
          for i in range(self.player_num) :
       

               self.players_strategy[i].probability =  congestion_game. refresh_strategy_minimize(
                   self.players_strategy[i].probability,
                   self.path_cost, 
                   learn_rate)

    def update_estimate_strategy(self, times, learn_rate, scale ) :
          for i in range(self.player_num) :
               

               self.players_strategy[i].estimate_probability =  congestion_game.refresh_strategy_minimize(
                   self.players_strategy[i].probability,
                   self.path_cost, 
                   learn_rate) 

    def social_cost(self) :
          total_cost = 0
          for path ,driver in self.total_path_select.items() :
               path_cost = self.cost_func[path](len(driver)) #calculate path cost
               total_cost+=path_cost*len(driver)
          return total_cost

    def play_a_game(self,T,gradient_times, learn_rate, scale):
        hindsight_real_diff = []
        p_value=[]
         
        sc=0
        for i in range(1, T+1) :
            print("T : ", i) 

            self.update_estimate_strategy(gradient_times, learn_rate, scale )
            self.random_select_cost()
            self.update_strategy(gradient_times, learn_rate, scale )
            self.hindsight()
            sc+=self.social_cost()
            temp_sc=sc/i
            self.social_cost_plt.append(temp_sc)



            hindsight_real_diff.append(sc)




            self.average_regret.append(sum(hindsight_real_diff)/i)#30rounds 1~30
            
            
            
            p_value.append( self.potential_function( self.total_path_select, self.cost_func))
            
            self.potential_value.append(sum(p_value)/i)#30rounds 1~30



