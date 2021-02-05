import re
import copy

colors_num = None
rows_num = None
colors = None

# data structure for each sudoku cell
class Cell:
    def __init__(self, number, color):
        self.number = number
        self.color = color
        self.domain = None
        self.degree = None
        self.num_constraints = []
        self.color_constraints = []

    def __str__(self):
        num = self.number
        color = self.color
        if num == None:
            num = "*"
        if color == None:
            color = "#"
        return str(num) + color

    def __eq__(self, other):
        if self.number == other.number or self.color == other.color:
            return True
        return False

    def __repr__(self):
        return str(self)


# data structure for each constraint
class Constraint:
    def __init__(self, i, j):
        self.i = i
        self.j = j

    def __str__(self):
        return '(' + str(self.i) + ', ' + str(self.j) + ')'

    def __repr__(self):
        return str(self)



# data structure for each sudoku state
class State:
    def __init__(self, rows):
        self.rows = rows
        self.init_constraints()


    # initializing the num and color constraints for each cell
    def init_constraints(self):
        table = self.rows
        for i in range(len(table)):
            for j in range(len(table[0])):
                constraint = Constraint(i, j)
                self.add_num_constraint(constraint, i, j)
                self.add_color_constraint(constraint, i, j)


    # adding a constraint to every cell in the same row and column
    def add_num_constraint(self, constraint, row, col):
        table = self.rows
        # adding constraint to the cells with the same row
        for j in range(len(table[row])):
            if j != col:
                table[row][j].num_constraints.append(constraint)
        # adding constraint to the cells with the same column
        for i in range(len(table)):
            if i != row:
                table[i][col].num_constraints.append(constraint)


    # adding a color constraint to adjacent cells
    def add_color_constraint(self, constraint, row, col):
        table = self.rows
        top = (row - 1, col)
        right = (row, col + 1)
        bottom = (row + 1, col)
        left = (row, col - 1)
        neighbors = [top, right, bottom, left]
        for neighbor in neighbors:
            # for each adjacent cell, if the cell exists add the color constraint
            if (neighbor[0] >= 0 and neighbor[0] < len(table)):
                if (neighbor[1] >= 0 and neighbor[1] < len(table[row])):
                    table[neighbor[0]][neighbor[1]].color_constraints.append(constraint)




    def __str__(self):
        string = ""
        for i in range(len(self.rows)):
            string += str(i+1) + ":  "
            for j in range(len(self.rows[i])):
                string += self.rows[i][j].__str__() + " "
            if len(self.rows[i]) == 0:
                string += '*#'
            string = string + "\n" if i != len(self.rows) - 1 else string
        return string

    def __eq__(self, other):
        return self.rows == other.rows

    def __repr__(self):
        return str(self)


def init_game(file_name):
    global rows_num, colors_num
    rows = []
    row_cells = []
    with open(file_name, 'r') as reader:
        # read first line
        colors_num, rows_num = [int(x) for x in next(reader).split()]
        rows = [None] * (rows_num + 1)
        row_cells = [None] * rows_num

        # reading each rows
        for i in range(rows_num + 1):
            rows[i] = [x for x in next(reader).split()]

        # reading colors' row
        colors = rows[0]

        # converting each element to our Cell data structure        
        for i in range(len(rows)-1):
            row_cells[i] = []
            for elem in rows[i+1]:
                match = re.match(r"([\*0-9]+)([\#a-z]+)", elem, re.I)
                if match:
                    elem_items = match.groups()
                    num = elem_items[0]
                    color = elem_items[1]
                    if num == "*":
                        num = None
                    if color == "#":
                        color = None 
                    cell = Cell(num, color)
                    row_cells[i].append(cell)

        # building the initial state
    init_state = State(row_cells)
    return init_state