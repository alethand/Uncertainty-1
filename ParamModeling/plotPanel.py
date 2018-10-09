# -*- coding: utf-8 -*
from numpy import arange, sin, pi
import matplotlib.pyplot as plt
import os
import networkx as nx

def showPanel(paPanel):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    G = nx.DiGraph()  # G
    # G.add_node(1, time='5pm')
    for index in paPanel.paramsName:
        G.add_node(index)
    for index in paPanel.effect:
        G.add_edge(index[0],index[1])


    nx.Graph.to_directed(G)

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=1000, font_size=15, font_color='b', node_color='#CCECFF',
            edge_color='r')
    # os.remove("ba.png")
    plt.savefig("ba.png")
    # plt.show()


