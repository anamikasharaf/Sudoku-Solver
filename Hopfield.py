import numpy as np

class Hopfield_Neuron:
  input=0.0
  output=0.0
  energy=0.0
  prev_energy=0.0
  alpha=1.0 # alpha is put to 1, because this neural network linearly transfers the energy to the output
  i=0
  j=0
  k=0

  #constructor to initialize values for each neuron
  def __init__(self, i, j, k, cell_value):
    self.i = i
    self.j = j
    self.k = k
    self.input = cell_value

  def energy_function(self,output_for_each_neuron):
    self.prev_energy=self.energy

    i = self.i
    j = self.j
    k = self.k
    temp = 0.0
    temp2 = 0.0

    # First term of the input
    temp= temp + self.input

    # Second term of the input
    for i2 in range(0,9):
      if(i2!=i):
        temp2 = temp2 + output_for_each_neuron[i2][j][k]
    for j2 in range(0,9):
      if(j2!=j):
        temp2 = temp2 + output_for_each_neuron[i][j2][k]
    for k2 in range(0,9):
      if(k2!=k):
        temp2 = temp2 + output_for_each_neuron[i][j][k2]

    box_num = (int)(i/3) * 3 + (int)(j/3)
    r_start = (int)(box_num/3) * 3
    c_start = (box_num%3) * 3
    for i2 in range(r_start,r_start+3):
      for j2 in range(c_start,c_start+3):
          if(i2!=i or j2!=j): # Do not consider cells considered in previous for loops
            temp2=temp2 + output_for_each_neuron[i2][j2][k]

    #calculate total energy for each neuron
    self.energy=temp + self.alpha * temp2
    self.output=self.energy
    return self.energy


class Hopfield_Network:
  sudoku_board=[[[0] * 9 for _ in xrange(9)]for _ in xrange(9)] # Initialize 9x9x9 matrix full of zeros
  output_for_each_neuron=[[[0] * 9 for _ in xrange(9)]for _ in xrange(9)] # Initialize 9x9x9 matrix full of zeros
  hints=[[[0] * 10 for _ in xrange(9)]for _ in xrange(9)] #initialize 9x9 matrix full of zeroes
  cell_change = [0]*81
  def __init__(self, sudoku_input_board):
    self.sudoku_board=[[[0] * 9 for _ in xrange(9)]for _ in xrange(9)]
    self.output_for_each_neuron=[[[0] * 9 for _ in xrange(9)]for _ in xrange(9)]
    self.hints=[[[0] * 10 for _ in xrange(9)]for _ in xrange(9)]
    self.cell_change = [0]*81
    # Set sudoku_board with values 0 or 1 given input board
    for i in range(0,9):
      for j in range(0,9):
        value = sudoku_input_board[i][j]
        if(value!=0):
          self.sudoku_board[i][j][value-1]=1

    # Generate array of Hopfield_Neuron objects
    self.hn = []
    self.energy_update=[]
    for i in range(0,9):
      for j in range(0,9):
        for k in range(0,9):
          self.hn.append(Hopfield_Neuron(i, j, k, self.sudoku_board[i][j][k]))
          self.energy_update.append(0.0)


  def energy_update_func(self):
    # Find and store gain difference for each neuron
    for i in range(0,729):
      self.energy_update[i]=self.hn[i].energy_function(self.output_for_each_neuron) - self.hn[i].prev_energy
      #please uncomment this code below to see energy changes for each neuron
      #if self.energy_update[i]==1:
      #    a=i/81
      #    b=(i-a*81)/9
      #    print "----->>>  %d,%d has energy update as 1"%(a,b)

    for i in range(0,9):
      for j in range(0,9):
        for k in range(0,9):
          index = (i*81) + (j*9) + k
          self.output_for_each_neuron[i][j][k]=self.hn[index].output

  def run_neural_nw(self):
    # Network continues running if at least one neuron's gain is 0
    # first iteration of energy_update_func to initialize output for each neuron to its default input
    self.energy_update_func()
    # second iteration of energy_update_func to calulate and update input to each neuron from other neurons in the domain
    self.energy_update_func()
    # search function finds the value(s) that each cell can have
    self.search()
    return self


  def search(self):
    for i in range(0,9):
    	for j in range(0,9):
            value_to_put=0
            for k in range(0,9):
        	if self.energy_update[((i*81)+(j*9)+k)]<1: # Get k with min energy
                    value_to_put=k
                    #print "Value %d should be put in cell %d, %d" % (value_to_put+1,i,j)
                    self.hints[i][j][k+1]=1

  def update_sudoku_board(self):
    for i in range(0,9):
   	for j in range(0,9):
      		count = 0
      		temp=-1
      		for k in range(0,10):
     			if (self.hints[i][j][k] == 1):
    				count = count + 1
    				temp=k
                if count==1:
                    self.sudoku_board[i][j][temp-1]=1
    print "--------------------"
