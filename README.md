# Tracking the environment of the Non-staitonary stochastic game with mutiple agents 

## Introduction

### Framework 

The framework of this project, simply to say, we want to implement some algorithms provided from [1] which can achive the best performance of congestion game. Algorithms give all players(drivers) a strategy they can follow, and help the whole game lower "indicators". Those algorithms use some methods to repond the change of the environment, that is, players change their strategy from time to time, so no matter what kinds of situation, players always can figure out the relatively better action. We called this kind of methods as "online algorithm" which means algorithms make decision after receiving partial information instead of all information(offline algorithm). 

Our research have little bit different from [1]. It designs algorithms for single agent; however, we implement those in mutiple agents conditions.Even so, we still observe reasonable result.

### Measurements
We have different indicators to measure the game-- regret, potential value, social cost. All indicators have strict definition,and they can be written as mathematics symbols. However, here we just explain them by the simplest example, so that readers can easily understand the meaning of each.![](https://i.imgur.com/pz6hxxc.png)

There are four paths can be selected by drivers, and each of them has a formula to measure the cost of choosing that path.(*x* is number of drivers) 

If three drivers choose path2, path2, and path3:

**Regret** 
As the name suggests, it measures how player's choice compares to best choice which found in some way(in fact, it is offline algorithm). 

The best path is path1; therefore, regret would be sum of player's cost 2(1x2+3)+1(3x1) minus the best path cost 3(2x3+1).
(the x here is Multiplication sign)

**Potential value**
Formal math symbol likes this : 

We would not expain it. You can find the specific explanation in [2, page223].

(1) **First driver** selects path2 when path2 has 1 people(himself), so his cost is 1x1+3.
(2) **Second driver** selects path2 when path2 has already had two people(first driver and himself), so his cost is 1x2+3.
(3) **Third driver** selects path3 when path3 has 1 people, so so his cost is 3x1.

To sum up, the total cost in this round is (1x1+3)+(1x2+3)+(3x1)

**Social cost**
The strict mathmatics definition of social cost also can be found in [2]. 

(1) **One driver** selects path2 when path2 has two people, so his cost is 1x2+3.
(2) **A nother driver** selects path2 when path2 has two people, so his cost is 1x2+3.
(3) **The other driver** selects path2 when path2 has two people, so his cost is 3x1.

To sum up, the total cost in this round is (1x2+3)+(1x2+3)+(3x1)

Be mindful of social cost and potential value. They are pretty similar, but potential value has notion of sequence, while social cost doesn't.

### Environment restrictions
**Bendit setting** 
In this setting, all players only know the cost of the path they select. It is reasonable to imagine, when we drive car on the highway, the only thing we can konw is if this road is jammed.

**Full information setting**
full-information provide more information about other path. There are some advanced devices on the car which monitor the condition of other paths, including paths not chosen by the driver.
### Definition of the problem
There are *N* players(drivers) intend to reach the same destination from the same outset, and *K* paths they can choose. This kind of the game would repeat *T* times, and in the end of each round all players receive **cost**(form of cost depends on Environment restrictions). Acorrding to cost, Players redesign their strategies, that is, they choose the path which is most efficient to reduce the indicators.

We need algorithms to gurantee all players can make this purpose.

## Algorithm
![](https://i.imgur.com/nbEKgAy.png)

This opitimistic gradient descent algorithm has two features 
1. It only inplies in full-information setting.
2. All players adopt the same strategy for same round.


As we mention before, this algorithm is designed for single agent, so, if we see each of players as a single entity and they use this algorithm, they would receive completely the same cost(Note that this is based on full-inoformation setting).

We also expain the updating formula in informal way : 
![](https://i.imgur.com/dqlfBN8.png)
**First term**
Expected loss(the loss of each road times their probability)
**Second term**
A penalty term that prevents new strategy from being too far away from the original strategy. 


## Algorithm realization
### weak offline and strong offline comparator
**Weak regret**
Offline algorithm can only choose one path(one action) in *T* rounds.
**Strong regret**
Offline algorithm can change its action T times in *T* rounds. 

Obviously, strong regret offline algorithm have better result, so, when we compare our online algorithm with it, we might have huge regret than comparing with weak regret offline algorithm.

**The diagrams of regret comparing to weak offline algorithm**
![](https://i.imgur.com/coA85bI.png)
Left one records exactly regret in each round, while right one records the t rounds average regret(in this way, the curve become more smooth, so that we can easily observe the trend of regret).

No matter in what way to present, we can see the regret has converged acutely before 200 round, though the speed of congergence gradually slow after it. Finally, it is stable in 79 in the average value. 

Another observation, left diagram shows that after 200 round, regret becomes alternate high and low every round. This phenomenon is caused by optimistic gradient descent. 

**The diagrams of regret comparing to strong offline algorithm**
![](https://i.imgur.com/6SJyPjv.png)
 Here, we design an offline algorithm pretty powerful. In each round, we pause the the game and allow all players have an opportunity to re-select their path in that round.

We call the initial condition(after making first selection) as **orginal env**. For each player,it faces the condition that other players are fixed. That player can freely re-select the path which has least cost for itself. After finishing one player, we recover the game to oringal env, and sequentially do the same process to another player until all players have completed. For each round, we add this step to generate a strict offline algorithm result to compare. Of couse, because this method always choose the least cost path, so the regret is never lower than 0.

As we can see, left diagram doesn't show any sign of convergence. Even though the right diagram indicates that average regret converges extremely in first 100 rounds, its convergence value(373) is still higher than weak comparator.

Our conclusion is that this algorithm works against relatively weak offline comparator, yet it is somehow useless for extremely strong offline comparator result.


### Upper bound theorem

**Upper bound in [1]**
![](https://i.imgur.com/Rf5PZcx.png)

From [1], this algorithms gurantees an upper bound. It allows our updating formula have a dynamic learning rate to achieve.Therefore, we try to use various learning rate to observe the difference they cause.
![](https://i.imgur.com/ebAXqMI.png)

The orange line means the theorem bound, and blue line means practical regret. upper-right diagram is the result of dynamic learning rate provided by [1]. Blue line almost overlaps on orange line, this means this theorem evaluates its upper bound very precisely. 

We also observed another interesting phenomenon, if the learning rate is smaller, the number of steps that regret tends to converge will be less. When learning rate is fixed in 0.001, practical regret start to converge in 45 step, though 0.005 and 0.01 can't see convergence in 100 steps. 

### Potential value and social cost
Here we simply show the diagrams of potential value and social cost.

**diagram of potential value**
![](https://i.imgur.com/LSDVbRa.png)
We can see the similar diagram like regret. We will further deeply  explain about this measurement. Now we just provide a conceptual impression that potential value is related with regret. 

**diagram of social cost**
![](https://i.imgur.com/pl2EULR.png)
Here, we also present social cost's result, while we would not spend too much time in this measuremnet.

Simply observing the convergence value of two measurement, social cost are equal or more than potential value. 

## Extended Issues
### Dynamic learning rate
During the experiment, we discover that there is an obvious impact on our experiment result by adjusting the learning rate. Choosing diffrernt kinds of learning rate causes different effects on result.

**(1)** Larger learning rate causes the faster speed of convergence.
**(2)** Small learning rate is able to reach the better experiment results.

We choose to use the **Dynamic learning rate** ,which sets the larger learning rate at the begining and reduces it gradually.
### Difference between continue and discrete
When experimenting different kinds of learning rate, we find out that our the experiment results are unable to reach the optimal condtion. It is because that there are the relatively larger particles when the amount of players in the game is fewer.This causes the gap between the optimal answer and our experiment result.

We use the **continue** congestion game to simulate the game that its players approach infinity. The flow of each road is equal to the expected flow. We discover some points.

**(1)** We can get the experiment results close to the optimal one when using the Continue game.
**(2)** The potential values of Discrete game are getting close to the Continue game when the amount of players increases.
### Application of batch learning
At the process of experiment, we always spend lots of time waiting the results. It is because our algorithm makes the players renew their strategy in each round. This method really makes the results converge ,but increasing the variation of the congestion game and the operating time.

We use **Batch learning** to reduce the operating time. Batch Learning lets players renew their strategy after several rounds, and collect the average cost in these rounds as the renew information. Although it costs more steps to reach convergence situation, it makes some adventages.
**(1)** Batch Learning reduces operating time effectively.
**(2)** Batching Learning makes the learning curve smoother,which decreases the variation of the congestion game.
## Self-made Algorithm
Previous research puts attention on full information setting; therefore, in this section, we want to make an algorithm by ourself to apply on bendit setting.

Refering to Rerun-UCB algorithm(deterministic) from [1] and full-information algorithms, we try to make a stochastic algorithm. After experimenting, this algorithm can output a result which only slightly worse than Rerun-UCB.

This self-made algorithm have some features we want to present before complete intruduction. It judges the environment by history data, can be measured by potential value and regret, and contains concept of probability and statistics.

### Simple introduce of Rerun-UBC
One of the most famous algorithm using exploration and exploitation to achive better result is UBC algorithm. We can't hlep but mention this great pattern. 

**UCB algorithm**[reference link](https://github.com/mo11om/online_learning_project)
![](https://i.imgur.com/zB4DnRl.png)
This algorithm provided from [1]. Forth row is the only one section to update player's action. As we can see, this is a diterministic method, because it would not generate a distribution but a clear path. The system appears to score all paths and incorporates a number of factors, including **exploration**(the paths already traveled have a score, depending on average of privious feedback) and **exploitation**(the paths never taken have higher score). This idea is reasonable to image, so we want to add this into our self-made algorithm.
 
"Re"run means this algorithm disconnects whole precess into many small period, this method can adopt non-stationary environment, that is, if we cut a long time period into many small time period, we can roughly seem samll one as a static environment, then apply methods dealing with static environment in this problem.

### Concept 
According to previous full-information algorithm ,we have a instinct thought -- 

(1) High cost decrease the desire to go that path.  
(2) Low cost increase the desire to go that path.

We want our algorithm can make it to update its policy, so that it can have relatively low expected loss.  
### Code
#### 1. **enviroment** 

   
 
    
* **player** 
    
    * pathnum
        * *int*
        * record how many path one player can choose

    * probability
        * record probility of player select road :
        *  EX :  [*1/3,1/3,1/3* ]
    * estimate_probability
        * record estimate probility of player select road
        *  EX :  [*1/3,1/3,1/3*]
* allplayer 
  * contain a list of player
  * [p1,p2,p3]  
#### 2. **algorithm**
   
##### **variable**
   *   self.cost_func
       *  *list()* 
       *  record path cost function of each path 
       *  use specific structure **np.poly** 
       *   [f(1),f(2),f(3)] 
   *   self.path_cost 
       *    *list()*
       *    record every path cost
       *    np.zeros(path_num)
       *    [1.5 ,5.7 , 9.8] 
   *   self.total_path_select 
       *  *dict()*  
       * record all player's final choice for one round
       * EX: {1:[p1],2:[p2]}    
   *   self.average_regret 
       *   *list()*
       *   record average regret of times
   *   self.potential_value 
       *   *list()*
       *    record average regret  of times
   *   self.all_play_total_path_select
       *   *list()*
       * record all player's final choice for one round
       * EX: {1:[p1],2:[p2]}
##### **function**
* random_select_cost
    * from strategy to select a path  and calculate every route cost

```python
 def random_select_cost(self) : 
          self.total_path_select = {new_list: [] for new_list in        range(self.path_num)} 
          #creat empty dict => {0:[], 1:[], 2:[]}
          for i in range (self.player_num) :
               choice_path = np.random.choice(
                   a=self.path_num,
                   size=1,
                   p=self.players_strategy[i].estimate_probability)

               self.total_path_select[choice_path[0]].append(i)

          
          path_sum={}# [0:5,1:5]
           
               

          for path ,driver in self.total_path_select.items() :
               path_sum[path]=(len(driver))
               path_cost = self.cost_func[path](len(driver))              
            #calculate path cost
               self.path_cost[path] = path_cost   
 
          self.all_play_total_path_select.append(path_sum)
          return self.path_cost
```
 
* update_strategy
  * update possibility disturbtion
*  hindsight 
   *  calculate hindsight cost
*  potential_function
   *  calculate potential value
*  play_a_game
   *  update_estimate
   * random_select_cost
   * calculate hindsight 
   * calculate potential value

### Algorithm [reference link](https://colab.research.google.com/drive/1lSbbo9vEnyNvPbuSklBpFCWmTnUTGE-A?usp=sharing)
Having refer to the full-information setting, we take the strategy of updating the probability distribution.
Self-made algorithm—**Algorithm 2**
![](https://i.imgur.com/WuBOUmZ.png)
The probability vector x[i] is constant in the current round, while the probability vector a[i] of next round is a variable which should be updated by minimizing the function as follows:

**(a[i]-x[i])‧(a[i]-x[i]) + learning_rate × x[i]‧(*n*×p[i] - p.sum)**

The vector p[i] is the weighted average of costs.

**p[i]:  (1-*e*)×cost[i] + *e*×p[i]**

***e*** is parameter can be adjusted dynamically between 0 and 1. It will affect the convergence speed and volatility.
Besides, a large learning rate should be set at the beginning, and reduced gradually as the optimal probability is approached. This action would lead to better results.

### Result
Since the setting of our example is quite simple, we can solve the simultaneous equations as follows.
𝑓1+20 = 5𝑓2+10 = 2𝑓3+30 = 𝑓4+50
𝑓1+𝑓2+𝑓3+𝑓4=50
𝑓1, 𝑓2, 𝑓3, 𝑓4 ≥ 0
Flow:
𝑓1=30.74, 𝑓2=8.15, 𝑓3=10.37, 𝑓4=0.74
Probability:
𝑝1=0.6148, 𝑝2=0.163, 𝑝3=0.2074, 𝑝4=0.148

The result of Algorithm 2 and Rerun-UCB:
![](https://i.imgur.com/NZhssse.png)

![](https://i.imgur.com/SrCLWUz.png)

We can see that the result of Rerun-UCB-V is closer to the optimal solution than Algorithm 2.
Rerun-UCB-V also performed better by measuring the regret and potential value, but our algorithm can also obviously observe the convergence situation, and the probability distribution also moves towards the optimal solution.

**Reasons**
There are two reasons we consider Algorithm 2 not performed well: 
1.Exploration and exploitation cannot approach less regret or potential value since this method should require costs to explore.
2.The function of Algorithm 2 minimizing is not rigorous in mathematics, the result converges near the optimal solution instead of toward it.

**Batch** [reference link](https://colab.research.google.com/drive/11qdocoBYlqueX5wWXHUe3BY8dMCFFN0W?usp=sharing)
As the situation at full-information setting, we want to see the batch used in the bandit setting. An intuitive idea is that the same group uses the same probability distribution to select paths, and the next group uses all the information obtained in this batch to update the probability distribution, which can reduce the influence of extreme situations and make the algorithm more stable. We take 5 rounds in a batch.

![](https://i.imgur.com/6fRkGLy.png)
![](https://i.imgur.com/x6WObMv.png)

The probability distribution with batch is more close to the Rerun-UCB-V solution. The potential value has made significant progress. Though there is still room for improvement, taking batchs would perform better than the algorithm without it. In comparison, it is recommended to use batches in a bandit setting as well.
## Future work

## Reference
[1]Chen-Yu Wei, Yi-Te Hong, Chi-Jen Lu(2017). Tracking the best Expert in Non-stationary Stochastic Environments. https://arxiv.org/abs/1712.00578
[2]Po-An Chen, Chi-Jen Lu(2016). Generalized mirror descents in congestion games.
https://www.sciencedirect.com/science/article/pii/S0004370216301084

### Code 
https://github.com/mo11om/online_learning_project
https://colab.research.google.com/drive/1HL5AMlb8TjPWydDSHI23iHphlNNy3w1H?usp=sharing
https://colab.research.google.com/drive/1lSbbo9vEnyNvPbuSklBpFCWmTnUTGE-A?usp=sharing
https://colab.research.google.com/drive/11qdocoBYlqueX5wWXHUe3BY8dMCFFN0W?usp=sharing
























