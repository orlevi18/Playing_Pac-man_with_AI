import random
import time

class Game:    
    """Game class --- presents a Pacman game played for given number of steps."""
    
    def __init__(self, steps, board):
        """Initialize the Game class.       
        steps - represents the number of steps the game is run 
        board - the initial state of the board"""
        self.steps = steps
        self.init = board
        self.set_locations()
        
        self.actions = dict(zip(('L','D','R','U'), ((-1,0), (0,1), (1,0), (0,-1))))
        
        
    def set_locations(self):
        """Sets the locations of ghost and pellets from the initial state.
        Magic numbers for ghosts and Pacman: 
        2 - red, 3 - blue, 4 - yellow, 5 - green and 7 - Pacman."""
        
        self.init_locations = dict.fromkeys((7, 2, 3, 4, 5))
        self.init_pellets = set()
        self.gates = set()
        
        for j, row in enumerate(self.init):
            for i, square in enumerate(row):
                what_is = divmod(square, 10)
                if 2 <= what_is[0] <= 5 or what_is[0] == 7:
                    self.init_locations[what_is[0]] = (i,j)
                if 1 <= what_is[1] <= 5:
                    self.init_pellets.add((i,j))
                if what_is[0] != 9 and what_is[1] == 9:
                    self.gates.add((i,j))
           
    def reset(self):
        """Resets the board and ghost locations to the initial state."""
        self.done = False
        self.locations = self.init_locations.copy()
        self.pellets = self.init_pellets.copy()
        self.board = list(list(row) for row in self.init)            

    def there_is_cell(self, move):
        if 0 <= move[0] < len(self.init[0]) and 0 <= move[1] < len(self.init):
            return True
        return False

    def move_gates(self):
        for gate in self.gates:
            if not 20 <= self.board[gate[1]][gate[0]] <= 80:
                if random.choice([False, True]):
                    self.board[gate [1]][gate [0]] = 89
                else:
                    self.board[gate [1]][gate [0]] = 19
    
    def move_pacman(self, move):    
        move_check = move[0] + self.locations[7][0], move[1] + self.locations[7][1]
        
        if not self.there_is_cell(move_check) or self.board[move_check[1]][move_check[0]] >= 89:
            return -1
        
        what_is = list(divmod(self.board[move_check[1]][move_check[0]],10))
        
        if 2 <= what_is[0] <= 5:
            self.done = True
            return 0
        else: 
            self.board[self.locations[7][1]][self.locations[7][0]] -= 60
            self.locations[7] = move_check
            
            if what_is[1] != 1 and not (what_is[1] == 5 and random.choice([False, False, True])):
                what_is[1] = 0
            else:
                self.pellets.remove(move_check)
            
            self.board[self.locations[7][1]][self.locations[7][0]] += (60 - what_is[1])
            return what_is[1]

    def move_ghost(self, ghost_num):
        ghost_location = self.locations[ghost_num]
        
        possible_act = []
        for action in ((1,0), (0,1), (-1,0), (0,-1)):
            move = ghost_location[0] + action[0], ghost_location[1] + action[1]
            if self.there_is_cell(move) and (self.board[move[1]][move[0]] < 20 
                                        or self.board[move[1]][move[0]] // 10 == 7):
                possible_act.append(move)
        
        if not possible_act:
            return False
        
        self.board[ghost_location[1]][ghost_location[0]] -= (ghost_num - 1) * 10
        
        act = random.choice(possible_act)  
        self.locations[ghost_num] = act
        
        if self.board[act[1]][act[0]] // 10 == 7:
            return True
        
        self.board[act[1]][act[0]] += (ghost_num - 1) * 10
        return False

    def move_all_ghosts(self):
        for ghost_num in (2, 3, 4, 5):
            if self.locations[ghost_num] != None and not self.done:
                self.done = self.move_ghost(ghost_num)
    
    def update_board(self, move):
        """Move the gates, the Pacman and than the ghosts, in this order."""
        self.move_gates()
        
        prize = self.move_pacman(move)
        
        self.move_all_ghosts()
        
        if self.done:
            prize -= 10
        elif not self.pellets:
            prize += 10
            self.done = True
        
        return prize

    def play_game(self, policy, visualize = True):
        """Execute given policy, for a given number of steps.
        if Visualize = True, prints all states along execution.
        Returns the reward"""
        reward = 0
        self.done = True
        
        for i in xrange(self.steps):
            if self.done:
                self.reset()
                
            t1 = time.time()
            move = policy.choose_next_move(tuple(tuple(row) for row in self.board))
            t2 = time.time()
            
            if move not in self.actions.keys():
                print "This is wrong!"
            
            reward += self.update_board(self.actions[move])
            
            if visualize:
                print self.board
                print "The choice of the next move took: ", t2 - t1, " seconds."
                               
        return reward

    def evaluate_policy(self, policy, times, visualize = True):
        return sum([self.play_game(policy, visualize) for i in xrange(times) ]) / (1.0 * times)
