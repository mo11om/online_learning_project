import numpy as np
from scipy.optimize import minimize

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
    
def  refresh_strategy(past_cost, past_strategy, times, learn_rate, scale) :
    strategy = np.zeros(len(past_strategy))
    gradient = np.zeros(len(past_strategy))
    for i in range(times): #moving times 
        gradient = past_cost + (2/learn_rate)*(strategy - past_strategy)
        strategy = strategy - gradient
    new_strategy = panning(strategy, scale) 
    return new_strategy

def object(strategy, last_strategy, cost, learn_rate) :
    return cost.dot(strategy.T) + (1/learn_rate)*(strategy - last_strategy).dot((strategy - last_strategy).T)

def constraint(strategy) :
    return np.sum(strategy)- 1

def refresh_strategy_minimize(last_strategy, cost, learn_rate) :
    x0 = np.full((1, len(last_strategy)), 1/len(last_strategy))
    b = (0, 1)
    buds = []
    for i in range(len(last_strategy)) :
        buds.append(b)
    cons = [{'type' : 'eq', 'fun' : constraint}]
    sol = minimize(fun=object, x0=x0, args=(np.array(last_strategy),
                   np.array(cost), learn_rate), method='SLSQP', bounds=buds,
                   constraints=cons)
    return sol.x
    
def get_key(val, total_path_select):
  for key, value in total_path_select.items():
    if val in value:
      return key

def potential_function(total_path_select, cost_func) : #cost_func is a set of poly1d
    potential_value=0
    for path, driver in total_path_select.items() :
        for i in range(0, len(driver)+1) :
            potential_value = potential_value + cost_func[path](i)
    return potential_value

