import numpy as np

class Snake():

    def __init__(self, model, grid_height, grid_width, initial_length, seed, move_limit=300):
        '''Initialize'''

        # model controlling snake
        self.model = model

        # setup information
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.initial_length = initial_length
        self.seed = seed
        
        # move limit / currently remaining: die without food
        self.move_limit = move_limit
        self.moves_remaining = move_limit

        # food counter
        self.eaten = 0

        # random generator
        self.rng = np.random.default_rng(seed)

        # spawn snake
        self.spawn_snake()

        # spawn food
        self.spawn_food()

        # old tail position for display
        self.tail_old = None

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
    

    def look(self, dh, dw):
        '''Compute distance from snake head to wall, food, body in direction (dh, dw).'''

        # distances
        wall_dist = None
        food_dist = None
        body_dist = None
        dist_counter = 0

        # initial position
        height, width = self.body[0]

        # while within grid bounds
        while (height >= 0) and (width >= 0) and (height <= self.grid_height - 1) and (width <= self.grid_width - 1):

            # check if at food
            if (height, width) == self.food:
                food_dist = dist_counter

            # check if in body (but not head) (and first time)
            if ((height, width) in self.body[1:]) and (body_dist is None):
                body_dist = dist_counter

            # increment distance
            height += dh
            width += dw
            dist_counter += 1

        # once out of bounds know at wall
        wall_dist = dist_counter

        # food or body not found: default -1
        if food_dist is None:
            food_dist = -1
        if body_dist is None:
            body_dist = -1

        return wall_dist, food_dist, body_dist
    
    
    def state_to_input(self):
        '''Compute model input vector from current gamestate.'''

        # collect input
        x = np.array([
            *self.look(-1, 0),
            *self.look(-1, 1),
            *self.look(0, 1),
            *self.look(1, 1),
            *self.look(1, 0),
            *self.look(1, -1),
            *self.look(0, -1),
            *self.look(-1, -1),
        ])

        return x


    def move_snake(self):
        '''Use model to move snake body.'''

        # no moves remaining: end
        if self.moves_remaining == 0:
            self.dead = True
            return None

        # compute input
        x = self.state_to_input()

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

            # reset moves remaining
            self.moves_remaining = self.move_limit

            # increment food counter
            self.eaten += 1

            # spawn new food
            status = self.spawn_food()

            # no new space: end
            if not status:
                self.dead = True
                return None

            # no tail removed
            tail_old = None

        else:

            # use up one move
            self.moves_remaining -= 1

            # remove tail
            tail_old = self.body.pop()

        # check collisions with walls
        if head_height_new < 0 or head_width_new < 0 or head_height_new >= self.grid_height or head_width_new >= self.grid_width:
            self.dead = True
            return None

        # check collisions with body
        if (head_height_new, head_width_new) in self.body:
            self.dead = True
            return None
        
        # no collisions: add head
        self.body.insert(0, (head_height_new, head_width_new))
        
        # store old tail position for display
        self.tail_old = tail_old

        return None