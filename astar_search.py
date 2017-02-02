# Generic A* Search algorithm
'''
NOTES:
* Insert into heap: heappush(expanded_nodes, node)
* Delete from heap: heappop(expanded_nodes)
* Heap node format: (f, g, state) where f(x) = g(x) + h(x)
* Necessary Functions From State Class:
    * all_next_expansions() # returns all possible actions and their costs
    * is_goal() # true/false if the current state is a goal state
    * heuristic() # returns heuristic score
'''

from heapq import heappush, heappop
import copy

class Astar:
    start_state = None
    expanded_nodes = [] # Use as a Priority Queue based on f(x) = g(x) + h(x)

    def __init__(self, start_state):
        self.start_state = start_state
        heappush(self.expanded_nodes, (0, 0, self.start_state))

    def solve(self):
        achieved_goal = False
        goal_state = None

        # Continuously expand nodes until we expand the goal_state
        while len(self.expanded_nodes) > 0:

            (_, curr_cost, curr_state) = heappop(self.expanded_nodes)

            # Stop once goal node has been found
            if curr_state.is_goal():
                goal_state = curr_state
                break

            self.expand_node(curr_cost, curr_state)

        return goal_state

    def expand_node(self, curr_cost, curr_state):
        # Get All Next States and Add to Heap
        next_states, next_state_costs = curr_state.all_next_expansions()
        for i in xrange(len(next_states)):
            # Calculate costs and heuristics
            g_score = curr_cost + next_state_costs[i]
            f_score = g_score + next_states[i].heuristic()

            # Add to heap
            heappush(self.expanded_nodes, (f_score, g_score, next_states[i]))
