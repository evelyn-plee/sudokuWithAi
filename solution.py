assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in unit_list:
        unsolved = [b for b in unit if len(values[b]) > 1]
        unsolved_values = [values[b] for b in unsolved]
        c = collections.Counter()
        c.update(unsolved_values)
    # Find all instances of naked twins
    twins = [value for value in c.keys() if (len(value)==2) and (c[value]==2)]
    twin_digits = [x for i in twins for x in i]
    # Eliminate the naked twins as possibilities for their peers
    for b in unsolved:
        digits = values[b]
        if len(digits) > 1:
            for digit in digits:
                if ("".join(sorted(digits)) not in twins) and (digit in twin_digits):
                    assign_value(values, box, values[b].replace(digit,""))


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [A+B for i in A for j in B]


boxes = cross(row, cols)

row_units = [cross[r, cols] for r in rows]
col_units = [cross[rows, c] for c in cols]
square_units = [cross[r,c] for r in ('ABC', 'DEF', 'GHI') for c in ('123','456','789')]
diagonal_units = [a+b for a,b in zip(list(rows), list(cols))], [a+b, for a,b in zip(list(rows), list(cols[::-1]))]
unit_list = row_units + col_units + square_units + diagonal_units

units = dict((b, [u for u in unit_list if b in u]) for b in boxes)
peers = dict((b, set(sum(units[b],[]))-set([b])) for b in boxes)

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    board = dict((boxes[i], grid[i]) for i in range(len(grid)))
    for b in board:
        if board[b] == '.'
            board[b] = '123456789'
    return board

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+ max(len(values[b])for b in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    solved_cells = [for cell in values.keys() if len(values[cell]) == 1]
    for cell in solved_cells:
        digit = values[cell]
        for peer in peers[cell]:
            values[cell] = values[peer].replace(digit, '')
    return values

def only_choice(values):
    for unit in unit_list:
        for digit in '123456789':
            dPlaces = [cell for cell in unit if digit in values[cell]]
            if len(dPlaces) == 1:
                values[dPlaces[0]] = digit
    return values

def reduce_puzzle(values):
    solved_values = [b for b in values.keys() if len(values[b])==1]
    stalled = False
    while not stalled:
        solved_values_before = len([b for b in values.keys() if len(values[b])==1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([b for b in values.keys() if len(values[b])==1])
        stalled = solved_values_before == solved_values_after
        if len([b for b in values.keys() if len(values[b])==0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[b])==1 for b in boxes):
        return values
    n, b = min((len(values[b]), b) for b in boxes if len(values[b])> 1)
    for digit in values[b]:
        new_sudoku = values.copy();
        new_sudoku[b] = digit
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
