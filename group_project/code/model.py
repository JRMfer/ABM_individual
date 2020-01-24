from mesa import Model
from mesa.space import ContinuousSpace
from mesa.datacollection import DataCollector
import matplotlib.pyplot as plt
import numpy as np
from agents import GangMember
from schedule import OneRandomActivation

GRID_DIM = [100, 100]

GANGS = [{"name": 0, "anchor": (21, 25), "gang_size": 21}, 
            {"name": 1, "anchor": (65, 77), "gang_size": 15}, 
            {"name": 2, "anchor": (22, 33), "gang_size": 19}]
PARS = {"min_jump_length": 0.1, "bounded_pareto": 1.1, "kappa": 3.5, 
        "weight_bias_home": 1, "highest_max_jump": 200, 
        "lowest_max_jump": 100}

class GangRivalry(Model):
    """
    """

    def __init__(self, grid_size=GRID_DIM, gang_info=GANGS, pars=PARS):
        super().__init__()

        self.width, self.height = grid_size
        self.area = ContinuousSpace(self.width, self.height, False)
        self.gang_info = gang_info
        self.parameters = pars
        self.total_gangs = len(self.gang_info)
        self.rivalry_matrix = np.zeros((self.total_gangs, self.total_gangs))
        self.road_density = np.random.rand(self.width, self.height)
        self.schedule_GangMember = OneRandomActivation(self)
        self.init_population()
        self.datacollector = DataCollector(
            {"Interaction": lambda m: self.schedule_GangMember.get_agent_count()
            })
        self.running = True
        self.datacollector.collect(self)

    def init_population(self):
        """
        """
        for gang in self.gang_info:
            size = gang["gang_size"]
            pos = gang["anchor"]
            name = gang["name"]

            for _ in range(size):
                self.new_agent(pos, name)
    
    def new_agent(self, pos, name):
        """
        """
        agent = GangMember(self.next_id(), self, pos, name)
        self.area.place_agent(agent, pos)
        self.schedule_GangMember.add(agent)
        
    def update_rivalry(self, agent1, agent2):
        """
        """
        self.rivalry_matrix[agent1.gang, agent2.gang] += 1

    def step(self):
        self.schedule_GangMember.step()
        self.datacollector.collect(self)

    def run_model(self, step_count=200):
        for _ in range(step_count):
            self.step()

if __name__ == "__main__":
    model = GangRivalry()
    model.run_model()

    data = model.datacollector.get_model_vars_dataframe()
    data.plot()
    plt.show()