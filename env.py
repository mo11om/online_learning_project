 


 
 
 
import numpy as np
 
import random 

class player :
     def  create_random(self):#romdom crate posssibility
          # print(self.path_num)
          
          tmp = np.zeros ((1,self.path_num-1))

    
          rdtmp =0
          total_num=self.path_num-1
          while total_num:
              
               
               rdtmp =      random.randint(1,100)    
               if(rdtmp  in tmp[0]):
                    continue
               tmp[0][total_num-1]= rdtmp
                    
               total_num=total_num-1
               
          tmp=np.append(tmp ,np.array( 100))
          tmp.sort()
          
          for i in range(self.path_num-1,0,-1):
                
               if i!=0:
                    tmp [i]= tmp [i]-tmp[i-1]
               
          tmp=tmp/100
           
          return tmp
     def __init__(self,path_num) :
          self.path_num=path_num

          self.possibility = np.ones(path_num)
          self.possibility=self.possibility/path_num
          #self.create_random()     
     def get_possibility (self):#[poss1 , poss2, poss3]
          return self.possibility

class all_player :
     def __init__(self,player_num,path_num):
          self.player_list=list()
          self.player_num = player_num
          for i in range(player_num):
               self.player_list .append(player(path_num)) 
          self.player_list=np.asarray(self.player_list)

     def player_print (self):
           
          for i in range(self.player_num):
             print(i,self.player_list[i].get_possibility() )



          
class path_cost_function:
     def __init__(self,cost_value,path_num,player_num ):     
          self.cost_func=list()
          self.path_num=path_num
          self.player_cost=np.zeros(player_num)
          for i in cost_value:
               self.cost_func.append(np.poly1d(i))
     def get_cost_func (self):
          
          return self.cost_func
     def random_select_cost(self,players):
          path=np.zeros(self.path_num)

          
          total_path_select= {new_list: [] for new_list in range(self.path_num)}
          for i in range (players.player_num):
               tmp=np.random.choice(a=3,size=1,p=players.player_list[i].possibility)
                
                
               total_path_select[tmp[0]].append(i)
          

          print(total_path_select)
          for key ,value in total_path_select.items():
               # print(key, type(key),value)
               tmp_cost=self.cost_func[key](len(value))
               for player in value:
                    # print(player,type(player))
                    # print(tmp_cost)
                    self.player_cost[player]=tmp_cost       

               
     def get_cost(self,players):
           
          for people in range(players.player_num):
               tmp = list()
               for poss in range(self.path_num):
                    n=self.cost_func[poss](players.player_list[people].possibility[poss] )
                    
                    tmp.append(n)
               self.player_cost.append(tmp)
          self.player_cost=np.asarray(self.player_cost)

     
if __name__ == '__main__':
     cost=[[2,3],
          [3,2],
          [4,0]]
     #n1=player(3)
     n2=path_cost_function(cost,3,6)
     #res = n1.possibility.dot( n2.cost_func)
     # # print (n1.get_possibility())
     
     
     print(n2.get_cost_func())
    

     #print ("res",res)
     n=all_player(6,3)
     n.player_print()
     n2.random_select_cost(n)
     print(n2.player_cost)
     #n.player_print()



