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
import sys
import random as rand
import numpy  as np
from matrix import Matrix
from filetemplates import *

def invalid_args():
        print("Invalid arguments given")
        print("Expecting 2 files")
        print("File 1: whitespace delimited adjacency matrix data")
        print("File 2: whitespace delimited node labels")

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
                sizes[labels[i]] = 25 * connections[i] / total

        return sizes

def recursive_position(direction):
        pass

def calculate_positions(adjMatrix, labels, sizes):
        positions   = {} 
        sortedSizes = sorted(sizes.items(), key=lambda x:x[1], reverse=True)
        
        positions[sortedSizes[0][0]] = Position(50, 50)
        i = 1
        numlabels  = len(labels)
        while(i < numlabels):
                positions[sortedSizes[i][0]] = Position(rand.randint(5, 95), \
                                                        rand.randint(5, 95))
                i += 1

        return positions

def generate_HTML(adjMatrix, labels):
        generated = htmlopen + svgopen
        return generated + svgclose +  htmlclose

def generate_CSS(adjMatrix, lables):
        generated  = svgcss + "\n\n" + nodecss + "\n\n" + circlecss + "\n\n" + linecss 
        generated += "\n\n" + textcss

        return generated

def generate_JS(adjMatrix, labels):
        generated = jsopen

        sizes = calculate_sizes(adjMatrix, labels)
        positions = calculate_positions(adjMatrix, labels, sizes)

        for label in labels:
                x = positions[label].x
                y = positions[label].y
                r = sizes[label]
                nodes[label] = Node(x, y, r, label)
                generated += node_JS(nodes[label]) 

        dimen = adjMatrix.dimen

        #Only supporting undirected graphs
        for row in range(dimen):
                for col in range(dimen):
                        if adjMatrix.at(col, row) != 0:
                                if adjMatrix.at(col, row) != adjMatrix.at(row, col):
                                        print("Warning: only undirected graphs supported currently")

                        if col > row: #draw vertex only once
                                continue

                        generated += vertex_JS(nodes[labels[col]], 
                                               nodes[labels[row]],
                                               str(adjMatrix.at(row, col)),
                                               "0"
                                               )


        return generated + jsclose

args = sys.argv
if len(args) != 3:
        invalid_args()
        quit()

try:
        inputdata = open(args[1], "r").read()
except IOError:
        print('"' + args[1] + '"' + " is invalid file (expecting adj matrix)")
        quit()

try:
        labeldata = open(args[2], "r").read()
except IOError:
        print('"' + args[2] + '"' + " is invalid file (expecting label info)")
        quit()

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

htmlString = generate_HTML(adjMatrix, labels)
cssString  = generate_CSS(adjMatrix, labels)
jsString   = generate_JS(adjMatrix, labels)

html.write(htmlString)
css.write(cssString)
js.write(jsString)

htmlpath = os.path.abspath('index.html')
webbrowser.open('file://' +  htmlpath)
