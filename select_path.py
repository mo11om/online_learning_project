import numpy as np

import env

import copy 
from scipy.optimize import minimize

 
 
# def panning(strategy, scale) : #strategy must be a np.array!!
#     sum_ = 0
#     sum_ = sum(strategy)
#     range_ = scale - sum_/len(strategy)
#     strategy = strategy + range_
#     positive_sum = sum([i for i in strategy if i > 0])
#     positive_number = len([i for i in strategy if i > 0])
#     while  abs(positive_sum - scale) > 0.01  :
#         range_ = (scale - positive_sum)/positive_number
#         strategy = strategy + range_
#         positive_sum = sum([i for i in strategy if i > 0])
#         positive_number = len([i for i in strategy if i > 0])
#     strategy[strategy < 0] = 0
#     strategy = strategy/scale
#     return strategy 
    
# def  refresh_strategy(past_cost, past_strategy, times, learn_rate, scale) :
#     strategy = np.zeros(len(past_strategy))
#     gradient = np.zeros(len(past_strategy))
#     for i in range(times): #moving times 
#         gradient = past_cost + (2/learn_rate)*(strategy - past_strategy)
#         strategy = strategy - gradient
#     new_strategy = panning(strategy, scale) 
#     return new_strategy




class congestion_game(env.all_player) :
     def __init__(self, coefficient, path_num, player_num) : 
          self.cost_func = list()
          self.path_cost = np.zeros(path_num) 
          self.total_path_select = dict() #record all player's final choice for each round
          self.hindsight_real_diff = 0
          self.average_regret = []
          self.potential_value = []
          self.all_play_total_path_select=[]
          super() .__init__( player_num=player_num, path_num=path_num) 
          for i in coefficient :
               self.cost_func.append(np.poly1d(i))
     



     def get_cost_func (self) :
          return self.cost_func
     
     
     def random_select_cost(self) : 
          self.total_path_select = {new_list: [] for new_list in range(self.path_num)} 
          #creat empty dict => {0:[], 1:[], 2:[]}
          for i in range (self.player_num) :
               choice_path = np.random.choice(
                   a=self.path_num,
                   size=1,
                   p=self.players_strategy[i].estimate_probability)

               self.total_path_select[choice_path[0]].append(i)

          # print("path distribution : ", self.total_path_select)
          #print (self.total_path_select)
          path_sum={}# [0:5,1:5]
           
               

          for path ,driver in self.total_path_select.items() :
               path_sum[path]=(len(driver))
               path_cost = self.cost_func[path](len(driver)) #calculate path cost
               self.path_cost[path] = path_cost   

          # print("path cost : ", self.path_cost)
          self.all_play_total_path_select.append(path_sum)
          return self.path_cost
     def object(strategy, last_strategy, cost, learn_rate) :
          return cost.dot(strategy.T) + (1/learn_rate)*(strategy - last_strategy).dot((strategy - last_strategy).T)
 

     def constraint(strategy) :
          return np.sum(strategy)- 1

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
          # print("player estimate strategy : ",  self.players_strategy[0].estimate_probability) 
     def get_key(self,val, total_path_select):
        for key, value in total_path_select.items():
            if val in value:
                return key
     def hindsight(self) :
          self.hindsight_real_diff = 0
          for number in range(self.player_num) :
               real_path = self.get_key(number, self.total_path_select) #本回合實際的路徑
               real_cost = self.path_cost[real_path]                           #本回合實際的cost
                                                    
               hindsight_cost = 100000000000000000                             #後見之明最低cost
               exclude_path_select = copy.deepcopy(self.total_path_select)
               exclude_path_select[real_path].remove(number)
               for path ,driver in exclude_path_select.items() :
                    path_cost = self.cost_func[path](len(driver)+1) #calculate path cost
                    if path_cost < hindsight_cost :
                         hindsight_cost = path_cost
                       
               self.hindsight_real_diff = self.hindsight_real_diff + (real_cost - hindsight_cost) 
            
               #所有人的[真實選擇與後見之明的差異]的總和

     def potential_function(self ) : #cost_func is a set of poly1d
        potential_value=0
        for path, driver in self.total_path_select.items() :
            for i in range(0, len(driver)+1) :
                potential_value = potential_value + self.cost_func[path](i)
        return potential_value   


     def play_a_game(self,T,gradient_times, learn_rate, scale):
        hindsight_real_diff = []
        p_value=[]
        
        for i in range(1, T+1) :
            print("T : ", i) 

            self.update_estimate_strategy(gradient_times, learn_rate, scale )
            self.random_select_cost()
            self.update_strategy(gradient_times, learn_rate, scale )
            self.hindsight()
            hindsight_real_diff.append(self.hindsight_real_diff)

            self.average_regret.append(sum(hindsight_real_diff)/i)#30rounds 1~30
            
            
            
            p_value.append( self.potential_function())
            
            self.potential_value.append(sum(p_value)/i)#30rounds 1~30


