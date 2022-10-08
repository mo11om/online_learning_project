import numpy as np 
import random 
import select_path

class player :
     def  create_random(self):#romdom crate posssibility
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

     def __init__(self,path_num) : 
          self.path_num = path_num
          self.possibility = np.ones(path_num)/path_num
          #self.create_random()     
     def get_possibility (self) : #[poss1 , poss2, poss3]
          return self.possibility

class all_player :
     def __init__(self,player_num,path_num) :
          self.player_list = list()
          self.player_num = player_num
          for i in range(player_num) : 
               self.player_list .append(player(path_num)) 
          self.player_list = np.asarray(self.player_list)

     def all_player_possibility(self) : #naming it "all_player_possibility" is batter
          for i in range(self.player_num) :
             print(i,self.player_list[i].get_possibility() )



          
class path_cost_function(all_player) :
     def __init__(self,coefficient,path_num,player_num) :  #changing "cost_value" to "coefficient" is better
          self.cost_func = list()
          self.path_num = path_num
          self.path_cost = np.zeros(path_num) 
          all_player.__init__(self,player_num=player_num,path_num=path_num)
          #the function of this array is to record all path cost instead of each player's cost
          #(because our setting is full information, all players share the exaclty same cost information no matter which path each of they selects)
          # therefore, changing name from "player_cost" to "path_cost" and parameter from "player_num" to "path_num" is better
          for i in coefficient :
               self.cost_func.append(np.poly1d(i))
     
     def get_cost_func (self) :
          return self.cost_func
     
     def random_select_cost(self ) : 
          total_path_select = {new_list: [] for new_list in range(self.path_num)} #creat empty dict => {0:[], 1:[], 2:[]}
          for i in range (self.player_num) :
               choice_path = np.random.choice(a = self.path_num,size = 1,p = self.player_list[i].possibility)
               total_path_select[choice_path[0]].append(i)
          # print(total_path_select)
          for key ,value in total_path_select.items() :
               path_cost = self.cost_func[key](len(value)) #calculate path cost
               self.path_cost[key] = path_cost    #change   





if __name__ == '__main__' :
     coefficient =[[2,3],[3,2],[4,0]]
     player_number = 6
     path_number = 3
     #_all_palyer = all_player(player_number, path_number)
     # a = all_player.all_player_possibility(_all_palyer)
     
     path_cost = path_cost_function(coefficient, path_number, player_number)
     path_cost.random_select_cost( )
     path_cost.all_player_possibility()

     print(path_cost.path_cost)



