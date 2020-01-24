import axelrod as axl
from mesa import Agent
import random


class Player(Agent):
    """
    A Player (agent), that walk around the grid. When meeting another agent it plays the iterative prisonners
    dilemma, and the winner reproduces, the loser dies!
    """
    def __init__(self, unique_id, model, pos, strategy):
        super().__init__(unique_id, model)

        self.strategy = strategy()

        self.pos = pos

    def random_move(self):
        """
        Step into a random direction.
        """
        possible_moves = self.model.grid.get_neighborhood(self.pos, moore=True, radius=1)

        new_pos = random.choice(possible_moves)

        self.model.grid.move_agent(self, new_pos)

    def play(self):
        """
        Select a single other player on your location, play with it, and the winner reproduces, loser dies...
        """
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=True, radius=0)
        neighbors = [neighbor for neighbor in neighbors if neighbor != self]

        if len(neighbors) > 0:
            random_neighbour = random.choice(neighbors)
            match = axl.Match((self.strategy, random_neighbour.strategy), turns=10)
            match.play()
            winner = match.winner()
            if winner:
                x = random.randrange(self.model.width)
                y = random.randrange(self.model.height)

                if self.strategy == winner:
                    self.model.remove_agent(random_neighbour)
                    self.model.new_agent((x, y), self.strategy.__class__)
                    self.strategy.reset()
                else:
                    self.model.new_agent((x, y), random_neighbour.strategy.__class__)
                    random_neighbour.strategy.reset()
                    self.model.remove_agent(self)

    def step(self):
        """
        walk around, and play prisonners dilemma
        """
        self.random_move()
        self.play()
