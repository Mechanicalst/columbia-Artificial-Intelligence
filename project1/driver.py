# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 15:10:47 2019

@author: joye
"""

import queue
import time
#import resource
import sys
import math
#### SKELETON CODE ####

## The Class that Represents the Puzzle

class PuzzleState(object):
    """docstring for PuzzleState"""
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        if n*n != len(config) or n < 2:
            raise Exception("the length of config is not correct!")
        self.n = n
        self.cost = cost
        #self.depth = depth
        self.parent = parent
        self.action = action
        self.dimension = n
        self.config = config
        self.children = []
        for i, item in enumerate(self.config):
            if item == 0:
                self.blank_row = i // self.n
                self.blank_col = i % self.n
                break
    def display(self):
        for i in range(self.n):
            line = []
            offset = i * self.n
            for j in range(self.n):
                line.append(self.config[offset + j])
            print(line)

    def move_left(self):
        if self.blank_col == 0:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index - 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Left", cost=self.cost + 1)

    def move_right(self):
        if self.blank_col == self.n - 1:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index + 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Right", cost=self.cost + 1)

    def move_up(self):
        if self.blank_row == 0:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index - self.n
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Up", cost=self.cost + 1)

    def move_down(self):
        if self.blank_row == self.n - 1:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index + self.n
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Down", cost=self.cost + 1)

    def astarcmp(self, other_state):
        action_priority = {"Up" : 0, "Down" : 1, "Left" : 2, "Right" : 3}
        if calculate_total_cost(self) < calculate_total_cost(other_state):
            return -1
        elif calculate_total_cost(self) > calculate_total_cost(other_state):
            return 1
        else:
            return action_priority[self.action] < action_priority[other_state.action]
        
    def __lt__(self, other_state):
        '''
        used in astar
        '''
        return self.astarcmp(other_state) < 0
        
    def __gt__(self, other_state):
        return self.astarcmp(other_state) > 0
    
    #def __eq__(self, other_state):
    #    return self.astarcmp(other_state) == 0
    
    #def __le__(self, other_state):
    #    return self.astarcmp(other_state) <= 0
   
    #def __ge__(self, other_state):
    #    return self.astarcmp(other_state) >= 0
     
    #def __ne__(self, other_state):
    #    return self.astarcmp(other_state) != 0
    
    def expand(self):
        """expand the node"""
        # add child nodes in order of UDLR
        if len(self.children) == 0:
            up_child = self.move_up()
            if up_child is not None:
                self.children.append(up_child)
            down_child = self.move_down()
            if down_child is not None:
                self.children.append(down_child)
            left_child = self.move_left()
            if left_child is not None:
                self.children.append(left_child)
            right_child = self.move_right()
            if right_child is not None:
                self.children.append(right_child)
        return self.children        
        
# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters
class Frontier(object):
    def __init__(self, state, container_class):
        self.explored = set()
        self.container = container_class()
        self.container.put(state)
        self.explored.add(state.config)
        pass
    
    def push(self, children_states):
        for child in children_states:
            if child.config in self.explored:
                continue
            else:
                self.explored.add(child.config)
                self.container.put(child)
                
    def isEmpty(self):
        return self.container.empty()
    
    def pop(self):
        return self.container.get()

class BFS_Frontier(Frontier):
    def __init__(self, state):
        Frontier.__init__(self, state, queue.Queue)
    
    #def pop(self):
    #    return Frontier.pop(self)
        #frontier_to_pop = self.container[0]
        #self.container = self.container[1:]
        #return frontier_to_pop

class DFS_Frontier(Frontier):
    def __init__(self, state):
        Frontier.__init__(self, state, queue.LifoQueue)
        
    def push(self, children_states):
        '''
        need to push in reverse-UDLR order, and pop off the result in UDLR order
        '''
        reversed_states = reversed(children_states)
        Frontier.push(self, reversed_states)

class Astar_Frontier(Frontier):
    def __init__(self, state):
        Frontier.__init__(self, state, queue.PriorityQueue)
        
 
def writeOutput(result_state, search_depth, max_search_depth, expanded_node, running_time):
    ### Student Code Goes here
    cost_of_path = result_state.cost
    path_to_goal = []
    while result_state.parent != None:
        path_to_goal.insert(0, result_state.action)
        result_state = result_state.parent
    max_ram_usage = 0.0
    if sys.platform == "win32":
        import psutil
        max_ram_usage = psutil.Process().memory_info().rss
    else:
        import resource
        max_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    write_file = open("output.txt", 'w+')
    print("path_to_goal: " + str(path_to_goal), file = write_file)
    print("cost_of_path: %d" % (cost_of_path), file = write_file)
    print("nodes_expanded: %d" % (expanded_node), file = write_file)
    print("search_depth: %d" % (search_depth), file = write_file)
    print("max_search_depth: %d" % (max_search_depth), file = write_file)
    print("running_time: %f" % (running_time), file = write_file)
    print("max_ram_usage: %f" % (max_ram_usage), file = write_file)
    write_file.close()
        
def bfs_search(initial_state):
    """BFS search"""
    ### STUDENT CODE GOES HERE ###
    start_time = time.time()
    #max_search_depth = 0
    search_depth = 0
    nodes_expanded = 0
    frontier = BFS_Frontier(initial_state)
    while not frontier.isEmpty():
        state = frontier.pop()    
        if test_goal(state):  
            search_depth = state.cost
            writeOutput(state, search_depth, search_depth+1, nodes_expanded, time.time()-start_time)
            return
        else:
            nodes_expanded += 1
            expand_children = state.expand()     
            frontier.push(expand_children)
    
def dfs_search(initial_state):
    """DFS search"""
    ### STUDENT CODE GOES HERE ###
    start_time = time.time()
    max_search_depth = 0
    nodes_expanded = 0
    frontier = DFS_Frontier(initial_state)
    while not frontier.isEmpty():
        state = frontier.pop()
        max_search_depth = max(max_search_depth, state.cost)
        if test_goal(state):
            search_depth = state.cost
            writeOutput(state, search_depth, max_search_depth, nodes_expanded, time.time() - start_time)
            return
        else:
            nodes_expanded += 1
            expand_children = state.expand()
            frontier.push(expand_children)
            
def A_star_search(initial_state):
    """A * search"""
    ### STUDENT CODE GOES HERE ###
    start_time = time.time()
    max_search_depth = 0
    nodes_expanded = 0
    frontier = Astar_Frontier(initial_state)
    while not frontier.isEmpty():
        state = frontier.pop()
        max_search_depth = max(max_search_depth, state.cost)
        if test_goal(state):
            search_depth = state.cost
            writeOutput(state, search_depth, max_search_depth, nodes_expanded, time.time() - start_time)
            return
        else:
            nodes_expanded += 1
            expand_children = state.expand()
            frontier.push(expand_children)
    
def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    ### STUDENT CODE GOES HERE ###
    return state.cost + sum([calculate_manhattan_dist(index, conf, state.n) for index, conf in enumerate(state.config)])

def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    ### STUDENT CODE GOES HERE ###
    row = idx // n
    col = idx % n
    target_row = value // n
    target_col = value % n
    return abs(row - target_row) + abs(col - target_col)

def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    ### STUDENT CODE GOES HERE ###
    golden_config = tuple([i for i in range(len(puzzle_state.config))])
    #print(puzzle_state.config)
    return puzzle_state.config == golden_config 
    
    
# Main Function that reads in Input and Runs corresponding Algorithm

def main():
    sm = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = tuple(map(int, begin_state))
    size = int(math.sqrt(len(begin_state)))
    hard_state = PuzzleState(begin_state, size)
    if sm == "bfs":
        bfs_search(hard_state)
    elif sm == "dfs":
        dfs_search(hard_state)
    elif sm == "ast":
        A_star_search(hard_state)
    else:
        print("Enter valid command arguments !")

if __name__ == '__main__':
    main()