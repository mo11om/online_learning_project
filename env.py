import numpy as np 
import random 
import select_path
import copy
 

class player :
     def  create_random(self) : #random crate propability
          # print(self.path_num)
          tmp = np.zeros ((1, self.path_num-1))
          rdtmp = 0
          total_num = self.path_num - 1
          while total_num :
               rdtmp = random.randint(1, 100)    
               if(rdtmp  in tmp[0]) :
                    continue
               tmp[0][total_num-1] = rdtmp
               total_num = total_num-1
          tmp = np.append(tmp ,np.array(100))
          tmp.sort()
          for i in range(self.path_num-1, 0, -1) : 
               if i != 0:
                    tmp [i] = tmp [i]-tmp[i-1]            
          tmp = tmp/100
          print(tmp)
          return tmp

     def __init__(self, path_num) : 
          self.path_num = path_num
          self.probability = np.ones(path_num)/path_num
          self.estimate_probability = np.ones(path_num)/path_num
          # self.probability = self.create_random()    
           
     def get_probability (self) : #[prob1 , prob2, prob3]
          return self.probability

class all_player :
     def __init__(self, player_num, path_num) :
          self.players_strategy = list()
          self.player_num = player_num
          for i in range(player_num) : 
               self.players_strategy.append(player(path_num)) 
          self.players_strategy = np.asarray(self.players_strategy)

     def all_player_probability(self) : 
          for i in range(self.player_num) :
             print(i, self.players_strategy[i].get_probability())

class congestion_game(all_player) :
     def __init__(self, coefficient, path_num, player_num) : 
          self.cost_func = list()
          self.path_num = path_num
          self.path_cost = np.zeros(path_num) 
          self.total_path_select = dict() #record all player's final choice
          
          all_player.__init__(self, player_num=player_num, path_num=path_num)
          for i in coefficient :
               self.cost_func.append(np.poly1d(i))
     
     def get_cost_func (self) :
          return self.cost_func
     
     def random_select_cost(self) : 
          self.total_path_select = {new_list: [] for new_list in range(self.path_num)} 
          print("init ",self.total_path_select)
          #creat empty dict => {0:[], 1:[], 2:[]}
          for i in range (self.player_num) :
               choice_path = np.random.choice(
                   a=self.path_num,
                   size=1,
                   p=self.players_strategy[i].estimate_probability)

               self.total_path_select[choice_path[0]].append(i)
          print("path distribution : ", self.total_path_select)
          for path ,driver in self.total_path_select.items() :
               path_cost = self.cost_func[path](len(driver)) #calculate path cost
               self.path_cost[path] = path_cost   
          print("path cost : ", self.path_cost)
          return self.path_cost

     def update_strategy(self, times, learn_rate, scale) :
          for i in range(self.player_num) :
               #different method to update player's strategy

               # self.players_strategy[i].probability = select_path.refresh_strategy(
               #   self.path_cost, 
               #   self.players_strategy[i].probability, 
               #   times, 
               #   learn_rate, 
               #   scale)

               self.players_strategy[i].probability = select_path.refresh_strategy_minimize(
                   self.players_strategy[i].probability,
                   self.path_cost, 
                   learn_rate)
          print("player strategy : ",  self.players_strategy[i].probability) 

     def update_estimate_strategy(self, times, learn_rate, scale) :
          for i in range(self.player_num) :
               #different method 

               # self.players_strategy[i].estimate_probability = select_path.refresh_strategy(
               #     self.path_cost,
               #     self.players_strategy[i].probability, 
               #     times, 
               #     learn_rate, 
               #     scale)

               self.players_strategy[i].estimate_probability = select_path.refresh_strategy_minimize(
                   self.players_strategy[i].probability,
                   self.path_cost, 
                   learn_rate)          
          print("player estimate strategy : ",  self.players_strategy[0].estimate_probability) 
     
     def hindsight(self) :
          hindsight_real_diff = 0
          for number in range(self.player_num) :
               real_path = select_path.get_key(number, self.total_path_select) #本回合實際的路徑
               real_cost = self.path_cost[real_path]                           #本回合實際的cost
                                                    
               hindsight_cost = 100000000000000000                             #後見之明最低cost
               exclude_path_select = copy.deepcopy(self.total_path_select)
               exclude_path_select[real_path].remove(number)
               for path ,driver in exclude_path_select.items() :
                    path_cost = self.cost_func[path](len(driver)+1) #calculate path cost
                    if path_cost < hindsight_cost :
                         hindsight_cost = path_cost
                       
               hindsight_real_diff = hindsight_real_diff + (real_cost - hindsight_cost) 
               #所有人的[真實選擇與後見之明的差異]的總和
          return hindsight_real_diff           

if __name__ == '__main__' :
      pass