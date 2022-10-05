import numpy as np
def panning(strategy) :
    sum_ = 0
    sum_ = sum(strategy)
    range_ = 1 - sum_/len(strategy)
    strategy = strategy + range_
    positive_sum = sum([i for i in strategy if i > 0])
    positive_number = len([i for i in strategy if i > 0])
    while(positive_sum != 1) :#float problem
        range_ = (1 - positive_sum)/positive_number
        strategy = strategy + range_
        positive_sum = sum([i for i in strategy if i > 0])
        positive_number = len([i for i in strategy if i > 0])
    return strategy

    


# def  refresh_strategy(past_cost , past_strategy, times, learn_rate)
#      strategy = np.zeros(len(path_strategy))
#      gradient = np.zeros(len(path_strategy))
#      for i in range(times): #moving times 
#         gradient = 2*strategy - 2*past_strategy + past_cost 
#         strategy = strategy - learn_rate*gradient
#     sum_ = sum(strategy)
#     new_strategy = map(strategy) 
#     return new_stratgy         


a = panning(np.array([-1.1, 0.2, 0.4]))
print(a)