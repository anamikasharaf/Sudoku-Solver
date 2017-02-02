from sudoku_board import Sudoku
import copy, time
from astar_search import Astar

class Sudoku_astar:
    board = None

    def __init__(self, start_board):
        self.board = start_board

    def all_next_expansions(self):
        all_expansions = []
        expansion_costs = []

        # Determine index to fill
        index = self.board.next_best_cell_to_fill()
        if index == None:
            return [], []
        r = int(index / 9)
        c = int(index % 9)

        # Fill with a hint value and see if board is still valid to expand on
        hints = self.board.get_hints(r,c)
        cost = self.board.cost_to_fill(r,c)
        for hint in hints:
            new_astar = copy.deepcopy(self)
            new_board = new_astar.board
            # Only add new state if it is valid
            if new_board.update_element(r, c, hint):
                all_expansions.append(new_astar)
                expansion_costs.append(cost)

        return all_expansions, expansion_costs

    def is_goal(self):
        return self.board.is_solved()

    def heuristic(self):
        return self.board.heuristic()
        # return 1

# def main():
#     ## EASY SUDOKU
#     # unsolved_input = "572138.4.4.6.59817....67..2.43725..61.5.43728..96.13.43.7.14..5218.9.473.54.72..1"
#     # solved_input   = "572138649436259817981467532843725196165943728729681354397814265218596473654372981"
#     ## HARD SUDOKU
#     # unsolved_input = ".......37.4.8......2......65..9..1..7........3.6..5..................91.....37..."
#     # solved_input = "165492837943876521827351496582963174794218365316745289431689752678524913259137648"
#     # unsolved_input = "..62.8...3......4..........4...7.1..........2.5..3.6.8.......9.....5......86....."
#     unsolved_input = "......5......2...79.3.1....4857.....3....8.6....5......7......2..9...4......4..3."



#     start_board = Sudoku(unsolved_input)
#     astar_start = Sudoku_astar(start_board)
#     my_astar = Astar(astar_start)

#     start_time = time.time()
#     pdb.set_trace()
#     solution = my_astar.solve()
#     return_output_astar = solution.board.get_element(i,j)
#     end_time = time.time()

#     print("Solving took %d seconds" % (end_time - start_time))
#     if solution != None:
#         solution.board.print_board()
#     else:
#         print("No solution found")

# if __name__ == "__main__":
#     main()
