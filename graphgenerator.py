################################################################################
#  Graph Viewer                                                                #
#  a lightweight graph visualizer for adjacency matrix data                    #
#  created by Sebastian Coates                                                 #
#                                                                              #
#  graphgenerator.py                                                           #
#  Generates graph data for layout testing                                     #
#                                                                              #
#  Copyright 2017 Sebastian Coates                                             #
#                                                                              #
#  Graph Viewer is free software: you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by        #
#  the Free Software Foundation, either version 3 of the License, or           #
#  (at your option) any later version.                                         #
#                                                                              #
#  Graph Viewer is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with Graph Viewer.  If not, see <http://www.gnu.org/licenses/>.       #
################################################################################

import numpy as np
import random as rand
import sys

def invalid_args():
        print("Invalid arguments given")
        print("Arg 1: number of nodes")
        print("Arg 2: max weight")

if len(sys.argv) != 3:
        invalid_args()
        quit()

num_nodes = int(sys.argv[1])
weight_range = int(sys.argv[2])

#likely not undirected
adjMatrix = np.random.randint(weight_range + 1, size=(num_nodes, num_nodes))

graphfile  = open("generatedgraph.txt", 'w')
labelsfile = open("generatedlabels.txt", 'w')

for row in range(num_nodes):
        for col in range(num_nodes):
                graphfile.write(str(adjMatrix[row][col]) + " ")

for num in range(num_nodes):
        labelsfile.write("node" + str(num) + " ")