# Agents
# Agents-based modeling
# University of Amsterdam
# Julien Fer
#
# This script contains the functionality to represent Sheep and Wolves
# as random walkers in a predator-prey simulation.

from mesa import Agent
import random

class RandomWalker(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)

        self.pos = pos

    def random_move(self):
        """
        This method should get the neighbouring cells (Moore's neighbourhood), 
        select one, and move the agent to this cell.
        """
        neighbourhood = self.model.grid.get_neighborhood(self.pos, True)
        new_pos = self.random.choice(neighbourhood)
        self.model.grid.move_agent(self, new_pos)


class Sheep(RandomWalker):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model, pos)

    def step(self):
        """
        This method should move the Sheep using the `random_move()` method 
        implemented earlier, then conditionally reproduce.
        """
        self.random_move()
        if random.random() < self.model.sheep_reproduction_chance:
            self.model.new_agent(Sheep, self.pos)


class Wolf(RandomWalker):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model, pos)
        self.total_eaten = 0
        self.age = 0

    def step(self):
        '''
        This method should move the wolf, then check for sheep on its location, 
        eat the sheep if it is there and reproduce, and finally conditionally 
        die.
        '''
        self.age += 1
        self.random_move()
        animals = self.model.grid.get_neighbors(
            self.pos, True, include_center=True, radius=0)
        for animal in animals:
            if isinstance(animal, Sheep):
                self.model.remove_agent(animal)
                self.model.new_agent(Wolf, self.pos)
                self.total_eaten += 1

        if random.random() < self.model.wolf_death_chance:
            self.model.remove_agent(self)
