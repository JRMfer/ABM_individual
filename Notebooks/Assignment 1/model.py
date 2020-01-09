import random

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation

from agents import Wolf, Sheep

def mean_wolf(model):
    """
    Determines mean sheep eaten by wolves over their lifetime.
    """
    
    sheap_eaten_wolf = sum([agent.total_eaten for agent in 
                            model.schedule_Wolf.agents])
    lifetime_wolves = sum([agent.age for agent in model.schedule_Wolf.agents])
    
    try:
        return sheap_eaten_wolf / lifetime_wolves
    except ZeroDivisionError:
        return 0

class WolfSheep(Model):
    '''
    Wolf-Sheep Predation Model
    '''
    
    def __init__(self, height=20, width=20,
                 initial_sheep=100, initial_wolves=30,
                 sheep_reproduction_chance=0.05, wolf_death_chance=0.05):

        super().__init__()

        self.height = height
        self.width = width
        self.initial_sheep = initial_sheep
        self.initial_wolves = initial_wolves
        self.sheep_reproduction_chance = sheep_reproduction_chance
        self.wolf_death_chance = wolf_death_chance

        # Add a schedule for sheep and wolves seperately to prevent 
        # race-conditions
        self.schedule_Sheep = RandomActivation(self)
        self.schedule_Wolf = RandomActivation(self)

        self.grid = MultiGrid(self.width, self.height, torus=True)
        self.datacollector = DataCollector(
             {"Sheep": lambda m: self.schedule_Sheep.get_agent_count(),
              "Wolves": lambda m: self.schedule_Wolf.get_agent_count(),
              "Mean": mean_wolf})

        # Create sheep and wolves
        self.init_population(Sheep, self.initial_sheep)
        self.init_population(Wolf, self.initial_wolves)

        # This is required for the datacollector to work
        self.running = True
        self.datacollector.collect(self)

    def init_population(self, agent_type, n):
        '''
        Method that provides an easy way of making a bunch of agents at once.
        '''
        for _ in range(n):
            x = random.randrange(self.width)
            y = random.randrange(self.height)

            self.new_agent(agent_type, (x, y))

    def new_agent(self, agent_type, pos):
        '''
        Method that creates a new agent, and adds it to the correct scheduler.
        '''
        agent = agent_type(self.next_id(), self, pos)

        self.grid.place_agent(agent, pos)
        getattr(self, f'schedule_{agent_type.__name__}').add(agent)

    def remove_agent(self, agent):
        '''
        Method that removes an agent from the grid and the correct scheduler.
        '''
        self.grid.remove_agent(agent)
        getattr(self, f'schedule_{type(agent).__name__}').remove(agent)

    def step(self):
        '''
        Method that calls the step method for each of the sheep, and then for 
        each of the wolves.
        '''
        self.schedule_Sheep.step()
        self.schedule_Wolf.step()

        # Save the statistics
        self.datacollector.collect(self)

    def run_model(self, step_count=200):
        '''
        Method that runs the model for a specific amount of steps.
        '''
        for _ in range(step_count):
            self.step()