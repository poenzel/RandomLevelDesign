import math 
import random
from tqdm import tqdm
from Grid import Grid


def selection(list_obj_rank, n_top, percentage=True):
    """
    Select the top `n_top` tuples based on their scores.

    Args:
        list_obj_rank (list of tuple): A list of tuples in the form (object, score).
        n_top (int): Number or percentage of top elements to select.
        percentage (bool): If True, treat n_top as a percentage; otherwise, as a number.

    Returns:
        list of tuple: A list containing the top `n_top` tuples.
    """
    # Sort the list by score in descending order
    sorted_list = sorted(list_obj_rank, key=lambda x: x[1], reverse=True)
    
    # Determine the number of top elements to select
    if percentage:
        n = max(1, int(len(sorted_list) * n_top / 100))  # Ensure at least 1 element is selected
    else:
        n = min(n_top, len(sorted_list))  # Avoid selecting more elements than available
    
    if n%2 != 0 :
        n+=1
    # Return the top `n` elements
    return sorted_list[:n]

def random_grid(width, length, valid_values) :
    """
    Generates a random grid of size width x length."""
    grid_str_len = width*length
    grid_str = ''
    for i in range(0, grid_str_len) :
        grid_str += random.choice(valid_values)

    grid = Grid(grid_str, width, length, valid_values)
    return grid

def mutate(grid, mutation_rate):
    """Randomly changes 1 letter in the grid."""
    grid_str = grid.get_grid_str()
    grid_list = list(grid_str)
    valid_values = grid.get_valid_values()
    for i in range(len(grid_str)):
        if random.random() < mutation_rate:
            grid_list[i] = random.choice(valid_values)  # Replace with a random valid value
    grid_str = ''.join(grid_list)
    mutated = Grid(grid_str, grid.get_width(), grid.get_length(), grid.get_valid_values())
    return mutated

def mutate_swap(grid) :
    """Swaps two random letters in the grid."""
    grid_str = grid.get_grid_str()
    grid_list = list(grid_str)
    
    idx1, idx2 = random.sample(range(len(grid_list)), 2)
    
    grid_list[idx1], grid_list[idx2] = grid_list[idx2], grid_list[idx1]
    
    mutated_str = ''.join(grid_list)
    mutated = Grid(mutated_str, grid.get_width(), grid.get_length(), grid.get_valid_values())
    return mutated


def crossover_sequence(grid_a, grid_b):
    """Given two input grids, creates a child grid with substrings of both grids mixed."""
    
    if  not grid_a.is_compatible_with(grid_b):
        print('Error : Incompatible grid parents.')
        return 
     
    a_str = grid_a.get_grid_str()
    b_str = grid_b.get_grid_str()

    len_max = len(a_str)
    offspring_str = ''
    a = True
    for i in range(len_max) :
        c = random.random()
        if c < 0.25 :
            a = not a
        if a :
            offspring_str += a_str[i]
        else :
            offspring_str += b_str[i] 
    
    offspring = Grid(offspring_str, grid_a.get_width(), grid_a.get_length(), grid_a.get_valid_values())

    return offspring


def crossover_row(grid_a, grid_b):
    """Given two input grids, creates a child grid with rows of both grids mixed."""
    if not grid_a.is_compatible_with(grid_b) :
        print('Error : Incompatible grid parents.')
        return
    
    array_a = grid_a.get_rows()
    array_b = grid_b.get_rows()

    offspring_array = [random.choice([a, b]) for a, b in zip(array_a, array_b)]

    offspring_str = ''.join(offspring_array)

    offspring = Grid(offspring_str, grid_a.get_width(), grid_a.get_length(), grid_a.get_valid_values())
    return offspring

def crossover_column(grid_a, grid_b):
    """Given two input grids, creates a child grid with columns of both grids mixed."""
    if not grid_a.is_compatible_with(grid_b) :
        print('Error : Incompatible grid parents.')
        return
    
    array_a = grid_a.get_columns()
    array_b = grid_b.get_columns()

    offspring_array = [random.choice([a, b]) for a, b in zip(array_a, array_b)]

    offspring_str =  ''.join([''.join(col) for col in zip(*offspring_array)])

    offspring = Grid(offspring_str, grid_a.get_width(), grid_a.get_length(), grid_a.get_valid_values())
    return offspring

def crossover_quadrant(grid_a, grid_b):
    """
    Performs a crossover between two grids by combining a dynamically sized section from one grid
    and the rest from the other grid. The section size is constrained to width-1 or smaller.
    """
    grid_a_array = grid_a.get_2d_array()
    grid_b_array = grid_b.get_2d_array()

    width, length = grid_a.get_width(), grid_b.get_length()

    # Determine the maximum section size
    max_section_size = min(length - 1, width - 1)

    # Randomly determine the section size (at least 2x2)
    section_size = random.randint(2, max_section_size)

    # Randomly pick the top-left corner for the section
    x = random.randint(0, length - section_size)
    y = random.randint(0, width - section_size)

    # Create a new grid initialized as a copy of grid2
    offspring_array = [row[:] for row in grid_b_array]

    # Replace the dynamically sized section in the offspring with the section from grid1
    for i in range(section_size):
        for j in range(section_size):
            offspring_array[x + i][y + j] = grid_a_array[x + i][y + j]

    offspring_str = ''.join([''.join(offspring_array[i]) for i in range(len(offspring_array))])

    offspring = Grid(offspring_str, width, length, grid_a.get_valid_values())
    return offspring


def generate_child_grid(grid_a, grid_b, mutation_rate) :
    crossovers = [crossover_sequence, crossover_row, crossover_column, crossover_quadrant]
    crossover_fct = random.choice(crossovers)
    offspring = crossover_fct(grid_a, grid_b)
    offspring = mutate(offspring, mutation_rate)
    additional_mutation_chance = random.random()
    if additional_mutation_chance < mutation_rate :
        offspring = mutate_swap(offspring)
    return offspring


def fitness(grid) :
    grid_str=  grid.get_grid_str()
    if grid_str.count('0') <= 5:
        return 0
    elif  grid_str.count('0') > 5 and  grid_str.count('0') <= 15 :
        return 5
    elif grid_str.count('0') > 15 and  grid_str.count('0') <= 30 :
        return 25
    else :
        return 5         

def genetic_algorithm(width, length, valid_values, n_selection, n_selection_mode, n_best_grid, mutation_rate, fitness_threshold, population_size=100, generations=50):
    # Step 1: Initialize Population
    population = [random_grid(width, length, valid_values) for _ in range(population_size)]
    
    for generation in tqdm(range(generations)):
        # Step 2: Evaluate Fitness

        fitness_scores = [(grid, fitness(grid)) for grid in population]

        # Step 3: Select Parents
        selected_parents = selection(fitness_scores, n_selection, n_selection_mode)

        # Step 4: Crossover
        new_population = [selected[0] for selected in selected_parents]
        for i in range(0, len(selected_parents), 2):
            parent1, parent2 = selected_parents[i][0], selected_parents[i+1][0]
            child1 = generate_child_grid(parent1, parent2, mutation_rate)
            child2 = generate_child_grid(parent2, parent1, mutation_rate)
            new_population.extend([child1, child2])
        

        if generation > 0 :
            remaining_pop_amount = len(fitness_scores)
            
            while len(new_population) < remaining_pop_amount:
                # Randomly select two parents
                parent1, parent2 = random.choice(selected_parents)[0], random.choice(selected_parents)[0]
                
                # Generate children from the selected parents
                child1 = generate_child_grid(parent1, parent2, mutation_rate)
                child2 = generate_child_grid(parent2, parent1, mutation_rate)

                # Add the children to the new population
                new_population.extend([child1, child2])


        # Step 6: Replace Population
        population = new_population
        
        # Step 7: Check Stopping Condition (optional)
        if max(fitness_scores, key=lambda x: x[1])[1] >= fitness_threshold:
            break
    
    # Return the best grid
    # best_index = max(range(len(fitness_scores)), key=lambda i: fitness_scores[i][1])
    top_indices = sorted(range(len(fitness_scores)), key=lambda i: fitness_scores[i][1], reverse=True)

    # Return the top n_bg grids based on the selected indices
    return [population[i] for i in top_indices[:n_best_grid]]




grid1 = 'DDDD00EDDD\nD0E0000E0D\nD000DD0T0D\nD000D0000D\n0D00000D00\n0D0DD00000\nD0000D0T0D\nD00D00000D\nD0B00000BD\nDDDD00DDDD'
grid2 = 'DDDD00EDDDD0E0000E0DD000DD0T0DD000D0000D0D00000D000D0DD00000D0000D0T0DD00D00000DD0B00000BDDDDD00DDDD'

valid_values = ['D','T','0']

# print(grid1)
# print("#################################")
# print_grid(grid2, 10, 7)
# print(grid_to_2d_array(grid2,10,10))
# print(grid1)
test = [('A',4),('B',2),('C',5),('D',10),('E',6),('F',2),('G',1),('H',7)]

w = 6
l = 6
# gridA = random_grid(w,l,valid_values)
# gridB = random_grid(w,l,valid_values)
# gridC = crossover_quadrant(gridA, gridB)
# print(gridA)
# print('XXXXXXXXXXXXXXXXXXXXX')
# print(gridB)
# print('XXXXXXXXXXXXXXXXXXXXX')
# print(gridC)

pop = genetic_algorithm(w,l, valid_values, 50, True, 5,0.1, 50, population_size=200, generations=500)
print('Displaying the best grids :')
for p in pop :
    print(p)
    print('#############################')