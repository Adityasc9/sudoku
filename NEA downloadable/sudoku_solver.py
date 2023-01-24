'''Sudoku Solver'''


def find_0(board):  # finds all the empty cells in the 2d array
    for i in range(len(board)):  # for every row in the board
        for j in range(9):  # for every column in every row
            if board[i][j] == 0:  # if the cell is empty, return the coordinates of the cell.
                return i, j

    return None  # if there are no more empty cells, return None


def check_valid(bo, number, pos):  # check if a number in a cell is valid based on sudoku rules

    # checks to see if the number is repeated again on the same row
    for i in range(9):  # for every cell in the same row
        if bo[pos[0]][i] == number and pos[1] != i:  # if the cell is equal to the number to input and the position of the cell is not the same as the position of the number to input, return False as it breaks a rule of soduku
            return False

    # checks to see if the number is repeated again in the same column
    for i in range(9):  # for every cell in same column
        if bo[i][pos[1]] == number and pos[0] != i:  # if the cell is equal to the number to input and the position of the cell is not the same as the position of the number to input, return False as it breaks a rule of sudoku
            return False

    # checks the 3x3 square
    box_x = pos[1] // 3  # box_x is the x coordinate of the 3x3 grid the number to input is in
    box_y = pos[0] // 3  # box_y is the y coordinate of the 3x3 grid the number to input is in

    for i in range(box_y * 3, box_y * 3 + 3):  # for every column in the 3x3 grid:
        for j in range(box_x * 3, box_x * 3 + 3):  # for every row in the 3x3 grid:
            if bo[i][j] == number and [i, j] != pos:  # if the cell is equal to the number to input and the position of the cell is not the same as the position of the number to input, return False as it breaks a rule of sudoku
                return False

    return True  # if no rules are broken, return True (valid)


def BT(bo):  # I am using a backtracking algorithm which uses recursion to find a solution to a problem

    find = find_0(bo)  # checks to see if there are any empty spots left
    if not find:
        return bo  # if no empty cells are left, the board is returned as it is completed

    else:
        row, col = find  # the list is split into row and column

    for i in range(1, 10):  # for every valid number that can be inputted:
        if check_valid(bo, i, (row, col)):  # algorithm tries every number in the empty cell and when it finds a valid number, it inserts that number into the cell
            bo[row][col] = i

            if BT(bo):  # recurses to try and find the next solution to the updated board.
                return bo  # if it solves, board is returned

            bo[row][col] = 0  # if no board is returned above, that means that the board becomes unvalid while trying to solve the rest of the board. Thus, that board value is set to 0 an tried again

    return False  # if no answer is found, return False