import random
import math
import pytest
import operator
from collections import defaultdict
from copy import deepcopy

from evolutionary import genetic_algorithm

def generate_the_review_assignment_max(problem_size, budget):
    """
    Exemplify the algorithm over the MAX ONE combinatorial problem. Max One Problem is the
    simplest problem that only performs the calculation of the maximum value from a number of binary strings.
    :param problem_size: how many dimensions (n bits) the problem has
    :param budget: how many iterations the algorithm is allowed to run
    :return:
    """

    mutation_probability = 0.2
    crossover_probability = 0.8

    # Just randomly initializing the vars
    t = 8
    c = 4
    preference_range = (-100, 100)
    direction = "MAX"

    class Object(object):
        pass

    class Topic(object):
        pass
    
    topic_list_index = [i+1 for i in range(t)]

    topic_list = []
    # assignment and their preferences on each topic
    for topic in topic_list_index:
        topic_preference = {}
        topic = Topic()

        # Assignment index
        for i in range(1, problem_size+1):
            topic_preference[i] = random.randint(preference_range[0], preference_range[1])
        setattr(topic, "preference_dict", topic_preference)
        topic_list.append(topic)
        print(topic_preference)

    def generate_random_individual():
        is_valid = False
        while is_valid == False:
            individual = list()
            for i in range(1, problem_size+1):
                topic = random.randint(1, t)
                individual.append(topic)
            if checkIndividual(individual) == True:
                is_valid = True
        return individual

    def checkIndividual(individual):
        count_topic_dict = defaultdict(lambda:0)
        for topic in individual:
            count_topic_dict[topic] += 1
        if max(count_topic_dict.values()) <= c:
            return True
        else:
            return False

    def compute_objective(individual):
        preference_sum = 0
        i = 1     # Assignment Index
        for topic_index in individual.genotype:
            topic = topic_list[topic_index - 1]
            preference_sum += topic.preference_dict[i]
            i += 1

        individual.fitness = preference_sum

    def initialize_population():
        population = list()
        for i in range(0, problem_size):
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

        count = 20
        is_valid = False
        while i < count and is_valid == False:
            # Choose a random cut point that cannot be the first or the last element
            cut_point = random.randint(1, len(genotype_parent_1) - 1)
            # Recombine the parents
            genotype_offspring_1 = genotype_parent_1[:cut_point] + genotype_parent_2[cut_point:]
            genotype_offspring_2 = genotype_parent_2[:cut_point] + genotype_parent_1[cut_point:]
            # Ensure we did not screw up
            assert len(genotype_offspring_1) == len(genotype_parent_1)
            assert len(genotype_offspring_2) == len(genotype_parent_2)

            if checkIndividual(genotype_offspring_1) == True and checkIndividual(genotype_offspring_2) == True:
                is_valid = True
            count += 1
        if is_valid == False:
            return parent_1, parent_2
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
        temp_genotype = deepcopy(individual.genotype)

        is_valid = False
        count = 20
        i = 0
        while i < 20 and is_valid == False:
            # Pick a topic to exchange with another topic
            topic_to_flip = random.randint(0, len(temp_genotype) - 1)
            topic_to_flip_with = random.randint(1, t)
            # Mutate the individual's genotype
            temp_genotype[topic_to_flip] = topic_to_flip_with
            if checkIndividual(temp_genotype):
                is_valid = True
        if is_valid == True:
            individual.genotype = temp_genotype
    return genetic_algorithm(budget, direction, initialize_population, compute_objective, selection_operator, crossover_operator,
                             crossover_probability, mutation_operator, mutation_probability)


def test_review_assignment(): 
    problem_size = 12
    budget = 50
    best_solution, best_score = generate_the_review_assignment_max(problem_size, budget)()
    print(best_solution.genotype, best_score)


test_review_assignment()