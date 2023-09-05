import random
import math
import pytest
import operator

from local import steepest_ascent_hill_climbing_with_random_restart


def generate_the_max_one_optimization_problem(problem_size, budget):
    """
    Exemplify the algorithms over the MAX ONE combinatorial problem. Max One Problem is the
    simplest problem that only performs the calculation of the maximum value from a number of binary strings.
    :param problem_size: how many dimensions (n bits) the problem has
    :param budget: how many iterations the algorithm is allowed to run
    :return:
    """
    random.seed(528)
    direction = "MAX"
    best_neighbor_operator = operator.lt if direction == "MIN" else operator.gt

    def generate_random_solution():
        individual = list()
        for i in range(0, problem_size):
            individual.append(random.randint(0, 100) % 2)
        return individual

    def compute_objective(individual):
        return sum(individual)

    def get_neighbors(individual):
        # Flip each bit one at the time
        neighbors = list()
        for i in range(0, problem_size):
            # Assuming the individual is a list
            neighbor = individual[:]
            # Flip the bit: 0 -> 1 % 2 = 1; 1 -> 2 % 2 = 0
            neighbor[i] = 0 if neighbor[i] == 1 else 1
            neighbors.append(neighbor)

        return neighbors

    def get_best_neighbor(individual):
        neighbors = get_neighbors(individual)
        best_score = compute_objective(neighbors[0])
        best_neighbor = neighbors[0]
        for neighbor in neighbors:
            neighbor_score = compute_objective(neighbor)
            # we maximize
            if best_neighbor_operator(neighbor_score, best_score):
                best_score = neighbor_score
                best_neighbor = neighbor

        return best_neighbor, best_score

    return steepest_ascent_hill_climbing_with_random_restart(budget, direction, generate_random_solution,
                                                             compute_objective, get_neighbors, get_best_neighbor)


def test_local_with_max_one():
    problem_size = 10
    budget = 12
    best_solution, best_score = generate_the_max_one_optimization_problem(problem_size, budget)()
    assert best_score == pytest.approx(problem_size)

def generate_the_sum_square_optimization_problem(problem_size, budget):
    random.seed(47402)
    bounds = (-10.0, 10.0)
    max_radius = 0.1
    # Sample n_neighbors per dimension
    n_neighbors = 10

    direction = "MIN"
    best_neighbor_operator = operator.lt if direction == "MIN" else operator.gt

    def generate_random_solution():
        individual = list()
        for i in range(0, problem_size):
            individual.append(random.uniform(bounds[0], bounds[1]))
        return individual

    def compute_objective(individual):
        score = 0.0
        for i in range(len(individual)):
            score += (i + 1) * individual[i] ** 2
        return score

    def get_neighbors(individual):
        # Sample a number of individuals within a given radius
        neighbors = list()
        for i in range(0, problem_size):
            for n in range(0, n_neighbors):
                neighbor = individual[:]
                # Move point by a random radius - NOTE: This could be also Gaussian
                neighbor[i] += random.uniform(-max_radius, max_radius)
                if bounds[0] <= neighbor[i] <= bounds[1]:
                    neighbors.append(neighbor)
                else:
                    print("Invalid neighbor rejected")

        return neighbors

    def get_best_neighbor(individual):
        neighbors = get_neighbors(individual)
        best_score = compute_objective(neighbors[0])
        best_neighbor = neighbors[0]
        for neighbor in neighbors:
            neighbor_score = compute_objective(neighbor)
            if best_neighbor_operator(neighbor_score, best_score):
                best_score = neighbor_score
                best_neighbor = neighbor

        return best_neighbor, best_score

    return steepest_ascent_hill_climbing_with_random_restart(budget, direction, generate_random_solution,
                                                             compute_objective, get_neighbors, get_best_neighbor)


def test_local_with_sum_square():
    problem_size = 1
    budget = 200
    best_solution, best_score = generate_the_sum_square_optimization_problem(problem_size, budget)()
    # Since we operate with real numbers we need to compare them using a tolerance value
    assert best_score == pytest.approx(0.0, abs=1e-3)


def generate_the_local_optima_optimization_problem(budget):
    random.seed(26972)
    # This function is 2D
    problem_size = 1
    # According to http://www.sfu.ca/~ssurjano/ackley.html this function is evaluated in with those bounds
    bounds = (0, 6.0)
    # Search radius
    max_radius = 0.05
    # Sample n_neighbors per dimension
    n_neighbors = 10
    #
    direction = "MIN"
    best_neighbor_operator = operator.lt if direction == "MIN" else operator.gt

    def generate_random_solution():
        individual = list()
        for i in range(0, problem_size):
            individual.append(random.uniform(bounds[0], bounds[1]))
        return individual

    def compute_objective(individual):
        # Standard local minima https://www.lindo.com/doc/online_help/lingo18_0/local_optima_vs__global_optima.htm
        x = individual[0]
        return x * math.cos(math.pi * x)

    def get_neighbors(individual):
        # Sample a number of individuals within a given radius
        neighbors = list()
        for i in range(0, problem_size):
            for n in range(0, n_neighbors):
                neighbor = individual[:]
                # Move point by a random radius - NOTE: This could be also Gaussian
                neighbor[i] += random.uniform(-max_radius, max_radius)
                if bounds[0] <= neighbor[i] <= bounds[1]:
                    neighbors.append(neighbor)
                else:
                    print("Invalid neighbor rejected")

        return neighbors

    def get_best_neighbor(individual):
        neighbors = get_neighbors(individual)
        best_score = compute_objective(neighbors[0])
        best_neighbor = neighbors[0]
        for neighbor in neighbors:
            neighbor_score = compute_objective(neighbor)
            if best_neighbor_operator(neighbor_score, best_score):
                best_score = neighbor_score
                best_neighbor = neighbor

        return best_neighbor, best_score

    return steepest_ascent_hill_climbing_with_random_restart(budget, direction, generate_random_solution,
                                                             compute_objective, get_neighbors, get_best_neighbor)


def test_local_with_local_optima():
    # TODO: A better test would be to start the search in a predefined location that would trap the search in the minima
    budget = 200
    # Note there's no problem dimension because Ackley is a 2D function
    best_solution, best_score = generate_the_local_optima_optimization_problem(budget)()
    # Since we operate with real numbers we need to compare them using a tolerance value
    # TODO We can also check whether the solution is closed by the "known" optimum
    assert best_solution[0] == pytest.approx(5.02, abs=1e-3)
    assert best_score == pytest.approx(-5.01, abs=1e-3)


