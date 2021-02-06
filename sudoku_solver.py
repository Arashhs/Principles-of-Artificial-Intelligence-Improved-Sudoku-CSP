import data_structures as ds
import copy, random


# defining the back-track function
def backtrack_search(csp):
    print(csp, "\n")
    if csp.is_complete("both"):
        return csp
    # cur_csp = copy.deepcopy(csp)
    cur_csp = copy.copy(csp)
    var, hint = cur_csp.next_var(option="both")
    if hint == "number":
        while len(var.number_domain) > 0:
            value = var.number_domain.pop(random.randrange(len(var.number_domain)))
            var.number = value
            inference = cur_csp.forward_check(var)
            if inference != 'failure':
                result = backtrack_search(cur_csp)
                if result != 'failure':
                    return result
            # var.number_domain.remove(value)
            var, cur_csp = restore_inferences(var, csp)
        return 'failure'
    elif hint == "color":
        while len(var.color_domain) > 0:
            value = var.color_domain.pop(random.randrange(len(var.color_domain)))
            var.color = value
            inference = cur_csp.forward_check(var)
            if inference != 'failure':
                result = backtrack_search(cur_csp)
                if result != 'failure':
                    return result
            # var.color_domain.remove(value)
            var, cur_csp = restore_inferences(var, csp)
        return 'failure'



# restoring inferences after a failure
def restore_inferences(var, csp):
    restored_csp = copy.copy(csp)
    new_var = restored_csp.rows[var.i][var.j]
    new_var.color_domain = var.color_domain.copy()
    new_var.number_domain = var.number_domain.copy()
    return new_var, restored_csp
    





def main():
    csp = ds.init_game("test5.txt")
    result = backtrack_search(csp)
    print("Final result:\n{}\n".format(result))

    

    


if __name__ == '__main__':
    main()