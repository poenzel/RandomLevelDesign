import math
import random

class Grid :
    def __init__(self, grid, width, length, valid_values) :
        self.grid = grid
        self.width = width
        self.length = length
        self.valid_values = valid_values
        
    def __str__(self):
        grid_str_len = len(self.grid)
        i = 1
        temp_grid = self.grid[0:self.width]
        while i < grid_str_len/self.width :
            temp_grid = temp_grid + '\n' + self.grid[self.width*(i):self.width*(i+1)]
            i+=1
        
        grid_array = temp_grid.split('\n')
        if len(grid_array[-1])!= self.width :
            print('Error : Width not compatible with string format.')
        else :
            return temp_grid
    
    def get_grid_str(self):
        return self.grid

    def get_width(self):
        return self.width
    
    def get_length(self):
        return self.length
    
    def get_valid_values(self):
        return self.valid_values

    def is_compatible_with(self, other):
        return (
            self.get_width() == other.get_width() and
            self.get_length() == other.get_length() and
            self.get_valid_values() == other.get_valid_values()
        )
    
    def get_rows(self):
        """ Returns an array containing the rows of the grid. """
        grid_str_len = len(self.grid)
        grid_array = [self.grid[self.width*(i):self.width*(i+1)] for i in range(0,int(math.ceil(grid_str_len/self.width)))]
        return grid_array

    def get_columns(self):
        """ Returns an array containing the columns of the grid. """
        grid_str_len = len(self.grid)
        grid_array = [''.join([self.grid[j*self.width+i] for j in range(0,self.length)]) for i in range(0, self.width)]
        return grid_array

    def get_2d_array(self):
        """ Returns a 2d-array containing each item in the grid. """
        return [list(self.grid[i * self.width: (i + 1) * self.width]) for i in range(self.length)]
