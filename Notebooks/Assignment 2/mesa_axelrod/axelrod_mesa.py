import random
import axelrod as axl
from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from agent import Player


class MesaAxelrod(Model):
    def __init__(self, height=20, width=20, players=100, strategies=[axl.Random, axl.TitForTat, axl.Grudger]):
        super().__init__()

        self.height = height
        self.width = width

        # add a scheduler
        self.scheduler = RandomActivation(self)

        # add a grid
        self.grid = MultiGrid(self.width, self.height, torus=True)

        # random players
        for i in range(players):
            x = random.randrange(self.width)
            y = random.randrange(self.height)

            strategy = random.choice(strategies)

            self.new_agent((x, y), strategy)

    def new_agent(self, pos, strategy):
        """
        Method that creates a new agent, and adds it to the correct scheduler.
        """
        agent = Player(self.next_id(), self, pos, strategy)

        self.grid.place_agent(agent, pos)
        self.scheduler.add(agent)

    def remove_agent(self, agent):
        """
        Method that removes an agent from the grid and the correct scheduler.
        """
        self.grid.remove_agent(agent)
        self.scheduler.remove(agent)

    def step(self):
        """
        step through all agents and step()
        self-implemented scheduler that allows removal of agents during stepping
        """
        agents = self.scheduler._agents

        agent_keys = list(agents.keys())
        for key in agent_keys:
            if key in agents:
                agents[key].step()

    def run_model(self, step_count=200):
        """
        Method that runs the model for a specific amount of steps.
        """
        for i in range(step_count):
            self.step()
