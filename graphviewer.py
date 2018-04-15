################################################################################
#  Graph Viewer                                                                #
#  a lightweight graph visualizer for adjacency matrix data                    #
#  created by Sebastian Coates                                                 #
#                                                                              #
#  graphviewer.py                                                              #
#  Contains main script                                                        #
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

import webbrowser
import os
from sys import argv
from math import ceil, sqrt, tan, cos, sin, atan
import random as rand
import numpy  as np
from matrix import Matrix
from filetemplates import *

def display_help():
        print("--colors=")
        quit()

def invalid_args():
        print("Invalid arguments given")
        print("Expecting 2 files")
        print("File 1: whitespace delimited adjacency matrix data")
        print("File 2: whitespace delimited node labels")

#currently unused - all nodes sized the same
def calculate_sizes(adjMatrix, labels):
        dimen = adjMatrix.dimen

        connections = np.zeros((dimen), dtype='int32')
        sizes = {}
        total = 0
 
        for row in range(dimen):
                for col in range(dimen):
                        weight = adjMatrix.at(row, col)
                        connections[row] += weight 
                        connections[col] += weight 
                        total += weight 

        for i in range(len(labels)):
                sizes[labels[i]] = 15 * sqrt(connections[i] / total)

        return sizes

def calculate_positions(adjMatrix, labels):
        positions   = {} 
        r = 0
        c = 0
        nodesPerRow  = ceil(sqrt(len(labels)))
        blockSize = 100 / nodesPerRow
        sideOffset = blockSize / 2#.25 * nodesPerRow * blockSize
        topOffset = blockSize / 2.714
        while(r < nodesPerRow and r * nodesPerRow + c < len(labels)):
                positions[labels[r * nodesPerRow + c]] = Position(c * blockSize + sideOffset, r * blockSize + topOffset)
                c += 1
                if c == nodesPerRow:
                        c = 0
                        r += 1

        return (positions, calculate_sizes(adjMatrix, labels))

def divide_tree(adjMatrix, labels, root):
        depth = 0
        addedLayers = set()
        inQueue = [False for i in range(len(labels))]
        grid = []
        queue = [(root, depth)]
        
        while len(queue) > 0:
            node, depth = queue.pop(0)
            inQueue[node] = True
            if depth not in addedLayers:
                grid.append([node])
                addedLayers.add(depth)
            else:
                grid[depth].append(node)

            for neighbor in range(len(labels)):
                if adjMatrix.at(node, neighbor) > 0 and not inQueue[neighbor]:
                    queue.append((neighbor, depth + 1))
                    inQueue[neighbor] = True

        disconnected = [i for i, notAdded in enumerate(inQueue) if notAdded == False]
        grid.append(disconnected)

        return grid

def calculate_tree_positions(adjMatrix, labels, root):
        positions = {}
        grid = divide_tree(adjMatrix, labels, root)
        height = len(grid)
        maxWidth = max([len(level) for level in grid])

        nodeSize = min([100/height, 100/maxWidth])
        topOffset = nodeSize / 2.714
        
        for i in range(len(grid)):
            row = grid[i]
            sideOffset = 100 / (1 + len(row))
            for j in range(len(row)):
                positions[labels[row[j]]] = Position(j * nodeSize + sideOffset, i * nodeSize + topOffset)

        return positions, nodeSize / 4

def distance_between(position1, position2):
    deltax = position1.x - position2.x
    deltay = position1.y - position2.y
    return (sqrt((deltax ** 2) + (deltay ** 2)))

def angle_between(position1, position2):
    deltax = position1.x - position2.x
    deltay = position1.y - position2.y
    if deltax == 0:
        return 0
    return atan(deltay / deltax)

def force_adjust(adjMatrix, positions, iteration, velocities):
    STEP_DISTANCE = 1 #/ (iteration + 1) 
    deltaPositions = {}
    degrees = []
    for i in range(len(positions)):
        degrees.append(0)
        for j in range(len(positions)):
            degrees[i] += adjMatrix.at(i, j)

    for node in positions:
        deltaPositions[node] = Position(0,0)

    for node in positions: #nodes indexed by 1 in positions
        position = positions[node]
        deltaPosition = deltaPositions[node]
        for neighbor in range(len(positions)):
            is_neighbor = adjMatrix.at(int(node) - 1, neighbor) #Assumes node is int label indexed by one
            neighborPosition = positions[str(neighbor + 1)] 
            distance = distance_between(position, neighborPosition)
            to_right = position.x - neighborPosition.x > 0
            above    = position.y - neighborPosition.y > 0
            angle    = abs(angle_between(position, neighborPosition))
            scale    = degrees[int(node) - 1] + degrees[neighbor] + 1
            if is_neighbor == 0 and distance != 0:
                if to_right:
                    deltaPosition.x += scale * STEP_DISTANCE * cos(angle) / distance ** 2
                else:
                    deltaPosition.x -= scale * STEP_DISTANCE * cos(angle) / distance ** 2
                if above:
                    deltaPosition.y += scale * STEP_DISTANCE * sin(angle) / distance** 2
                else:
                    deltaPosition.y -= scale * STEP_DISTANCE * sin(angle) / distance** 2
            elif distance != 0:
                    deltaPosition.x += scale * STEP_DISTANCE * cos(angle) / distance ** 2
                    deltaPosition.y += scale * STEP_DISTANCE * sin(angle) / distance** 2

    for node in positions:
        vX, vY = velocities[int(node) -1 ] 
        vX += deltaPositions[node].x
        vY += deltaPositions[node].y
        velocities[int(node) - 1] = (vX, vY)
        newPositionX = positions[node].x + vX * STEP_DISTANCE
        newPositionY = positions[node].y + vY * STEP_DISTANCE
        size = 10
        if newPositionX > 0 + size and newPositionX < 100 - size:
            positions[node].x = newPositionX
        if newPositionY > 0 + size and newPositionY < 100 - size:
            positions[node].y = newPositionY

    return positions, velocities


def generate_HTML(adjMatrix, labels, options):
        generated = htmlopen + svgopen
        NUM_FORCES = 100 
    
        sizes = {}

        if options[0] == "NO_ROOT":
            (positions, sizes) = calculate_positions(adjMatrix, labels)
            #start from middle
            i = 0.0
            offset = 10
            for pos in positions:
                positions[pos] = Position(rand.randint(offset, 100 - offset), rand.randint(offset, 100 - offset))
                i += offset/len(positions)

            velocities = [(0,0) for l in labels] 
            for i in range(NUM_FORCES):
                positions, velocities = force_adjust(adjMatrix, positions, i, velocities)
                for position in positions:
                    pass
                    #print(positions[position].x)
                    #print(positions[position].y)
        else: 
            (positions, size) = calculate_tree_positions(adjMatrix, labels, options[0])
        

        for label in labels:
                x = positions[label].x
                y = positions[label].y
                if sizes == {}:
                    r = size
                else:
                    r = sizes[label]
                nodes[label] = Node(x, y, r, label)
                generated += node_JS(nodes[label]) 

        dimen = adjMatrix.dimen

        #Only supporting undirected graphs
        for row in range(dimen):
                for col in range(dimen):

                        bidirectional = adjMatrix.at(col, row) == adjMatrix.at(row,col)

                        if col > row and bidirectional: #draw vertex only once
                               continue #don't draw same vertex twice

                        if bidirectional:
                            generated += vertex_JS(nodes[labels[col]], 
                                                   nodes[labels[row]],
                                                   str(adjMatrix.at(row, col)),
                                                   0
                                                   )
                        else:
                            generated += vertex_JS(nodes[labels[col]], 
                                                   nodes[labels[row]],
                                                   str(adjMatrix.at(row, col)),
                                                   1
                                                   )

        return generated + svgclose +  htmlclose

def generate_CSS(adjMatrix, labels, options):
        generated  = svgcss + "\n\n" + nodecss + "\n\n" + circlecss + "\n\n" + linecss 
        generated += "\n\n" + textcss

        if options[1] != "NO_COLORS":
                color_labels = open(options[1], 'r').read().split()
                for i, color in enumerate(color_labels):
                        generated += add_node_color(labels[i], color)

        return generated

def generate_JS(adjMatrix, labels):
        generated = jsopen
        return generated + jsclose


##################################### MAIN #####################################
options = ["NO_ROOT", "NO_COLORS"]

if argv[1] in {'help', '--help', 'h', '--h'}:
        display_help()

if len(argv) < 3:
        invalid_args()
        quit()

try:
        inputdata = open(argv[1], "r").read()
except IOError:
        print('"' + argv[1] + '"' + " is invalid file (expecting adj matrix)")
        quit()

try:
        labeldata = open(argv[2], "r").read()
except IOError:
        print('"' + argv[2] + '"' + " is invalid file (expecting label info)")
        quit()

for arg in argv[3:]: #additional command line options handled here
    if "--root=" in arg:
        options[0] = int(arg.replace("--root=", ""))
    if "--colors=" in arg:
        options[1] = arg.replace("--colors=", "")


#files for viewing graph in browser
html = open("index.html", "w")
css  = open("index.css" , "w")
js   = open("index.js"  , "w")

rawdata   = inputdata.split()
try:
        adjMatrix = Matrix(rawdata)
except ValueError:
        print("Invalid graph data: dimensions non-square")
        quit()

labels = labeldata.split()
if len(labels) != adjMatrix.dimen:
        print("Error: number of labels does not match dimensions of adj matrix")
        quit()

htmlString = generate_HTML(adjMatrix, labels, options)
cssString  = generate_CSS(adjMatrix, labels, options)
jsString   = generate_JS(adjMatrix, labels)

html.write(htmlString)
css.write(cssString)
js.write(jsString)

htmlpath = os.path.abspath('index.html')
webbrowser.open('file://' +  htmlpath)
