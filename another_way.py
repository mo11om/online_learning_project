import select_path
import numpy as np 

class congestion_game(select_path.congestion_game):
    def __init__(self, coefficient, path_num, player_num):
        super().__init__(coefficient, path_num, player_num)
        self.hcost=np.zeros(path_num)
        self.social_cost_plt=[]
    def h_cost(self,cost):
        self.hcost[0]=cost[0]*2-2
        self.hcost[1]=cost[1]*2-1
        self.hcost[2]=cost[2]*2-4
        self.hcost[3]=cost[3]*2-0

    def object(strategy, last_strategy, cost, learn_rate) :
        return cost.dot(strategy.T) + (1/learn_rate)*(strategy - last_strategy).dot((strategy - last_strategy).T)

    def social_cost(self) :
          total_cost = 0
          for path ,driver in self.total_path_select.items() :
               path_cost = self.cost_func[path](len(driver)) #calculate path cost
               total_cost+=path_cost*len(driver)
          return total_cost
    def play_a_game(self,T,gradient_times, learn_rate, scale):
        hindsight_real_diff = []
        p_value=[]
        social_cost_plt = []
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



