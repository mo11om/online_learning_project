import numpy as np
def panning(strategy, scale) : #strategy must be a np.array!!
    sum_ = 0
    sum_ = sum(strategy)
    range_ = scale - sum_/len(strategy)
    strategy = strategy + range_
    positive_sum = sum([i for i in strategy if i > 0])
    positive_number = len([i for i in strategy if i > 0])
    while  abs(positive_sum - scale) > 0.01  :
        range_ = (scale - positive_sum)/positive_number
        strategy = strategy + range_
        positive_sum = sum([i for i in strategy if i > 0])
        positive_number = len([i for i in strategy if i > 0])
    strategy[strategy < 0] = 0
    strategy = strategy/scale
    return strategy 
    
def  refresh_strategy(past_cost , past_strategy, times, learn_rate, scale) :
    strategy = np.zeros(len(past_strategy))
    gradient = np.zeros(len(past_strategy))
    for i in range(times): #moving times 
        gradient = past_cost + (2/learn_rate)*(strategy - past_strategy)
        strategy = strategy - gradient
    new_strategy = panning(strategy, scale) 
    return new_strategy

def get_key(val, total_path_select):
  for key, value in total_path_select.items():
    if val in value:
      return key
