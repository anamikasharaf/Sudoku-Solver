# Sudoku Solver

## Members
* Kumari Anamika Sharaf
* Sarabh Marathe
* William Nguyen

## How to Run
To run the code, all that is needed is to run the Knowledge Base file since it integrates both our A* search algorithm and the Hopfield neural network. To do so, first cd into the directory with the code and run the `KnowledgeBase.py` file.

```
$ cd /path/to/folder
$ python KnowledgeBase.py
```

## Providing Custom Sudoku Board
In the `KnowledgeBase.py` file, we initialize the sudoku problem as a string of digits 0-9. 0 or a period '.' represents an empty cell. To provide your own input, change the `unsolved_input` to a valid sudoku puzzle with only one solution. The `unsolved_inputs` variable is found in the beginning of the `if __name__ == '__main__':` block.

Here is the sudoku puzzle we initially provide.

```
if __name__ == "__main__":
	unsolved_input = "89127456.6.31859..457639...5.641723.7429.381.31..26.5.93854.67.16479.32..7536149."
```

We also provided several other puzzles in the main function. To test these other inputs, please comment out one line and leave all other lines commented out.

## Sample Output
```
Sudoku now solved by A*

This is first iteration of HNN
--------------------

Output board is:-
[8, 9, 1, 2, 7, 4, 5, 6, 3]
[6, 2, 3, 1, 8, 5, 9, 4, 0]
[4, 5, 7, 6, 3, 9, 1, 8, 0]
[5, 8, 6, 4, 1, 7, 2, 3, 9]
[7, 4, 2, 9, 5, 3, 8, 1, 6]
[3, 1, 9, 8, 2, 6, 7, 5, 0]
[9, 3, 8, 5, 4, 2, 6, 7, 1]
[1, 6, 4, 7, 9, 8, 3, 2, 0]
[2, 7, 5, 3, 6, 1, 4, 9, 8]

Neral Network confused about following cells, and their possible values are:-
Cell 1,8 has following possible hints
2 4 7
Cell 2,8 has following possible hints
1 2 8
Cell 5,8 has following possible hints
4 7 9
Cell 7,8 has following possible hints
5 8

The cell chosen is 1,8, with commanilty index as 3
17
x->-1
y->-1

This is 2 iteration
This is a hint provided by A* solution
7 is the value to be put in 1,8
--------------------

Output board is:-
[8, 9, 1, 2, 7, 4, 5, 6, 3]
[6, 2, 3, 1, 8, 5, 9, 4, 7]
[4, 5, 7, 6, 3, 9, 1, 8, 2]
[5, 8, 6, 4, 1, 7, 2, 3, 9]
[7, 4, 2, 9, 5, 3, 8, 1, 6]
[3, 1, 9, 8, 2, 6, 7, 5, 4]
[9, 3, 8, 5, 4, 2, 6, 7, 1]
[1, 6, 4, 7, 9, 8, 3, 2, 5]
[2, 7, 5, 3, 6, 1, 4, 9, 8]

-1
x->0
y->0

Now with hints from A*, HNN was able to solve the sudoku entirely
```