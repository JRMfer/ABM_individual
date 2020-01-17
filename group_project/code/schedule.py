from mesa.time import RandomActivation
import random

class OneRandomActivation(RandomActivation):
    """
    """

    def step(self):
        """
        """
        for agent in self.agent_buffer(shuffled=True):
            agent.step()
            break
        self.steps += 1
        self.time += 1