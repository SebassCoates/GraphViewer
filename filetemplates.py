################################################################################
#  Graph Viewer                                                                #
#  a lightweight graph visualizer for adjacency matrix data                    #
#  created by Sebastian Coates                                                 #
#                                                                              #
#  filetemplates.py                                                            #           
#  Contains useful string consts/classes for html/css/js file writing          #
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

from math import atan2

trig45 = 2 ** .5 / 2.0

#############################HTML Code Templates################################
htmlopen = """<!doctype html>\
<html>
<head>
        <title>Graph Viewer</title>\
        <meta charset="utf-8"/>
        <link rel="stylesheet" href="index.css"/>
        <script src="index.js"></script>
</head>
<body onload=load()>
"""

htmlclose = """</body> 
</html>"""

svgopen = "<svg height='100%' width='100%' id='pane'>"
svgclose = "</svg>"

def node_HTML(label):
        return '<div class="node" id="' + label + '">' + label + '</div>\n'
################################################################################


#############################CSS Code Templates#################################
svgcss = """html, body { 
        margin:0; 
        padding:0; 
        overflow:hidden 
}

svg { 
        position:fixed;
        top:0; 
        bottom:0; 
        left:0; 
        right:0;
        margin:0px;
        padding:0px;
        background-color: rgb(225,225,225);
}"""

nodecss = """.node {
        border-style: solid;
        border-color: black;
        text-align: center;
        vertical-align: middle;
        width: 100px;
        height: 100px;
        -moz-border-radius: 50%;
        -webkit-border-radius: 50%;
        border-radius: 50%;
        padding: 0px;
        margin: 0px;
}"""

circlecss = """circle {
        stroke: black;
        fill: white;   
        padding: 0px;
        margin: 0px;
}"""

linecss = """line {
        padding: 0px;
        margin: 0px;
        stroke: black;
        stroke-width: 2;
}"""

textcss = """text {
        dy: .3em;
        text-anchor: middle;
}"""
################################################################################


#############################JS Code Templates##################################
jsopen = "function load() {\n"

jsclose = "}"

nodes = {} #to maintain set of node objects

class Node:
        def __init__(self, x, y, r, label):
                self.x = x
                self.y = y
                self.r = r
                self.label = label

def circle_JS(x, y, r, label):
        circlestring  = "<g>"
        circlestring += "<circle cx='" + str(x) + "%' cy='" + str(y) + "%' r='" + str(r) + "%' id='" + label + "'/>"
        circlestring += "<text x='" + str(x) + "%' y='" + str(y) + "%' font-size='" + str(r / 1.8) + "vw'>" + label + "</text>"
        circlestring += "</g>"
        return "circle = " + '"' + circlestring + '"' + ';\n'


def line_JS(x1, y1, x2, y2, label):
        linestring  = "<g>" 
        linestring += "<line x1='" + str(x1) + "%' y1='" + str(y1) + "%' x2='" + str(x2) + "%' y2='" + str(y2) + "%'/>"
        linestring += "</g>"

        if (x2 < x1):
                x1, x2 = x2, x1
        if (y2 < y1):
                y1, y2 = y2, y1

        linestring += "<text x='" + str(x1 + abs(x2 - x1) / 2.0) + \
                         "%' y='" + str(y1 + abs(y2 - y1) / 2.0 - .33) + "%'  font-size='" + str(2) + "vw'>" + label + "</text>"
        
        return "line = " + '"' + linestring + '"' + ';\n'

def node_JS(node):
        nodejs = circle_JS(node.x, node.y, node.r, node.label)
        nodejs += "document.getElementById('pane').innerHTML += circle;\n"
        return nodejs

def vertex_JS(node1, node2, weight, direction):
        if weight == "0":
                return ""
        
        if node1 == node2:
                print('warning: self-loops not yet supported')
                return "" 

        deltaX = node1.x - node2.x
        deltaY = node1.y - node2.y

        # directionRatio = float(deltaY) / float(deltaX)
        angle = abs(atan2(deltaY, deltaX))
        
        if angle < .75 or angle > 2.5:
                if deltaX < 0:
                        x1 = node1.x + node1.r
                        x2 = node2.x - node2.r    
                else: 
                        x1 = node1.x - node1.r
                        x2 = node2.x + node2.r

                y1 = node1.y
                y2 = node2.y    

        elif angle >= .75 and angle < 1.25 or angle <= 2.5 and angle > 2:
                if deltaX < 0:
                        x1 = node1.x + node1.r * trig45
                        x2 = node2.x - node2.r * trig45
                else: 
                        x1 = node1.x - node1.r * trig45
                        x2 = node2.x + node2.r * trig45

                if deltaY < 0:
                        y1 = node1.y + node1.r * trig45
                        y2 = node2.y - node2.r * trig45
                else: 
                        y1 = node1.y - node1.r * trig45
                        y2 = node2.y + node2.r * trig45

        else: 
                if deltaY < 0:
                        y1 = node1.y + node1.r
                        y2 = node2.y - node2.r
                else: 
                        y1 = node1.y - node1.r
                        y2 = node2.y + node2.r

                x1 = node1.x
                x2 = node2.x

        


        vertexjs = line_JS(x1, y1, x2, y2, weight)
        vertexjs += "document.getElementById('pane').innerHTML += line;\n"

        return vertexjs

################################################################################