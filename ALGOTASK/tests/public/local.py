#
# Use this file to implement your Steepest-Ascent/Descent Hill Climbing with Random Restart
#
import operator


def steepest_ascent_hill_climbing_with_random_restart(budget, direction, generate_random_solution, compute_objective,
                                                      get_neighbors, get_best_neighbor):
    """
    :param direction: Min/Max
    :param budget: how many iterations the algorithms can run
    :param generate_random_solution: call this function to generate a new random solution
    :param compute_objective: call this function to evaluate a solution
    :param get_neighbors: call this function to return the neighbors of a solution
    :param get_best_neighbor: call this function to return the best of the neighbors of a solution
    """
    assert str(direction).upper() == "MIN" or str(direction).upper() == "MAX", "Invalid direction for search {}".format(
        direction)
    assert isinstance(budget, int), "Budget must be an integer. Provided {}".format(type(budget))
    assert budget > 0, "Budget must be a positive integer. Provided value {}".format(budget)

    # The following must be functions. We might even check what parameters they declare?
    assert callable(generate_random_solution)
    assert callable(compute_objective)
    assert callable(get_neighbors)
    assert callable(get_best_neighbor)

    # Configure the compare operator
    # NOTE: you can call "compare_operator(a, b)" instead of a >= b (or a <= b).
    if direction == "MIN":
        compare_operator = operator.le
    else:
        compare_operator = operator.ge
    
    # Note: We are using High-Order function, so we return a function (the optimization_algorithm) that is configured
    #       with the parameters and functions that we passed as input to steepest_ascent_hill_climbing_with_random_restart
    def optimization_algorithm():
        """
        This is the actual function that will be called by the test cases
        :return: the best solution found and its fitness
        """
        best_solution = None
        if direction.upper() == "MAX":
            best_score = -float("inf")
        else:
            best_score = float("inf")

        # TODO Implement here your solution.
        # NOTE: you can refer to the variables bound to steepest_ascent_hill_climbing_with_random_restart
        i = 0
        while i < budget:
            population = generate_random_solution()
            temp, temp_score = get_best_neighbor(population)
            if direction.upper() == "MAX":
                if temp_score >= best_score:
                    best_score = temp_score
                    best_solution = temp
            elif direction.upper() == "MIN":
                if temp_score <= best_score:
                    best_score = temp_score
                    best_solution = temp

            i = i + 1


        return best_solution, best_score

    # Return the configured optimization algorithm function that is ready to run
    return optimization_algorithm