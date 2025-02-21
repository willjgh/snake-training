import numpy as np

class Snake():

    def __init__(self, model, grid_height, grid_width, initial_length, seed):
        '''Initialize'''
        self.model = model
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.initial_length = initial_length
        self.seed = seed

        # random generator
        self.rng = np.random.default_rng(seed)

        # spawn snake
        self.spawn_snake()

        # spawn food
        self.spawn_food()

        # old positions for display
        self.tail_old = None
        self.food_old = None

        # snake status
        self.dead = False

    def spawn_snake(self):
        '''Generate random locations for position of snake.'''

        # head position
        head_height = self.rng.integers(0, self.grid_height)
        head_width = self.rng.integers(0, self.grid_width)

        # direction
        if head_height > self.grid_height / 2:
            dh = -1
        else:
            dh = 1
        if head_width > self.grid_width / 2:
            dw = -1
        else:
            dw = 1

        # create body
        self.body = [(head_height, head_width + i*dw) for i in range(self.initial_length)]

    
    def __len__(self):
        '''Get current snake length.'''
        return len(self.body)


    def spawn_food(self):
        '''Generate random location for food to spawn.'''

        # check empty square exists
        if len(self.body) == self.grid_height * self.grid_width:
            return False

        while True:

            food_height = self.rng.integers(0, self.grid_height)
            food_width = self.rng.integers(0, self.grid_width)

            if (food_height, food_width) not in self.body:
                self.food = (food_height, food_width)
                return True


    def move_snake(self):
        '''Use model to move snake body.'''

        # collect state
        x = np.array(self.body[0])

        # pass to model
        move = self.model.move(x)

        # old head position
        head_height_old = self.body[0][0]
        head_width_old = self.body[0][1]

        # get new position: 0 = up, 1 = right, 2 = down, 3 = left
        if move == 0:
            head_height_new = head_height_old - 1
            head_width_new = head_width_old
        elif move == 1:
            head_height_new = head_height_old
            head_width_new = head_width_old + 1
        elif move == 2:
            head_height_new = head_height_old + 1
            head_width_new = head_width_old
        elif move == 3:
            head_height_new = head_height_old
            head_width_new = head_width_old - 1

        # moving into food: do not delete tail
        if (head_height_new, head_width_new) == self.food:

            # store position of old food for display
            food_old = self.food

            # spawn new food
            status = self.spawn_food()

            # no new space: end
            if not status:
                return False

            # no tail removed
            tail_old = None

        else:

            # no new food
            food_old = None

            # remove tail
            tail_old = self.body.pop()

        # check collisions with walls
        if head_height_new < 0 or head_width_new < 0 or head_height_new >= self.grid_height or head_width_new >= self.grid_width:
            self.dead = True
            return False

        # check collisions with body
        if (head_height_new, head_width_new) in self.body:
            self.dead = True
            return False
        
        # no collisions: add head
        self.body.insert(0, (head_height_new, head_width_new))
        
        # store old tail and food position for display
        self.tail_old = tail_old
        self.food_old = food_old

        # return success
        return True


