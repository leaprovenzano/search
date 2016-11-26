import itertools
from copy import deepcopy
import sys






def simple_csp_search(data, valid, is_goal):
    """Originally written to solve constraint satisfaction
     logic puzzles like zebra puzzle where given a set of 'boxes'
     and a set of rules we need to generate states that only 
     tick one 'box' for each category in order to find out goal. 
     be aware: dumb searcher in that it returns the first value 
     to pass is_goal. so heavy lifiting is done in *valid*
     and *is_goal*. 

    given categorically grouped *data* and set of rules in 
    the form of the *valid* function generates a set of valid 
    states in which each catagorical value from the *data* appears 
    only once. If the set of states is the goal state (as defined 
    in *is_goal* ... obviously) returns that state else, returns 
    None.

    Args:
        data (list): list of equal length lists containing
                     unique values of same catagorical type.

        valid (function): processess a set of rules 
                          (defined within that function) 
                           on a single state object, 
        is_goal (function): a function that returns true
                            if a given state set is goal.

    Returns:
        list (of tuples): list of unique sets with one 
                          value from each category if goal
                          is found.... else None.
    """
    valid_states = [st for st in itertools.product(*data) if valid(st)]
    for state in valid_states:
        states = [state]
        p_states = itertools.ifilterfalse(lambda x: any(
            (any((e in s for e in x)) for s in states)), valid_states)
        while True:
            try:
                states.append(p_states.next())
            except StopIteration:
                break
        if is_goal(states):
            return states
    return None






def grid_heuristic_with_orientation(field, gen_moves, is_goal, cost_function, is_passable):
    """builds heuristic for pathfinding on 2D grid with orientation in 4 directions.
        
    Arguments:
        field {List} -- [a 2D matrix representing the 'world']
        gen_moves {function} -- [a function to generate possible actions]
        is_goal {function} -- [returns True if given x, y is goal]
        cost_function {function} -- [returns cost of a given action]
        is_passable {function} -- [returns True if a given cell is passable]
    
    Returns:
        [list] -- [heuristic for all 4 orientations]
    """
    change = true
    X, Y = len(field), len(field[0])
    value = [[[lambda (x, y): 0 if is_goal(x, y) else sys.maxint for y in range(Y)] 
                                                                    for x in range(X)] for o in range(4)]
    policy =  [deepcopy.copy(field) for o in range(4)];
    while (change):
        change = False
        for x in range(X):
            for y in range(Y):
                if is_passable(policy[0][x][y]):
                    for orient in range(4):
                        moves = getMoves(orient, [x, y])
                        for ori, x2, y2, mv in moves:
                            cost = getCost(mv) + value[orient][x2][y2]
                            if cost < value[orient][x][y]:
                                change = True
                                value[orient][x][y] = cost
                                policy[orient][x][y] = mv
    return policy


