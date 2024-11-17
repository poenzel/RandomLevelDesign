import math
import random

def print_grid(grid, width, length) : 
    grid_str_len = len(grid)
    i = 1
    temp_grid = grid[0:width]
    while i < grid_str_len/width :
        temp_grid = temp_grid + '\n' + grid[width*(i):width*(i+1)]
        i+=1
    
    grid_array = temp_grid.split('\n')
    if len(grid_array[-1])!= width :
        print('Error : Width not compatible with string format.')
    else :
        print(temp_grid)


def grid_to_rows(grid,width):
    """ Returns an array containing the rows of the grid. """
    grid_str_len = len(grid)
    grid_array = [grid[width*(i):width*(i+1)] for i in range(0,int(math.ceil(grid_str_len/width)))]
    return grid_array

def grid_to_columns(grid, width, length):
    """ Returns an array containing the columns of the grid. """
    grid_str_len = len(grid)
    grid_array = [''.join([grid[j*width+i] for j in range(0,length)]) for i in range(0, width)]
    return grid_array

def grid_to_2d_array(grid, width, length) :
    """ Returns a 2d-array containing each item in the grid. """
    return [list(grid[i * width: (i + 1) * width]) for i in range(length)]



def swap_random_letters(grid):
    """
    Swaps two random letters in the given string.

    Args:
        grid (str): The input string.

    Returns:
        str: A new string with two letters swapped.
    """
    # Convert string to a list to allow modifications
    grid_list = list(grid)
    
    # Get two unique random indices
    idx1, idx2 = random.sample(range(len(grid_list)), 2)
    
    # Swap the letters at the chosen indices
    grid_list[idx1], grid_list[idx2] = grid_list[idx2], grid_list[idx1]
    
    # Convert list back to string and return
    return ''.join(grid_list)

# print(swap_random_letters('AABBEEZEBLOOP'))
a = True 
a = not a
print("[['T', 'T', 'T', 'D', 'D', '0'], ['T', 'T', 'D', 'T', 'T', 'D'], ['T', '0', '0', '0', '0', 'D'], ['T', 'D', 'T', '0', '0', 'T'], ['T', 'T', 'T', '0', '0', 'D'], ['T', 'D', 'T', 'D', '0', 'D']]")
test = [['T', 'T', 'T', 'D', 'D', '0'], ['T', 'T', 'D', 'T', 'T', 'D'], ['T', '0', '0', '0', '0', 'D'], ['T', 'D', 'T', '0', '0', 'T'], ['T', 'T', 'T', '0', '0', 'D'], ['T', 'D', 'T', 'D', '0', 'D']]
print(''.join([''.join(test[i]) for i in range(len(test))]))