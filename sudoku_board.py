import pdb
class Sudoku:
    def __init__(self):
        self.set_defaults()

    def __init__(self, start):
        self.set_defaults()
        for i in xrange(81):
            c = start[i]
            if not c == '.':
                self.board[i] = int(c)

                # Remove value from hints row-, col-, and box-wise
                self.remove_hints(int(i / 9), int(i % 9), int(c))
                if not self.is_valid():
                    raise Exception("Input Sudoku board is invalid.")

    def set_defaults(self):
        self.board = [0] * 81
        self.hints = []
        for i in range(81):
            self.hints.append(set(range(1,10)))

    def remove_hints(self, i, j, value):
        # Empty the hints set for cell (i,j)
        self.hints[i*9+j].clear()

        # Remove hints from cells in Row
        for c in xrange(9):
            index = i * 9 + c
            self.hints[index].discard(value)

        # Remove hints from cells in Col
        for r in xrange(9):
            index = r * 9 + j
            self.hints[index].discard(value)

        # Remove hints from cells in Box
        r_start = int(i / 3) * 3
        c_start = int(j / 3) * 3
        r_end = r_start + 3
        c_end = c_start + 3

        for r in xrange(r_start, r_end):
            for c in xrange(c_start, c_end):
                index = r * 9 + c
                self.hints[index].discard(value)

    def get_element(self, i, j):
        index = i * 9 + j
        return self.board[index]

    def get_hints(self, i, j):
        index = i * 9 + j
        return self.hints[index]

    def update_element(self, i, j, value):
        index = i * 9 + j

        # Value can only be from 1 - 9
        # Possible exception: 0 if we want to reset a board space
        if not self.board[index] == 0:
            raise Exception("Cell (%s, %s) already has a value." % (i, j))
        elif value < 0 or value > 9:
            raise Exception("Sudoku boards can only accept values 0-9.")

        # Check if value is in hint set
        if value not in self.hints[index]:
            return False

        # Update value and Check
        # Reset value if the board becomes invalid, otherwise remove hints
        self.board[index] = value
        if not self.is_valid():
            self.board[index] = 0
            return False
        self.remove_hints(i, j, value)

        return True

    def all_empty_cells(self):
        # Returns a list of indicies of empty cells
        return filter(lambda x: self.board[x] == 0, xrange(81))

    def next_best_cell_to_fill(self):
        # Custom comparator for reduce
        def fewer_hints(x,y):
            if len(self.hints[x]) <= len(self.hints[y]):
                return x
            return y

        # Of all empty cells, find the cell with the least hints
        empty_cells = self.all_empty_cells()
        if len(empty_cells) >0:
            return reduce(lambda x,y: fewer_hints(x,y), empty_cells)
        else:
            return None

    def is_valid(self):
        # An invalid board results in a cell with no hints
        for i in xrange(81):
            if self.board[i] == 0 and len(self.hints[i]) == 0:
                return False

        # An invalid board has conflicts
        # Check Row:
        for r in xrange(9):
            has_val = [False] * 10 # 10 because 0 is also a possible digit
            for c in xrange(9):
                index = r * 9 + c
                if self.board[index] != 0 and has_val[self.board[index]]:
                    return False
                has_val[self.board[index]] = True

        # Check Col:
        for c in xrange(9):
            has_val = [False] * 10
            for r in xrange(9):
                index = r * 9 + c
                if self.board[index] != 0 and has_val[self.board[index]]:
                    return False
                has_val[self.board[index]] = True


        # Check Box:
        for b in xrange(9):
            has_val = [False] * 10

            r_start = int(b / 3) * 3
            c_start = int(b % 3) * 3
            r_end = r_start + 3
            c_end = c_start + 3

            for r in xrange(r_start, r_end):
                for c in xrange(c_start, c_end):
                    index = r * 9 + c
                    if self.board[index] != 0 and has_val[self.board[index]]:
                        return False
                    has_val[self.board[index]] = True

        return True

    def is_solved(self):
        return len(self.all_empty_cells()) == 0 and self.is_valid() == True

    def cost_to_fill(self, i, j):
        # Cost is the amount of hints for the cell to be filled
        index = i * 9 + j
        return len(self.hints[index])

    def heuristic(self):
        # Heuristic used is amount of hints left
        h_total = sum(list(map(lambda x: len(x), self.hints)))
        return h_total

    def print_board(self, mode=0):
        # Modes:
        # 0 - 9x9 board
        # 1 - 1x81 board
        if mode == 0:
            for r in xrange(9):
                print(self.board[r*9:(r+1)*9])
        else:
            print(self.board)

def main():
    # Test the Sudoku class' methods
    unsolved_input = "572138.4.4.6.59817....67..2.43725..61.5.43728..96.13.43.7.14..5218.9.473.54.72..1"
    solved_input   = "572138649436259817981467532843725196165943728729681354397814265218596473654372981"
    invalid_input  = "572138849436259817981467532843725196165943728729681354397814265218596473654372981"
    unsolved_board = Sudoku(unsolved_input)

    assert unsolved_board.get_element(0,0) is 5, "get_element error"
    print(unsolved_board.all_empty_cells() == list(filter(lambda x: unsolved_input[x] == '.', xrange(81))))
    print(unsolved_board.is_valid() == True)
    print(unsolved_board.get_hints(0, 6))
    print(unsolved_board.cost_to_fill(0, 6))
    print(unsolved_board.heuristic())
    print(unsolved_board.update_element(0, 6, 8) == False)
    print(unsolved_board.update_element(0, 6, 6) == True)
    print(unsolved_board.heuristic())

    try:
        unsolved_board.update_element(0,0,1)
    except Exception as e:
        print(e)
    try:
        unsolved_board.update_element(0,8,10)
    except Exception as e:
        print(e)

    for i in unsolved_board.all_empty_cells():
        r = int(i / 9)
        c = int(i % 9)
        unsolved_board.update_element(r, c, int(solved_input[i]))
    print(unsolved_board.heuristic())

    try:
        invalid_board = Sudoku(invalid_input)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
