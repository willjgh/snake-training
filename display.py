import pygame
import pygame.gfxdraw
import numpy as np

class Display():
    
    def __init__(self, grid_height, grid_width, tick=1):
        '''Initialize.'''

        # initialize pygame
        pygame.init()

        # window: high resolution, display on screen
        self.window_width = 500
        self.window_height = 500
        self.window = pygame.display.set_mode((self.window_width, self.window_height))

        # canvas: low resolution, draw on then draw to window
        self.canvas_width = grid_height
        self.canvas_height = grid_width
        self.canvas = pygame.Surface((self.canvas_width, self.canvas_height))

        # pygame settings
        pygame.display.set_caption("Snake evolution")
        self.clock = pygame.time.Clock()
        self.tick = tick

        # state
        self.running = True


    def event_handler(self):
        '''Handle inputs.'''

        # loop over events
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False


    def draw_initial_snake(self, snake):
        '''Initial drawing of snake body, food and grid.'''
        
        # fill canvas with black
        self.canvas.fill((0, 0, 0))

        # draw snake body in green
        for pos in snake.body:
            
            pygame.gfxdraw.pixel(self.canvas, pos[1], pos[0], (0, 255, 0))

        # draw food in red
        pygame.gfxdraw.pixel(self.canvas, snake.food[1], snake.food[0], (255, 0, 0))

        # blit canvas to window
        self.window.blit(
            pygame.transform.scale(
                self.canvas,
                (
                    self.window_width,
                    self.window_height
                )
            ),
            (
                0,
                0
            )
        )

        # update display
        pygame.display.flip()


    def draw_snake(self, snake):
        '''Update snake display.'''

        # set refresh rate
        self.clock.tick(self.tick)
        
        # draw over old tail position
        if snake.tail_old:
            pygame.gfxdraw.pixel(self.canvas, snake.tail_old[1], snake.tail_old[0], (0, 0, 0))

        # draw new head position
        pygame.gfxdraw.pixel(self.canvas, snake.body[0][1], snake.body[0][0], (0, 255, 0))

        # draw over old food position
        if snake.food_old:
            pygame.gfxdraw.pixel(self.canvas, snake.food_old[1], snake.food_old[0], (0, 255, 0))

            # draw new food position
            pygame.gfxdraw.pixel(self.canvas, snake.food[1], snake.food[0], (0, 255, 0))

        # blit canvas to window
        self.window.blit(
            pygame.transform.scale(
                self.canvas,
                (
                    self.window_width,
                    self.window_height
                )
            ),
            (
                0,
                0
            )
        )

        # update display
        pygame.display.flip()


class MultiDisplay():
    
    def __init__(self, multi_size, grid_height, grid_width, tick=1):
        '''Initialize.'''

        # initialize pygame
        pygame.init()

        # window: high resolution, display on screen
        self.window_width = 1000
        self.window_height = 1000
        self.window = pygame.display.set_mode((self.window_width, self.window_height))

        # canvas: low resolution, draw on then draw to window
        self.canvas_width = grid_height
        self.canvas_height = grid_width
        self.multi_size = multi_size
        self.canvas_list = [pygame.Surface((self.canvas_width, self.canvas_height)) for i in range(self.multi_size**2)]

        # pygame settings
        pygame.display.set_caption("Snake evolution")
        self.clock = pygame.time.Clock()
        self.tick = tick

        # state
        self.running = True


    def event_handler(self):
        '''Handle inputs.'''

        # loop over events
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False


    def draw_initial_population(self, snakes):
        '''Initial drawing of snake body, food and grid.'''

        # fill window with white
        self.window.fill((255, 255, 255))

        # for each snake
        for i, snake in enumerate(snakes):

            # get canvas
            canvas = self.canvas_list[i]
        
            # fill canvas with black
            canvas.fill((0, 0, 0))

            # draw snake body in green
            for pos in snake.body:
                
                pygame.gfxdraw.pixel(canvas, pos[1], pos[0], (0, 255, 0))

            # draw food in red
            pygame.gfxdraw.pixel(canvas, snake.food[1], snake.food[0], (255, 0, 0))

        # blit each canvas to section on window
        for i in range(self.multi_size):
            for j in range(self.multi_size):
                canvas = self.canvas_list[i*self.multi_size + j]
                self.window.blit(
                    pygame.transform.scale(
                        canvas,
                        (
                            self.window_width // self.multi_size - 1,
                            self.window_height // self.multi_size - 1
                        )
                    ),
                    (
                        j * (self.window_width // self.multi_size),
                        i * (self.window_height // self.multi_size)
                    )
                )

        # update display
        pygame.display.flip()


    def draw_population(self, snakes):
        '''Update snake display for each snake.'''

        # set refresh rate
        self.clock.tick(self.tick)

        # for each snake
        for i, snake in enumerate(snakes):

            # do not update dead snakes
            if snake.dead:
                continue

            # get canvas
            canvas = self.canvas_list[i]
            
            # draw over old tail position
            if snake.tail_old:
                pygame.gfxdraw.pixel(canvas, snake.tail_old[1], snake.tail_old[0], (0, 0, 0))

            # draw new head position
            pygame.gfxdraw.pixel(canvas, snake.body[0][1], snake.body[0][0], (0, 255, 0))

            # draw over old food position
            if snake.food_old:
                pygame.gfxdraw.pixel(canvas, snake.food_old[1], snake.food_old[0], (0, 255, 0))

                # draw new food position
                pygame.gfxdraw.pixel(canvas, snake.food[1], snake.food[0], (0, 255, 0))

        # blit each canvas to section on window
        for i in range(self.multi_size):
            for j in range(self.multi_size):
                canvas = self.canvas_list[i*self.multi_size + j]
                self.window.blit(
                    pygame.transform.scale(
                        canvas,
                        (
                            self.window_width // self.multi_size - 1,
                            self.window_height // self.multi_size - 1
                        )
                    ),
                    (
                        j * (self.window_width // self.multi_size),
                        i * (self.window_height // self.multi_size)
                    )
                )

        # update display
        pygame.display.flip()