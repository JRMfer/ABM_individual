# Agents
# Agents-based modeling
# University of Amsterdam
# Julien Fer
#
# This script contains the functionality to represent gang members.

from mesa import Agent
import random
import numpy as np


class SBLN(Agent):
    def __init__(self, unique_id, model, pos, gang):
        super().__init__(unique_id, model)
        self.pos = pos
        self.gang = gang
        
    def random_move(self):
        """
        This method should determine the jump length and direction of a
        specific agent and makes the move.
        """

        while True:
            max_jump_length = self.determine_max_jump()
            jump_length = self.determine_jump_length(max_jump_length)
            bias = self.determine_bias()
            angle_bias = random.vonmisesvariate(bias,
                                                self.model.parameters["kappa"])

            pos_change = np.array([jump_length * np.cos(angle_bias),
                                jump_length * np.sin(angle_bias)])

            new_pos = np.array(self.pos) + pos_change

            if not self.model.area.out_of_bounds(new_pos):
                self.model.area.move_agent(self, tuple(new_pos))
                break

        # HIER MOET NOG EEN CHECK KOMEN OF DE AGENT NAAR EEN ANDERE REGIO
        # VERPLAATST
        pass

    def determine_max_jump(self):
        """
        Determines the upper bound fo the Bounded Pareto distribution.
        """

        x, y = self.pos
        road_dens = self.model.road_density[int(round(x)), int(round(y))]
        lowest_max_jump = self.model.parameters["lowest_max_jump"]
        highest_max_jump = self.model.parameters["highest_max_jump"]

        return (1 - road_dens) * highest_max_jump + lowest_max_jump

    def determine_jump_length(self, H):
        """
        Generates random number from a Bounded Pareto distribution
        """

        k = self.model.parameters["bounded_pareto"]
        L = self.model.parameters["min_jump_length"]

        x = random.uniform(0, 1)
        U = ((1 - L ** k * x ** (-k)) / (1 - (L / H) ** k))
        number = ((-(U * H ** k - U * L ** k - H ** k) / (H ** k * L ** k)) **
                  (- 1 / k))

        return number

    def determine_bias(self):
        """
        Determines the bias of the direction
        the agents wants to move
        """

        gang_info = self.model.gang_info.copy()
        bias_home = self.bias_to_home(gang_info)
        bias_rivals = self.bias_to_rivals(gang_info)
        bias_total = bias_home + bias_rivals
        x, y = bias_total
        if not x:
            return np.arctan(0)
        
        return np.arctan(y / x)

    def bias_to_home(self, gang_info):
        """
        Determines the bias towards or away
        the gang member's own set space.
        """

        home_coords = gang_info[self.gang]["anchor"]
        home_vector = np.array(home_coords) - np.array(self.pos)
        norm_home = np.linalg.norm(home_vector, ord=2)
        gang_info.pop(self.gang)
        weight_bias = self.model.parameters["weight_bias_home"]

        if not norm_home:
            return np.array([0.0, 0.0])

        return weight_bias * norm_home * home_vector / norm_home

    def bias_to_rivals(self, gang_info):
        """
        Determines the bias towards gang rivals.
        """

        bias_to_rivals = np.array([0.0, 0.0])
        contact_all_rivals = self.model.rivalry_matrix[self.gang, :].sum()

        for info in gang_info:
            contact_rival = self.model.rivalry_matrix[self.gang, info["name"]]
            rival_vector = (np.array(info["anchor"]) -
                            np.array(self.pos))
            norm_rival = np.linalg.norm(rival_vector)

            weight_bias = 0
            if contact_all_rivals and norm_rival:
                weight_bias = (contact_rival / contact_all_rivals) / norm_rival
                bias_to_rivals = (bias_to_rivals + weight_bias * rival_vector
                                  / norm_rival)

        return bias_to_rivals


class GangMember(SBLN):
    def __init__(self, unique_id, model, pos, gang):
        super().__init__(unique_id, model, pos, gang)

    def step(self):
        """
        Moves the gangster according a semi biased Levy model.
        """
        self.random_move()
        self.check_rivals()

    def check_rivals(self):
        """
        After moving checks for rivals
        and if found updates rivalry matrix.
        """

        # DIT IS EEN PARAMETER!! WILLEN WE WEL MET MOORE DISTANCE WERKEN??
        vision = 3  # self.model.parameters["vision"]
        poss_agents = self.model.area.get_neighbors(self.pos, vision,
                                                    include_center=True)

        for agent in poss_agents:
            if self.gang != agent.gang:
                self.model.update_rivalry(self, agent)
