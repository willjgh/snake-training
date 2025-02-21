from model import Model
from snake import Snake
from display import Display

# create model
md = Model()

# initialize
md.initialize_parameters()

# create snake game
sk = Snake(md, 16, 16, 3, 1)

# create a display
ds = Display(16, 16, tick=10)

# draw initial snake
ds.draw_initial_snake(sk)

# loop
while ds.running:

    # if snake alive
    if not sk.dead:

        # move snake
        sk.move_snake()

        # draw update
        ds.draw_snake(sk)

    # handle events
    ds.event_handler()