#
# Use this file to implement your the Genetic Algorithm
#
from math import ceil, floor
from copy import deepcopy
import operator
import random
def get_minimum_index(population):
    mini = float("inf")
    min_index = None
    for i in range(len(population)):
        if population[i].fitness < mini:
            mini = population[i].fitness
            min_index = i
    return min_index

def get_maximum_index(population):
    maxi = -float("inf")
    max_index = None
    for i in range(len(population)):
        if population[i].fitness > maxi:
            maxi = population[i].fitness
            max_index = i
    return max_index
def genetic_algorithm(budget, direction, initialize_population, compute_objective, selection_operator, crossover_operator,
                      crossover_probability, mutation_operator, mutation_probability):
    """
        :param budget: how many iterations the algorithms can run
        :param direction: MIN or MAX
        :param initialize_population: call this function to initialize the population
        :param compute_objective: call this function to evaluate an individual, i.e., compute its fitness value
        :param selection_operator: operator to select the individuals
        :param crossover_operator: recombine two parents (individuals) to generate (at most two) offsprings
        :param crossover_probability: the probability to trigger the crossover
        :param mutation_operator: mutate an individual
        :param mutation_probability: the probability to trigger this mutation
        """

    assert isinstance(budget, int), "Budget must be an integer. Provided {}".format(type(budget))
    assert budget > 0, "Budget must be a positive integer. Provided value {}".format(budget)

    assert str(direction).upper() == "MIN" or str(direction).upper() == "MAX", "Invalid direction for search {}".format(
        direction)

    assert 0.0 <= crossover_probability <= 1.0, "Invalid Crossover probability"
    assert 0.0 <= mutation_probability <= 1.0, "Invalid Mutation probability"

    # The following must be functions. We might even check what parameters they declare?
    assert callable(initialize_population)
    assert callable(compute_objective)
    assert callable(selection_operator)
    assert callable(crossover_operator)
    assert callable(mutation_operator)

    # Configure the compare operator to find the BEST solution
    # NOTE: you can call "compare_operator(a, b)" instead of a >= b (or a <= b).
    compare_operator = None
    if direction == "MIN":
        compare_operator = operator.le # operator.lt if you want < instead
    else:
        compare_operator = operator.ge # operator.gt if you want > instead

    # Note: We are using High-Order function, so we return a function (the optimization_algorithm) that is configured
    #       with the parameters and functions that we passed as input to genetic_algorithm


    def optimization_algorithm():
        """
            This is the actual function that will be called by the test cases
            :return: the best solution found and its fitness
        """
        best_solution = None
        best_score = None

        # TODO Implement here your solution

         # generate population
        population = initialize_population()
        POPULATION_SIZE = len(population)

        # compute objective for every population object
        for object in population:
            compute_objective(object)

        j = 0
        while j < budget:

            parent1 = selection_operator(population)
            parent2 = selection_operator(population)

            for i in range(0, POPULATION_SIZE, 2):
                if random.random() < crossover_probability:
                    temp_parent1, temp_parent2 = crossover_operator(parent1, parent2)
                    compute_objective(temp_parent1)
                    compute_objective(temp_parent2)
                    if direction.upper() == "MAX":
                        if population[get_minimum_index(population)].fitness < temp_parent1.fitness:
                            population[get_minimum_index(population)] = temp_parent1
                        if population[get_minimum_index(population)].fitness < temp_parent2.fitness:
                            population[get_minimum_index(population)] = temp_parent2
                    elif direction.upper() == "MIN":
                        if population[get_minimum_index(population)].fitness > temp_parent1.fitness:
                            population[get_maximum_index(population)] = temp_parent1
                        if population[get_maximum_index(population)].fitness > temp_parent2.fitness:
                            population[get_maximum_index(population)] = temp_parent2


            for i in range(POPULATION_SIZE):
                if random.random() < mutation_probability:
                    temp_parent = population[i]
                    mutation_operator(temp_parent)
                    compute_objective(temp_parent)
                    if direction.upper() == "MAX":
                        if population[get_minimum_index(population)].fitness < temp_parent.fitness:
                            population[get_minimum_index(population)] = temp_parent
                    elif direction.upper() == "MIN":
                        if population[get_minimum_index(population)].fitness > temp_parent.fitness:
                            population[get_maximum_index(population)] = temp_parent
            j += 1

        if direction == "MAX":
            i = get_maximum_index(population)
            best_solution = population[i]
            best_score = best_solution.fitness
        elif direction == "MIN":
            i = get_minimum_index(population)
            best_solution = population[i]
            best_score = best_solution.fitness

        return best_solution, best_score

    # Return the configured optimization algorithm function that is ready to run
    return optimization_algorithm


