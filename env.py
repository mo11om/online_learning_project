 


 
import numpy as np
import math  
import random 

class player :
     def  create_random(self):#3 
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

          self.possibility =self.create_random()     
     def get_possibility (self):
          
          return self.possibility

class all_player :
     def __init__(self,player_num,path_num):
          self.palyer_list=list()
          self.num_player = player_num
          for i in range(player_num):
               self.palyer_list .append(player(path_num)) 

     def player_print (self):
          
          for i in range(self.num_player):
             print(i,  self.palyer_list[i].get_possibility() )



          
class path_cost_function:
     def __init__(self,cost_value):     
          self.xpower=np.array(cost_value)
          
     def get_xpower (self):
          
          return self.xpower
     #def get_cost(self,parameter):

if __name__ == '__main__':
     cost=[[2,3],
          [3,2],
          [4,0]]
     n1=player(3)
     # n2=path_cost_function(cost)
     # res = n1.possibility.dot( n2.xpower)
     # # print (n1.get_possibility())
     
     
     # # print (n2.get_xpower())


     # print ("res",res)
     n=all_player(6,3)
     n.player_print()



