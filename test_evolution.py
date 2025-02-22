from population import Population

# create population of models
population = Population(population_size=100)

# initialize population
population.initialize()

# for each generation
for gen in range(100):

    # compute fitness
    population.compute_fitness()

    # display stats
    population.print_population_statistics()

    # display best performance
    if gen % 10 == 0:
        population.display_fittest()

    # evolve new generation
    population.evolve_population(selected_number=5)