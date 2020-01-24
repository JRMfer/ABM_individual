from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from axelrod_mesa import MesaAxelrod


# A simple server that visualizes the three different strategies over time
def agent_portrayal(agent):
    cmap = {'Grudger': 'red',
            'Tit For Tat': 'green',
            'Random: 0.5': 'orange'}

    portrayal = {"Shape": "circle",
                 "Color": cmap[str(agent.strategy)],
                 "Filled": "true",
                 "Layer": 0,
                 "r": 0.5}

    return portrayal

grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)
server = ModularServer(MesaAxelrod,
                       [grid],
                       "mesa + axelrod",
                       {})

server.port = 8521
server.launch()
