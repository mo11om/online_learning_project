import numpy as np 
import random 
import select_path

class player :
     def  create_random(self) : #romdom crate posssibility
          # print(self.path_num)
          tmp = np.zeros ((1,self.path_num-1))
          rdtmp = 0
          total_num = self.path_num-1
          while total_num :
               rdtmp = random.randint(1,100)    
               if(rdtmp  in tmp[0]) :
                    continue
               tmp[0][total_num-1] = rdtmp
               total_num = total_num-1
          tmp = np.append(tmp ,np.array( 100))
          tmp.sort()
          for i in range(self.path_num-1,0,-1) : 
               if i != 0:
                    tmp [i] = tmp [i]-tmp[i-1]            
          tmp = tmp/100
          return tmp

     def __init__(self, path_num) : 
          self.path_num = path_num
          self.probability = np.ones(path_num)/path_num
          #self.create_random()     
     def get_probability (self) : #[poss1 , poss2, poss3]
          return self.probability


class all_player :
     def __init__(self, player_num, path_num) :
          self.players_strategy = list()
          self.player_num = player_num
          for i in range(player_num) : 
               self.players_strategy .append(player(path_num)) 
          self.players_strategy = np.asarray(self.players_strategy)

     def all_player_probability(self) : 
          for i in range(self.player_num) :
             print(i,self.players_strategy[i].get_probability())


class congestion_game(all_player) :
     def __init__(self,coefficient,path_num,player_num) : 
          self.cost_func = list()
          self.path_num = path_num
          self.path_cost = np.zeros(path_num) 
          all_player.__init__(self, player_num = player_num, path_num = path_num)
          for i in coefficient :
               self.cost_func.append(np.poly1d(i))
     
     def get_cost_func (self) :
          return self.cost_func
     
     def random_select_cost(self) : 
          total_path_select = {new_list: [] for new_list in range(self.path_num)} #creat empty dict => {0:[], 1:[], 2:[]}
          for i in range (self.player_num) :
               choice_path = np.random.choice(a = self.path_num,size = 1,p = self.players_strategy[i].probability)
               total_path_select[choice_path[0]].append(i)
          for path ,driver in total_path_select.items() :
               path_cost = self.cost_func[path](len(driver)) #calculate path cost
               self.path_cost[path] = path_cost   
          print("paths cost : ", self.path_cost)

     def update_strategy(self, times, learn_rate) :
          for i in range(self.player_num) :
               self.players_strategy[i].probability = select_path.refresh_strategy(self.path_cost, self.players_strategy[i].probability, times, learn_rate)
               print("strategy of: ",i, self.players_strategy[i].probability)
          
if __name__ == '__main__' :
     coefficient =[[6,3,6],[3,7,2],[2,9,0], [4,6,5], [7,2,2], [5,8,0], [3,3,3]]
     player_number = 10
     path_number = 7
     gradient_times = 100
     learn_rate = 10
     T = 10
     game = congestion_game(coefficient, path_number, player_number)
     for i in range(0, T) :
          print("T = ",i)
          game.random_select_cost()
          game.update_strategy(gradient_times, learn_rate)



