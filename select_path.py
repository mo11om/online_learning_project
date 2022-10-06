import numpy as np
def panning(strategy) :
    sum_ = 0
    sum_ = sum(strategy)
    range_ = 1 - sum_/len(strategy)
    strategy = strategy + range_
    positive_sum = sum([i for i in strategy if i > 0])
    positive_number = len([i for i in strategy if i > 0])
    while  abs(positive_sum - 1) > 0.01  :
        range_ = (1 - positive_sum)/positive_number
        strategy = strategy + range_
        positive_sum = sum([i for i in strategy if i > 0])
        positive_number = len([i for i in strategy if i > 0])
    strategy[strategy < 0] = 0
    return strategy 
    
def  refresh_strategy(past_cost , past_strategy, times, learn_rate) :
    strategy = np.zeros(len(past_strategy))
    gradient = np.zeros(len(past_strategy))
    for i in range(times): #moving times 
        gradient = past_cost + (2/learn_rate)*(strategy - past_strategy)
        strategy = strategy - gradient
        print(strategy)
    new_strategy = panning(strategy) 
    return new_strategy
    #rera   
