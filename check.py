import pacman
import random
import ex2
import time

def evaluate(board ,steps):    
    """Run solver function on given problem and evaluate it's effectiveness."""
    run_pacman = pacman.Game(steps, board) 

    t1 = time.time()
    controller = ex2.Controller(board, steps)
    t2 = time.time()
    
    print "Controller initialization took: ", t2 - t1, " seconds."
    print "The average score for the problem is:", 
    print run_pacman.evaluate_policy(controller, 30, visualize = False)

def main():
    """Print students id's and run evaluation on a given game"""
    print ex2.ids
    
    game0 = ((20,10,10,99,10),
             (10,10,10,19,45),
             (10,11,10,99,11),
             (10,11,10,89,10),
             (70,15,10,99,11))
    
    evaluate(game0, 100)    


if __name__ == '__main__':
    main()
    

