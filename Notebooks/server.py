from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule

# Import the implemented classes
import IPython
import os
import sys

# Change stdout so we can ignore most prints etc.
orig_stdout = sys.stdout
sys.stdout = open(os.devnull, 'w')
IPython.get_ipython().magic("run Mesa_introduction.ipynb")
sys.stdout = orig_stdout

# You can change this to whatever ou want. Make sure to make the different types
# of agents distinguishable
def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Color": "blue" if type(agent) is Wolf else "green",
                 "Filled": "true",
                 "Layer": 0,
                 "r": 0.5}
    return portrayal

# Create a grid of 20 by 20 cells, and display it as 500 by 500 pixels
grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)

# Create a dynamic linegraph
chart = ChartModule([{"Label": "Sheep",
                      "Color": "green"},
                      {"Label": "Wolves",
                      "Color": "red"}],
                    data_collector_name='datacollector')

# Create the server, and pass the grid and the graph
server = ModularServer(WolfSheep,
                       [grid, chart],
                       "WolfSheep Model",
                       {})

server.port = 8521

server.launch()
