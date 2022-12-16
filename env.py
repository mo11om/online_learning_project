import numpy as np 
import random 

 
 

class player :
     

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

 
