<!-- # online_learning_project![csn-xski-ghs - 2022年9月23日 1](https://user-images.githubusercontent.com/66251276/191983443-6f52f73b-c9f7-4302-a267-7389eaa663b1.png) -->
# 1. **enviroment** 

   * env.py
   * **allplayer**
    * *variable*
        * **player** 
            * *variable*
            1. pathnum(*int*)
               * record how many path one player can choose

            2. probability
                * record probility of player select road :
                *  EX :  [*1/3,1/3,1/3* ]
            3. estimate_probability
                * record estimate probility of player select road
                *  EX :  [*1/3,1/3,1/3*]
        * allplayer 
          * contain a list of player
          * [p1,p2,p3]  
# 2. **algorithm**
   1. **hindcost**
       * **select_path.py**   
         * **variable**
           *   self.cost_func
               *  *list()* 
               *  record path cost function of each path 
               *  use specific structure 
               *   np.poly 
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
         * **function**
            * random_select_cost
              * from strategy to select a path  and calculate every route cost   
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