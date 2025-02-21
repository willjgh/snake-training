import numpy as np
import copy
from model import Model

rng = np.random.default_rng()

class Population():

    def __init__(self, size=4, mutation_rate=0.2):
        self.size = size
        self.population = []
        self.mutation_rate = mutation_rate

    def initialize(self):
        '''Initialize a new population.'''
        # clear population
        self.population = []

        # initialize new models
        for i in range(self.size):
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
    
    def evolve(self, selected=[]):
        '''Evolve new generation'''

        # fail if less than 2 selected
        if len(selected) < 2:
            print("Select 2 or more models")
            return False

        # setup new population
        new_population = []

        # keep model or replace with mutated or crossed versions
        for i in range(self.size):

            # keep
            if i in selected:
                new_population.append(self.population[i])
            else:
                u = rng.uniform()

                # crossover
                if u < 0.5:

                    # choose random selected models
                    j, k = rng.choice(selected, size=2).tolist()

                    model_cross = self.crossover(self.population[j], self.population[k])
                    new_population.append(model_cross)

                # mutation
                else:

                    # choose random selected model
                    j = int(rng.choice(selected, size=1))

                    model_mut = self.mutation(self.population[j])
                    new_population.append(model_mut)

        # set to population
        self.population = new_population