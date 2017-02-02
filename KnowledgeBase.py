from __future__ import with_statement
import time
import contextlib
from sudoku_astar import Sudoku_astar
from sudoku_board import Sudoku
from astar_search import Astar
from Hopfield import Hopfield_Network, Hopfield_Neuron
from pyke import knowledge_engine, krb_traceback, goal

def get_output_astar(unsolved_input):
    output_string = [0]*81

    for i in xrange(81):
            c = unsolved_input[i]
            if not c == '.':
                output_string[i] = int(c)

    start_board = Sudoku(unsolved_input)
    astar_start = Sudoku_astar(start_board)
    my_astar = Astar(astar_start)


    solution = my_astar.solve()

    if solution != None:
        output_astar = ''.join(map(lambda x: str( x ), solution.board.board))
        print "Sudoku now solved by A*"
        print ""
    	return solution

    else:
        print("No solution found")

def get_output_HNN(input,index_HNN,sudoku_puzzle):

  if (input == -1):
	  print ("This is first iteration of HNN")
  elif(input > 0):
  	sudoku_puzzle[index_HNN/9][index_HNN%9] = input


  # Create Sudoku AI and run it
  Sudoku_AI = Hopfield_Network(sudoku_puzzle)

  Hopfield_Nw=Sudoku_AI.run_neural_nw()

  Sudoku_AI.update_sudoku_board()

  cell_change = [0]*81
  cell_req_help=[]
  cell_with_highest_commonality=-1
  for i in range(0,9):
  	for j in range(0,9):
  		count = 0
  		for k in range(0,10):
  			if (Hopfield_Nw.hints[i][j][k] == 1):
  				count = count + 1
  		cell_change[i*9+j%9] = count

  print ""
 # print cell_change

  print "Output board is:-"
  for i in range(0,9):
      for j in range(0,9):
          for k in range(0,9):
              if(Hopfield_Nw.sudoku_board[i][j][k]==1 and cell_change[i*9+j%9]==1):
                  sudoku_puzzle[i][j]=k+1
  for r in sudoku_puzzle:
	        	print r
  print ""

  index = -1
  count2=0
  for i in range(0,81):
 	if (cell_change[i] > 1):
 		index = i
 		cell_req_help.append(i)
 		count2=count2+1

  if (index!=-1):
    print  "Neural Network confused about following cells, and their possible values are:"
    for i in range(0,count2):
        print "Cell %d,%d has following possible hints"%(cell_req_help[i]/9,cell_req_help[i]%9)
        for k in range(0,10):
            if (Hopfield_Nw.hints[cell_req_help[i]/9][cell_req_help[i]%9][k]==1):
                print k,
        print ""
    print  ""


  #code to find cell with highest commonality index
  index2=0
  index3=0
  counter=0
  temp=-1
  for i in range(0,count2):
       	index2=cell_req_help[i]
       	a=index2/9
       	b=index2%9
       	for j in range(0,count2):
       	    if i!=j:
       	        index3=cell_req_help[j]
       	        a2=index3/9
       	        b2=index3%9
       	        for k in range(0,10):
       	            if(Hopfield_Nw.hints[a][b][k]==Hopfield_Nw.hints[a2][b2][k] and Hopfield_Nw.hints[a][b][k]==1):
       	                counter=counter+1
       	if(counter>temp):
       	    cell_with_highest_commonality=index2
       	    temp=counter
       	counter=0

  if(cell_with_highest_commonality!=-1):
    print "The cell chosen is %d,%d, with commonality index as %d"%(cell_with_highest_commonality/9,cell_with_highest_commonality%9,temp)

  return cell_with_highest_commonality

if __name__ == "__main__":
    engine = knowledge_engine.engine(__file__)

    fc_goal = goal.compile('sudoku.status($iteration, $status_value)')

    ## These are the EASY SUDOKU puzzles
    unsolved_input = "89127456.6.31859..457639...5.641723.7429.381.31..26.5.93854.67.16479.32..7536149."
    # unsolved_input = "572138.4.4.6.59817....67..2.43725..61.5.43728..96.13.43.7.14..5218.9.473.54.72..1"
    # unsolved_input = "49.63..58.6.28...91....74.3.5.4..68..4.8693753..7.592.875.9...6..4576.32.321.8597"
    # unsolved_input = "..5.397.6.976851..6.2..45....35..47.2..86.931718.9326.53674.82..71.2.3..4.9.58617"

    ## These are the HARD SUDOKU puzzles
    # unsolved_input = ".......37.4.8......2......65..9..1..7........3.6..5..................91.....37..."
    # unsolved_input = "..62.8...3......4..........4...7.1..........2.5..3.6.8.......9.....5......86....."
    # unsolved_input = "......5......2...79.3.1....4857.....3....8.6....5......7......2..9...4......4..3."

    # This code creates a sudoku puxxle similar to the commented-out sudoku_puzzle found below
    sudoku_puzzle = []
    for r in xrange(9):
        new_row = []
        for c in xrange(9):
            index = r*9 + c
            digit = unsolved_input[index]
            if digit == '.':
                digit = 0
            new_row.append(int(digit))
        sudoku_puzzle.append(new_row)

    # sudoku_puzzle = [
    #     [8,9,1,2,7,4,5,6,0], # Simple sudoku board with 66 cells filled and 15 cells empty
    #     [6,0,3,1,8,5,9,0,0],
    #     [4,5,7,6,3,9,0,0,0],
    #     [5,0,6,4,1,7,2,3,0],
    #     [7,4,2,9,0,3,8,1,0],
    #     [3,1,0,0,2,6,0,5,0],
    #     [9,3,8,5,4,0,6,7,0],
    #     [1,6,4,7,9,0,3,2,0],
    #     [0,7,5,3,6,1,4,9,0]
    #   ]

    solution= get_output_astar(unsolved_input)
    index_HNN = get_output_HNN(-1,-1,sudoku_puzzle)

    count = 1

    filled_cells = 0
    for r in sudoku_puzzle:
        for c in r:
            if c != 0:
                filled_cells = filled_cells + 1

    engine.add_universal_fact('sudoku', 'sudoku_solved', (count, filled_cells, 81))

    engine.reset()
    engine.activate('sudoku_rb')
    with fc_goal.prove(engine, iteration=count) as gen:
        for vars,plan in gen:
            x=vars['status_value']
    print "x->%s"%x
    y=int(x)
    print "y->%d"%y

    count=2
    while (y==-1):
        print ""
        print "This is %d iteration"%(count)
        value_return = solution.board.get_element(index_HNN/9,index_HNN%9)
        print "This is a hint provided by A* solution"
        print ("%d is the value to be put in %d,%d"%(value_return,index_HNN/9,index_HNN%9))
        index_HNN = get_output_HNN(value_return,index_HNN,sudoku_puzzle)

        filled_cells = 0
        for r in sudoku_puzzle:
            for c in r:
                if c != 0:
                    filled_cells = filled_cells + 1

        engine.add_universal_fact('sudoku', 'sudoku_solved', (count, filled_cells, 81))

        engine.reset()
        engine.activate('sudoku_rb')
        with fc_goal.prove(engine, iteration=count) as gen:
            for vars,plan in gen:
                x=vars['status_value']
        print "x->%s"%x
        y=int(x)
        print "y->%d"%y

        count = count + 1

    print ""
    print "Now with hints from A*, HNN was able to solve the sudoku entirely"
    print ""
