import numpy as np
import copy
from model import Model
from snake import Snake
from display import Display

rng = np.random.default_rng()

class Population():

    def __init__(self, population_size, mutation_rate=0.05):
        '''Initialize.'''
        self.population_size = population_size
        self.population = []
        self.mutation_rate = mutation_rate
        self.generation = 0


    def initialize(self):
        '''Initialize a new population.'''

        # reset generations
        self.generation = 0

        # clear population
        self.population = []

        # initialize new models
        for i in range(self.population_size):
            model = Model()
            model.initialize_parameters()
            self.population.append(model)


    def mutation(self, model):
        '''Mutate parameters of a given model.'''

        # store mutated parameters
        weights_mut = []
        biases_mut = []
        
        # mutate weight matrices
        for weight in model.weights:

            # create bernoulli mask for mutated values
            mask = rng.binomial(1, self.mutation_rate, size=weight.shape)

            # create uniform mutations
            mut = rng.uniform(-1, 1, size=weight.shape)

            # add mutation
            weight_new = weight + mask * mut

            # store
            weights_mut.append(weight_new)

        # mutate bias
        for bias in model.biases:

            # create bernoulli mask for mutated values
            mask = rng.binomial(1, self.mutation_rate, size=bias.shape[0])

            # create uniform mutations
            mut = rng.uniform(-1, 1, size=bias.shape[0])

            # add mutation
            bias_new = bias + mask * mut

            # store
            biases_mut.append(bias_new)

        # create a copy of model
        model_mut = copy.deepcopy(model)

        # set to mutated parameters
        model_mut.weights = weights_mut
        model_mut.biases = biases_mut

        # return mutated model
        return model_mut


    def crossover(self, model_1, model_2):
        '''Crossover parameters of 2 given models.'''

        # store crossed parameters
        weights_cross = []
        biases_cross = []
        
        # crossover each weight matrix
        for weight_1, weight_2 in zip(model_1.weights, model_2.weights):

            # get shape
            m, n = weight_1.shape

            # flatten
            weight_1.flatten()
            weight_2.flatten()

            # crossover point
            cross = rng.integers(0, m * n)

            # crossover
            weight_new = np.concat((weight_1[:cross], weight_2[cross:]))

            # reshape
            weight_new.reshape((m, n))

            # store
            weights_cross.append(weight_new)

        # crossover each bias
        for bias_1, bias_2 in zip(model_1.biases, model_2.biases):

            # get length
            m = bias_1.shape[0]

            # crossover point
            cross = rng.integers(0, m)

            # crossover
            bias_new = np.concat((bias_1[:cross], bias_2[cross:]))

            # store
            biases_cross.append(bias_new)

        # create a copy of model_1
        model_cross = copy.deepcopy(model_1)

        # set to crossover parameters
        model_cross.weights = weights_cross
        model_cross.biases = biases_cross

        # return crossed model
        return model_cross
    

    def compute_fitness(self, trials=3):
        '''Run trials to compute fitness of each model in population.'''

        # trials
        seed_list = rng.integers(0, 1000, size=trials)
        length_list = [3 for i in range(trials)]

        # for each model in population
        for model in self.population:

            # clear fitness information
            model.information = []
            model.fitness = 0

            # run multiple trials
            for i in range(trials):

                # setup trial: seed and initial length
                seed = seed_list[i]
                initial_length = length_list[i]
                grid_height = 16
                grid_width = 16

                # create a snake with trial settings
                snake = Snake(model, grid_height, grid_width, initial_length, seed)

                # run until dead
                while not snake.dead:
                    snake.move_snake()

                # trial information
                trial_info = {
                    'seed': seed,
                    'initial_length': initial_length,
                    'grid_width': grid_width,
                    'grid_height': grid_height,
                    'fitness': snake.eaten
                }

                # store
                model.information.append(trial_info)

            # compute overall fitness (will later be sum over several trials)
            model.fitness = np.mean([trial_info['fitness'] for trial_info in model.information])


    def print_population_statistics(self):
        '''Display information about fitness of population.'''

        print("-"*20)
        print(f"Generation {self.generation}:")
        print(f"Best fitness: {max([model.fitness for model in self.population])}")
        print(f"Average fitness: {np.mean([model.fitness for model in self.population])}")
        print("-"*20)

    
    def display_fittest(self):
        '''Display the best performing model.'''

        # get model with highest fitness
        fittest_model = max(self.population, key=lambda md: md.fitness)

        # find trial with highest fitness
        best_trial = max(fittest_model.information, key=lambda trial_info: trial_info['fitness'])

        # create a snake game with given settings
        snake = Snake(
            fittest_model,
            best_trial['grid_height'],
            best_trial['grid_width'],
            best_trial['initial_length'],
            best_trial['seed']
        )

        # create a display
        display = Display(
            best_trial['grid_height'],
            best_trial['grid_width']
        )

        # draw initial snake
        display.draw_initial_snake(snake)

        # loop
        while display.running:

            # if snake alive
            if not snake.dead:

                # move snake
                snake.move_snake()

                # draw update
                display.draw_snake(snake)

            # handle events
            display.event_handler()

        # close display
        display.quit()


    def evolve_population(self, selected_number=10):
        '''Use fitness to evolve a new population via selection, crossover and mutation.'''

        # sort population by fitness
        self.population.sort(key=lambda md: md.fitness, reverse=True)

        # select highest fitness models
        selected = self.population[:selected_number]

        # setup new population
        new_population = selected

        # for remaining models: crossover or mutate selected models
        for i in range(self.population_size - selected_number):

            # randomly select to crossover or mutate
            u = rng.uniform()

            if u < 0.5:

                # choose random selected models
                model_1, model_2 = rng.choice(selected, size=2)

                # crossover
                model_cross = self.crossover(model_1, model_2)

                # add to new population
                new_population.append(model_cross)

            else:

                # choose random selected model
                model = rng.choice(selected, size=1)[0]

                # mutate
                model_mut = self.mutation(model)

                # add to new population
                new_population.append(model_mut)

        # update population
        self.population = new_population

        # update generations
        self.generation += 1