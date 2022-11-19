
import matplotlib.pyplot as plt        
class plot():
    def plot_diff(T,real_diff ):        
        times=[i+1 for i in range(T)]
        plt.plot(times,real_diff,color=(255/255,100/255,100/255))
        plt.title("indicator") # title
        plt.ylabel("diff") # y label
        plt.xlabel("times") # x label
    def show():
        plt.show()
        plt.clf()

    def plot_select_path(player_select_path_num):
        
        for times in player_select_path_num:
            plt.clf()
            
            names = list(times.keys())
            values = list(times.values()) 
            plt.bar(range(len(times)), values, tick_label=names)
            plt.pause(0.3)
         
        