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
          self.path_num = path_num
          self.player_num = player_num
          for i in range(player_num) : 
               self.players_strategy.append(player(path_num)) 
          self.players_strategy = np.asarray(self.players_strategy)

     def all_player_probability(self) : 
          for i in range(self.player_num) :
             print(i, self.players_strategy[i].get_probability())

 
