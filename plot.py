import numpy as np
import matplotlib.pyplot as plt     
def ramdom_color():
        col=  (np.random.random(), np.random.random(), np.random.random())   
        print(col)
        return  col          
class plot():
    
          
    def plot_diff(T,real_diff ,line_name):        
        times=[i+1 for i in range(T)]
       
        plt.plot(times,real_diff,color=ramdom_color(),label=line_name)
        plot.line_show()
        
    def line_show():
        plt.legend(
        loc='best',
         
         
        )
        plt.title("indicator") # title
        plt.ylabel("diff") # y label
        plt.xlabel("times") # x label
        plt.show()

    def show():
        plt.show()
        plt.clf()
        plt.close()


    def plot_select_path(player_select_path_num):
        
        for times in player_select_path_num:
            plt.clf()
            
            names = list(times.keys())
            values = list(times.values()) 
            plt.bar(range(len(times)), values, tick_label=names,color=ramdom_color())
            plt.pause(0.3)
        plot.show()

    def plot_prob(path_prob,T): 
        path_prob = path_prob.T
        times=[i+1 for i in range(T)]
        plt.plot(times, path_prob[0],'r',label="path1")
        plt.plot(times, path_prob[1],'y',label="path2")
        plt.plot(times, path_prob[2],'g',label="path3")
        plt.plot(times, path_prob[3],'b',label="path4")
        plt.show()     
        