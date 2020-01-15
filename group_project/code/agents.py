# Agents
# Agents-based modeling
# University of Amsterdam
# Julien Fer
#
# This script contains the functionality to represent gang members.

from mesa import Agent
import random

class RandomWalker(Agent):
    def __init__(self, unique_id, model, pos, anchor_point, gang):
        super().__init__(unique_id, model)
        self.pos = pos
        self.pos_eucldean = pos
        self.anchor_point = anchor_point
        self.gang = gang

    def random_move(self):
        """
        This method should determine the jump length and direction of a 
        specific agent and makes the move.
        """

        # neighbourhood = self.model.grid.get_neighborhood(self.pos, True)
        # new_pos = self.random.choice(neighbourhood)
        # self.model.grid.move_agent(self, new_pos)

        max_jump_length = self.determine_max_jump()
        jump_length = self.determine_jump_length(max_jump_length)
        pass

    def determine_max_jump(self):
        """
        Determines the upper bound fo the Bounded Pareto distribution.
        """

        x, y = self.pos
        road_dens = self.model.road_density[x, y]
        lowest_max_jump = self.model.parameters["lowest_max_jump"]
        highest_max_jump = self.model.parameters["highest_max_jump"]

        return (1 - road_dens) * highest_max_jump + lowest_max_jump

    def determine_jump_length(self, H):
        """
        Generates random number from a Bounded Pareto distribution
        """

        k = self.model.parameters["scale"]
        L = self.model.parameters["min_jump_length"]

        x = random.uniform(0, 1)
        U = ((1 - L ** k * x ** (-k)) / (1 - (L / H) ** k))
        number = ((-(U * H ** k - U * L ** k - H ** k) / (H ** k * L ** k)) ** 
                    (- 1 / k))

        return number

    def determine_bias(self):
        """
        Determines the bias of the direction the agents wants to move
        """

        gang_info = self.model.gang_info.copy()
        home_vector = 

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
