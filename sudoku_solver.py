import data_structures as ds
import copy



# defining the back-track function
def backtrack_search(csp):
    print(csp, "\n")
    if csp.is_complete("number"):
        return csp
    cur_csp = copy.deepcopy(csp)
    var = cur_csp.next_var(option="number")
    for value in var.number_domain:
        var.number = value
        inference = cur_csp.forward_check(var)
        if inference != 'failure':
            result = backtrack_search(cur_csp)
            result = backtrack_search_color(result)
            if result != 'failure':
                return result
        var.number_domain.remove(value)
        cur_csp = copy.deepcopy(csp)
    return 'failure'


# backtrack search for color
def backtrack_search_color(csp):
    print(csp, "\n")
    if csp.is_complete("color"):
        return csp
    cur_csp = copy.deepcopy(csp)
    var = cur_csp.next_var(option="color")
    for value in var.color_domain:
        if cur_csp.color_is_consistent(var, value):
            var.color = value
            inference = cur_csp.forward_check(var)
            if inference != 'failure':
                result = backtrack_search_color(cur_csp)
                if result != 'failure':
                    return result
        var.color_domain.remove(value)
        cur_csp = copy.deepcopy(csp)
    return 'failure'
    





def main():
    csp = ds.init_game("test1.txt")
    result = backtrack_search(csp)
    print("Final result:\n{}\n".format(result))

    

    


if __name__ == '__main__':
    main()