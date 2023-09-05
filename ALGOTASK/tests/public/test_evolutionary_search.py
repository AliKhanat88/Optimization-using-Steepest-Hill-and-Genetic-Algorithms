import random
import math
import pytest
import operator

from evolutionary import genetic_algorithm

def generate_the_max_one_optimization_problem(problem_size, budget):
    """
    Exemplify the algorithm over the MAX ONE combinatorial problem. Max One Problem is the
    simplest problem that only performs the calculation of the maximum value from a number of binary strings.
    :param problem_size: how many dimensions (n bits) the problem has
    :param budget: how many iterations the algorithm is allowed to run
    :return:
    """
    random.seed(67660)
    population_size = 4
    mutation_probability = 0.2
    crossover_probability = 0.8

    direction = "MAX"

    class Object(object):
        pass

    def generate_random_individual():
        individual = [1, 1, 1]
        for i in range(3, problem_size):
            individual.append(random.randint(0, 100) % 2)
        return individual

    def compute_objective(individual):
        individual.fitness = sum(individual.genotype)

    def initialize_population():
        population = list()
        for i in range(0, population_size):
            genotype = generate_random_individual()
            individual = Object()
            setattr(individual, "genotype", genotype)
            setattr(individual, "fitness", None)
            population.append(individual)
        return population

    def selection_operator(individuals):
        # Roulette Wheel Selection
        # Compute the total
        total_fitness = sum([individual.fitness for individual in individuals])

        # Computes for each chromosome the probability
        chromosome_probabilities = [individual.fitness / total_fitness for individual in individuals]

        # Selects one chromosome based on the computed probabilities
        wheel = random.uniform(0.0, 1.0)
        i = 0
        the_sum = chromosome_probabilities[i]
        while the_sum < wheel:
            i += 1
            the_sum += chromosome_probabilities[i]

        return individuals[i]

    def crossover_operator(parent_1, parent_2):
        # Extract genotype:
        genotype_parent_1 = parent_1.genotype
        genotype_parent_2 = parent_2.genotype

        # We cannot recombine parents when they are too short!
        if len(genotype_parent_1) == 1:
            return parent_1, parent_2

        # Choose a random cut point that cannot be the first or the last element
        cut_point = random.randint(1, len(genotype_parent_1) - 1)
        # Recombine the parents
        genotype_offspring_1 = genotype_parent_1[:cut_point] + genotype_parent_2[cut_point:]
        genotype_offspring_2 = genotype_parent_2[:cut_point] + genotype_parent_1[cut_point:]
        # Ensure we did not screw up
        assert len(genotype_offspring_1) == len(genotype_parent_1)
        assert len(genotype_offspring_2) == len(genotype_parent_2)

        # Create the new individuals
        offspring_1 = Object()
        setattr(offspring_1, "genotype", genotype_offspring_1)
        setattr(offspring_1, "fitness", None)

        offspring_2 = Object()
        setattr(offspring_2, "genotype", genotype_offspring_2)
        setattr(offspring_2, "fitness", None)

        return offspring_1, offspring_2

    def mutation_operator(individual):
        # Extract the genotype
        genotype = individual.genotype
        # Pick a bit at random and flip it
        bit_to_flip = random.randint(0, len(genotype) - 1)
        # Mutate the individual's genotype
        genotype[bit_to_flip] = 0 if genotype[bit_to_flip] == 1 else 1

    return genetic_algorithm(budget, direction, initialize_population, compute_objective, selection_operator, crossover_operator,
                             crossover_probability, mutation_operator, mutation_probability)


def test_local_with_max_one():
    problem_size = 4
    budget = problem_size + 2
    best_solution, best_score = generate_the_max_one_optimization_problem(problem_size, budget)()
    assert best_score == pytest.approx(problem_size)


test_local_with_max_one()
