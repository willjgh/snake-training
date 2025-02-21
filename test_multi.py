from population import Population
from snake import Snake
from display import MultiDisplay

multi_size = 5
grid_size = 16
ticks = 10

# create population of models
pop = Population(multi_size**2)

# initialize
pop.initialize()

# create a list of snakes
snakes = [Snake(pop.population[i], grid_size, grid_size, 3, None) for i in range(multi_size**2)]

# create a display
mds = MultiDisplay(multi_size, grid_size, grid_size, tick=ticks)

# draw initial snakes
mds.draw_initial_population(snakes)

# loop
while mds.running:

    # move each snake (if not dead)
    for snake in snakes:
        if not snake.dead:
            snake.move_snake()

    # draw update
    mds.draw_population(snakes)

    # handle events
    mds.event_handler()