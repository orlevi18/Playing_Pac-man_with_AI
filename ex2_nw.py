from mdp import *
import time
import random

class Controller:
    "This class is a controller for a Pacman game."
    
    # document: creating all the posible board states and policy at a given 60 sec, need to think on reducing time maybe 
    # insted of creating the whole board, create only the area near pacman.
    def __init__(self, board, steps):   
        """Initialize controller for given game board and number of steps.
        This method MUST terminate within the specified timeout."""
        begin_time = time.time()
        self.board = board
        self.steps = steps
        self.mdp = GridMDP(board, set(),set(), pacman_position(board))
        val_iter = value_iteration(self.mdp, begin_time)
        self.policy = best_policy(self.mdp,val_iter)

    # document: finding the index of the given board and calling policy with that index and pacman current position.
    def choose_next_move(self, board):
        "Choose next action for Pacman given the current state of the board."
        move = dict(zip(((-1,0), (0,1), (1,0), (0,-1)),('L','D','R','U')))
        j = 0
        for i in self.mdp.states:
           j += 1
           if board == i:
             break
        print pacman_position(board) , move[self.policy[j-1,pacman_position(board)]]
        return move[self.policy[j-1,pacman_position(board)]]

# document: return pacman position (i,j)
def pacman_position(board):
          for j, row in enumerate(board):
            for i, square in enumerate(row):
                what_is = divmod(square, 10)
                if what_is[0] == 7:
                    return (i,j)

class GridMDP(MDP):
    """A two-dimensional grid MDP, as in [Figure 17.1].  All you have to do is 
    specify the grid as a list of lists of rewards; use None for an obstacle
    (unreachable state).  Also, you should specify the terminal states.
    An action is an (x, y) unit vector; e.g. (1, 0) means move east."""
    def __init__(self, grid, terminals, obstacle, init=(0,0), gamma=0.9):
        MDP.__init__(self, init, actlist= [(1,0),(0,1),(0,-1),(-1,0)],
                     terminals=terminals, gamma=gamma)
        update(self, grid=grid, rows=len(grid), cols=len(grid[0]), cherry= set(),ghost = set(),pallets = set(),gates = set(),emptysquare = set(), pacman_post = set())
        self.grid = grid
        self.sort_states(grid)
    
    # document: harvest board for data regarding positions of: cherry,gates,monsters,pallets,emptysquare
    # after, create self.state((board),(board)...) of possible board states. and self.reward[(Board_Index,(i,j))] for each move state.

    # TODO: complete self.reward[(Board_Index,(i,j))] = reward for a certain state: (i,j) at a certain board: index_i, rewards are:
    # -10 = monster, 1 = pallet, (1.0/3.0)*5 = cherry,  0 = blank/packman, -0.5 = gate closed/open
    # complete board state creating proccess
    # every following code sample create board state.
    #    board_index +=1
    #    self.states.add(tuple(tuple(z) for z in tempgrid))
    #    tempgrid = map(list, grid) 


    def sort_states(self,grid):
         for j, row in enumerate(grid):
            for i, square in enumerate(row):
               # start remove - need to make it automaticly with currect values
               self.reward[(0,(i,j))] = 0 
               self.reward[(1,(i,j))] = 0 
               self.reward[(2,(i,j))] = 0 
               self.reward[(3,(i,j))] = 0 
               self.reward[(4,(i,j))] = 0 
               self.reward[(5,(i,j))] = 0 
               self.reward[(6,(i,j))] = 0 
               self.reward[(7,(i,j))] = 0 
               self.reward[(8,(i,j))] = 0 
               self.reward[(9,(i,j))] = 0 
               self.reward[(10,(i,j))] = 0 
               self.reward[(11,(i,j))] = 0 
               self.reward[(12,(i,j))] = 0 
               # end remove
               what_is = divmod(square, 10)
               if what_is[0] == 7:
                   self.pacman_pos = (i,j)
               if what_is[1] == 5:
                   self.cherry.add((i,j))
               if  20 <= square <= 59:
                   self.ghost.add(((i,j),(what_is[0]*10)))
               if square == 11:
                   self.pallets.add((i,j))
               if square !=99 and what_is[1] == 9:
                   self.gates.add((i,j))
               if square == 10:
                   self.emptysquare.add((i,j))
         
         board_index = 0
         tempgrid = map(list, grid)
         for j, row in enumerate(grid):
            for i, square in enumerate(row):
                     what_is = divmod(square, 10)
                     if what_is[1] == 5:
                        tempgrid[j][i] = 10 
                        self.reward[((board_index),(i,j))] = 0 
                        board_index += 1
                        self.states.add(tuple(tuple(z) for z in tempgrid))
                        tempgrid = map(list, grid)  
                        tempgrid[j][i] = 15 
                        self.reward[((board_index),(i,j))] = (1.0/3.0)*5
                        board_index += 1
                        self.states.add(tuple(tuple(z) for z in tempgrid))
                        tempgrid = map(list, grid)  
                        tempgrid[self.pacman_pos[1]][self.pacman_pos[0]] = 15
                        tempgrid[j][i] = 75 
                        self.reward[((board_index),(i,j))] = 0
                        board_index +=1
                        self.states.add(tuple(tuple(z) for z in tempgrid))
                        tempgrid = map(list, grid)  
                        for ghost in self.ghost:
                               tempgrid[ghost[0][1]][ghost[0][0]] -= ghost[1]-10
                               tempgrid[j][i] = 5+ghost[1]
                               self.reward[((board_index),(i,j))] = -10
                               board_index += 1
                               self.states.add(tuple(tuple(z) for z in tempgrid))
                               tempgrid = map(list, grid)  
                     elif  20 <= square <= 59:
                        self.reward[((board_index),(i,j))] = 0 
                        for ghost in self.ghost:
                               tempgrid[ghost[0][1]][ghost[0][0]] = ghost[1]+5
                               tempgrid[j][i] = 15+ghost[1]
                               self.reward[((board_index),(i,j))] = 0
                               board_index +=1
                               self.states.add(tuple(tuple(z) for z in tempgrid))
                               tempgrid = map(list, grid)   
                     elif square == 11:
                        self.reward[((board_index),(i,j))] = 0
                        board_index +=1
                        self.states.add(tuple(tuple(z) for z in tempgrid))
                        tempgrid = map(list, grid) 
                        self.pallets.add((i,j))
                     elif square !=99 and what_is[1] == 9:
                        self.reward[((board_index),(i,j))] = 0
                        board_index +=1
                        self.states.add(tuple(tuple(z) for z in tempgrid))
                        tempgrid = map(list, grid) 
                        self.gates.add((i,j))
                     elif square == 10:
                        self.reward[((board_index),(i,j))] = 0
                        board_index +=1
                        self.states.add(tuple(tuple(z) for z in tempgrid))
                        tempgrid = map(list, grid) 
                        self.emptysquare.add((i,j))
                     else:
                        self.reward[((board_index),(i,j))] = 0
                        board_index +=1
                        self.states.add(tuple(tuple(z) for z in tempgrid))
                        tempgrid = map(list, grid) 

    def R(self,board_i, state): 
        "Return a numeric reward for this state."
        return self.reward[((board_i),state)]


    def actions(self, board_i, state):
        """Set of actions that can be performed in this state.  By default, a 
        fixed list of actions, except for terminal states."""
        posible_actions_list = self.posible_actions(board_i, state, [(1,0),(-1,0),(0,1),(0,-1)] )
        random.shuffle(posible_actions_list)
        return posible_actions_list
     
    def posible_actions(self,board_i, state, act_list):
            a_list = []  
            for act in act_list:
                if 0 <= state[0]+act[0] < self.cols and 0 <= state[1]+act[1] < self.rows :
                  if self.reward[board_i,(state[0]+act[0],state[1]+act[1])] >= 0:  
                    a_list.append(act)
            if len(a_list) == 0:
                return [None]
            return a_list
    
    #todo: understand the meaning of T and probability and implement the currect way.
    def T(self, board_i, state, action):
            """Transition model. From a state and an action, return a list of (probability, result-state) pairs."""
            b_list = []
            temp = list(self.states)
            for a in self.actlist:
                    if ((0 <= (state[0]+action[0]+a[0]) < len(temp[board_i][0])) and (0 <= (state[1]+action[1]+a[1]) < len(temp[board_i]) )) :
                        b_list.append((1.0/len(self.actlist),(state[0]+action[0]+a[0],state[1]+action[1]+a[1])))
            return b_list
 

# todo: check time limit and product 
def value_iteration(mdp,begin_time, epsilon=0.001):
    "Solving an MDP by value iteration. [Fig. 17.4]"    
    R, T, gamma = mdp.R, mdp.T, mdp.gamma
    U_list = {}
    while (time.time()-begin_time<59):
     for board_i, board in enumerate(mdp.states):
         U1 = {}
         for j, row in enumerate(board):
           for i, square in enumerate(row):
             U1[(i,j)] =  mdp.R(board_i, (i,j))
         flag = True
         while flag:
             U = U1.copy()
             #print U[mdp.init]
             delta = 0
             for j, row in enumerate(board):
               for i, square in enumerate(row):
                 e_of_a_list=[]
                 for a in mdp.actions(board_i, (i,j)):
                     if (time.time()-begin_time>56):
                             U_list[board_i] = U
                             return U_list
                     sume=0
                     for (p, s1) in T(board_i, (i,j), a):   
                         sume+=p*U[s1]
                     e_of_a_list.append(sume)
                     sume=0
                 U1[(i,j)] = R(board_i,(i,j)) + gamma * max(e_of_a_list)  
                 delta = max(delta, abs(U1[(i,j)] - U[(i,j)]))
                 if delta < epsilon * (1 - gamma) / gamma:
                     U_list[board_i] = U
                     flag = False
     if (time.time()-begin_time<59):
         return U_list
    U_list[board_i] = U
    return U_list


def expected_utility(a, board_i, s, U, mdp):
    "The expected utility of doing a in state s, according to the MDP and U."
    return sum([p * U[s1] for (p, s1) in mdp.T(board_i, s, a)])   

def best_policy(mdp, U):
    """Given an MDP and a utility function U, determine the best policy,
    as a mapping from state to action. (Equation 17.4)"""
    "Connect PI to S -> Every pi[board_index][state - (x,y)] = New Reward Value after 60 sec iterations"
    pi = {}
    for board_i, board in enumerate(mdp.states):
       for j, row in enumerate(board):
          for i, square in enumerate(row):
            pi[board_i, (j,i)] = argmax(mdp.actions(board_i,(j,i)), lambda a:expected_utility(a, board_i, (j,i), U[board_i], mdp))
    return pi        
