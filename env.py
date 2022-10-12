import numpy as np 
import random 
import select_path

class player :
     
          # create player  possibility martrix according  num of path
          # default possibility of every road is 1/pathnum eg..[1/3,1/3,1/3] for path is 3

     def  create_random(self) : #romdom crate posssibility
          tmp = np.zeros ((1,self.path_num-1))
          rdtmp = 0
          total_num = self.path_num-1
          while total_num :
               rdtmp = random.randint(1,100)    
               if(rdtmp  in tmp[0]) :
                    continue
               tmp[0][total_num-1] = rdtmp
               total_num = total_num-1
          tmp = np.append(tmp ,np.array(100))
          tmp.sort()
          for i in range(self.path_num-1,0,-1) : 
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
     # def get_probability (self) : #[poss1 , poss2, poss3]
     #      return self.probability


class all_player ():
     
     #all player get into a np_array 



     def __init__(self, player_num, path_num) :
          
          self.players_strategy = list()
          # self.players_estimate = list()
          self.player_num = player_num
          for i in range(player_num) : 
               self.players_strategy .append(player(path_num)) 
          self.players_strategy = np.asarray(self.players_strategy)

     # def all_player_probability(self) : 
     #      for i in range(self.player_num) :
     #         print(i,self.players_strategy[i].get_probability())


class congestion_game(all_player) :
     #selcet path according path possibility for everyone
     #  


     def __init__(self,coefficient,path_num,player_num) : 
          self.cost_func = list()
          self.path_num = path_num
          self.path_cost = np.zeros(path_num) 
          all_player.__init__(self, player_num = player_num, path_num = path_num)
          for i in coefficient :
               self.cost_func.append(np.poly1d(i))
     
     # def get_cost_func (self) :
     #      return self.cost_func
     
     def random_select_cost(self) : 
          total_path_select = {new_list: [] for new_list in range(self.path_num)} #creat empty dict => {0:[], 1:[], 2:[]}
          for i in range (self.player_num) :
               choice_path = np.random.choice(a = self.path_num,size = 1,p = self.players_strategy[i].estimate_probability)
               total_path_select[choice_path[0]].append(i)
          print("path distribution : ", total_path_select)
          for path ,driver in total_path_select.items() :
               path_cost = self.cost_func[path](len(driver)) #calculate path cost
               self.path_cost[path] = path_cost   
          print("path cost : ", self.path_cost)
          return self.path_cost

     def update_strategy(self, times, learn_rate, scale) :
          for i in range(self.player_num) :
               # print("check", self.players_strategy[i].probability)
               self.players_strategy[i].probability = select_path.refresh_strategy(self.path_cost, self.players_strategy[i].probability, times, learn_rate, scale)
               print("player ", i, " strategy : ",  self.players_strategy[i].probability)

     def update_estimate_strategy(self, times, learn_rate, scale) :
          for i in range(self.player_num) :
               self.players_strategy[i].estimate_probability = select_path.refresh_strategy(self.path_cost, self.players_strategy[i].probability, times, learn_rate, scale)          
               print("player ", i, " estimate strategy : ",  self.players_strategy[i].estimate_probability) 



if __name__ == '__main__' :
     coefficient =[[2.2,3], [1,0.3],  [0.6,5], [3,2]]
     player_number = 6
     path_number = 4
     gradient_times = 100
     learn_rate = 3
     T = 50
     scale = 30
     
     game = congestion_game(coefficient, path_number, player_number)
     for i in range(0, T) :
          print("T = ",i)
          game.update_estimate_strategy(gradient_times, learn_rate, scale)
          game.random_select_cost()
          game.update_strategy(gradient_times, learn_rate, scale)


