import data_structures as ds
import copy



# defining the back-track function
def backtrack_search(csp):
    if csp.is_complete():
        return csp
    cur_state = copy.deepcopy(csp)
    cell = csp.next_var(option="number")
    cell.number = 2
    csp.forward_check(cell)
    cell = csp.next_var()
    cell.number = 3
    print(cell)
    





def main():
    csp = ds.init_game("test1.txt")
    print(csp)
    backtrack_search(csp)

    

    


if __name__ == '__main__':
    main()