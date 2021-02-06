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
        self.number_domain = []
        self.color_domain = []
        self.number_constraints = []
        self.color_constraints = []


    # initializing domain
    def init_domain(self):
        global colors
        self.domain = copy.deepcopy(colors)

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
class CSP:
    def __init__(self, rows):
        self.rows = rows
        self.init_constraints()
        self.init_domains()


    # initializing the num and color constraints for each cell
    def init_constraints(self):
        table = self.rows
        for i in range(len(table)):
            for j in range(len(table[0])):
                constraint = Constraint(i, j)
                self.add_number_constraint(constraint, i, j)
                self.add_color_constraint(constraint, i, j)


    # adding a constraint to every cell in the same row and column
    def add_number_constraint(self, constraint, row, col):
        table = self.rows
        # adding constraint to the cells with the same row
        for j in range(len(table[row])):
            if j != col:
                table[row][j].number_constraints.append(constraint)
        # adding constraint to the cells with the same column
        for i in range(len(table)):
            if i != row:
                table[i][col].number_constraints.append(constraint)


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


    # initializing the domains for each sell
    def init_domains(self):
        global colors
        table = self.rows
        number_domain = [i for i in range(1, len(table) + 1)]
        for i in range(len(table)):
            for j in range(len(table[0])):
                table[i][j].number_domain = copy.deepcopy(number_domain)
                table[i][j].color_domain = copy.deepcopy(colors)
        self.init_consistent_domain()
        

    # deleting inconsistent initial values from domains
    def init_consistent_domain(self):
        table = self.rows
        for i in range(len(table)):
            for j in range(len(table[0])):
                self.forward_check(table[i][j])

    
    # forward checking algorithm after assigning a value for assigned_var
    def forward_check(self, assigned_var):
        global colors
        table = self.rows
        # deleting the assigned number and color from assigned_var domains
        if assigned_var.number in assigned_var.number_domain:
            assigned_var.number_domain.remove(assigned_var.number)
        if assigned_var.color in assigned_var.color_domain:
            assigned_var.color_domain.remove(assigned_var.color)
        # forward checking for number domain
        for index in assigned_var.number_constraints:
            cell = table[index.i][index.j]
            self.number_arc_consistency(assigned_var, cell)

        # forward checking for color domain
        for index in assigned_var.color_constraints:
            # first we make prevent colors to be the same in adjacent cells
            cell = table[index.i][index.j]
            self.color_arc_consistency(assigned_var, cell)
            self.color_arc_consistency(cell, assigned_var)
    

    # make cell's number domain consistent with the assigned value for assigned_var
    def number_arc_consistency(self, assigned_var, cell):
        # forward checking for number domain
        if assigned_var.number in cell.number_domain:
            cell.number_domain.remove(assigned_var.number)


    # make cell's color domain consistent with the assigned value for assigned_var
    def color_arc_consistency(self, assigned_var, cell):
        # forward checking for color domain
        # first we make prevent colors to be the same in adjacent cells
        number = assigned_var.number
        color = assigned_var.color
        if color in cell.color_domain:
            cell.color_domain.remove(color)
        # now we make sure cell with a higher number doesn't have any lower priority color in domain
        number = assigned_var.number
        remove_elems = []
        if self.is_assigned(assigned_var, "both") and not self.is_assigned(cell, "color") and self.is_assigned(cell, "number"):
            assigned_color_ind = colors.index(color)
            if cell.number > number:
                for c in cell.color_domain:
                    cell_color_ind = colors.index(c)
                    if cell_color_ind > assigned_color_ind:
                        remove_elems.append(c)
            elif cell.number < number:
                for c in cell.color_domain:
                    cell_color_ind = colors.index(c)
                    if cell_color_ind < assigned_color_ind:
                        remove_elems.append(c)
            for elem in remove_elems:
                cell.color_domain.remove(elem)

        # reverse of the above condition
        elif self.is_assigned(assigned_var, "both") and not self.is_assigned(cell, "number") and self.is_assigned(cell, "color"):
            assigned_color_ind = colors.index(color)
            cell_color_ind = colors.index(cell.color)
            if assigned_color_ind < cell_color_ind:
                for n in cell.number_domain:
                    if n > number:
                        remove_elems.append(n)
            elif assigned_color_ind > cell_color_ind:
                for n in cell.number_domain:
                    if n < number:
                        remove_elems.append(n) 
            for elem in remove_elems:
                cell.number_domain.remove(elem)
           


    # checking if assignment is complete
    def is_complete(self, option="number"):
        table = self.rows
        # checking number assignment
        if option == "number":
            for i in range(len(table)):
                for j in range(len(table[0])):
                    if table[i][j].number == None:
                        return False
        # checking color assignment        
        elif option == "color":
            for i in range(len(table)):
                for j in range(len(table[0])):
                    if table[i][j].color == None:
                        return False
        # checking both the color and number assignments       
        elif option == "both":
            for i in range(len(table)):
                for j in range(len(table[0])):
                    if table[i][j].color == None or table[i][j].number == None:
                        return False
        return True

    
    # returning the next cell variable for assignment based on MRV and degree heuristics
    def next_var(self, option="number"):
        table = self.rows
        mrv_cells = self.get_mrv_vars(option)
        next_cell = None
        if len(mrv_cells) == 1:
            next_cell = mrv_cells[0]
        else:
            next_cell = self.degree_heuristic(mrv_cells, option)
        return next_cell


    # returning the cells with
    def get_mrv_vars(self, option="number"):
        mrv_vars = []
        min_domain_size = 100000
        table = self.rows
        # finding minimum domain size
        for i in range(len(table)):
            for j in range(len(table[0])):
                # domain size for number
                if option == "number":
                    dom_size = len(table[i][j].number_domain)
                # domain size for color
                elif option == "color":
                    dom_size = len(table[i][j].color_domain)
                
                if dom_size < min_domain_size and not self.is_assigned(table[i][j], option):
                    min_domain_size = dom_size

        # finding cells for which domain size is the same as min_domain_size
        for i in range(len(table)):
            for j in range(len(table[0])):
                # domain size for number
                if option == "number":
                    dom_size = len(table[i][j].number_domain)
                # domain size for color
                elif option == "color":
                    dom_size = len(table[i][j].color_domain)
                
                if dom_size == min_domain_size and not self.is_assigned(table[i][j], option):
                    mrv_vars.append(table[i][j])
        return mrv_vars

    
    # checking if the given cell has already an assigned value for its given option
    def is_assigned(self, cell, option="number"):
        if option == "number" and cell.number != None:
            return True
        elif option == "color" and cell.color != None:
            return True
        elif option == "both" and cell.number != None and cell.color != None:
            return True
        return False

    
    # getting the next variable using degree heuristic for when mrv heuristic doesn't return a single variable
    def degree_heuristic(self, mrv_vars, option="number"):
        max_degree = 0
        # finding minimum degree
        for i in range(len(mrv_vars)):
            # degree for number
            if option == "number":
                cur_degree = len(mrv_vars[i].number_constraints)
            # degree for color
            elif option == "color":
                cur_degree = len(mrv_vars[i].color_constraints)
            
            if cur_degree > max_degree:
                max_degree = cur_degree
        # returning the mrv variable with the least degree
        for i in range(len(mrv_vars)):
            # degree for number
            if option == "number":
                cur_degree = len(mrv_vars[i].number_constraints)
            # degree for color
            elif option == "color":
                cur_degree = len(mrv_vars[i].color_constraints)
            
            if cur_degree == max_degree:
                return mrv_vars[i]
                

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
    global rows_num, colors_num, colors
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
                    else:
                        num = int(num)
                    if color == "#":
                        color = None 
                    cell = Cell(num, color)
                    row_cells[i].append(cell)

    # building the CSP
    init_state = CSP(row_cells)
    return init_state