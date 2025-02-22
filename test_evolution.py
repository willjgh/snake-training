from population import Population

# create population of models
population = Population(population_size=1000)

# initialize population
population.initialize()

# for each generation
for gen in range(5):

    # compute fitness
    population.compute_fitness()

    # display best performance
    population.display_fittest()

    # evolve new generation
    population.evolve_population(selected_number=5)