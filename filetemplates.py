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
        <link href="https://fonts.googleapis.com/css?family=Anton" rel="stylesheet"> 
</head>
<body onload=load()>
"""

htmlclose = """</body> 
</html>"""

svgopen = "<div id='svg-container' style='width:100%;height:100%;'><svg height='100%' width='100%' id='pane' viewBox='0 0 100 100' preserveAspectRatio='none'>" #
svgclose = "</svg></div>"

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
        background-color: rgb(255,219,169);
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
        fill: rgb(163,217,119);   
        padding: 0px;
        margin: 0px;
        stroke-width: .5;
}"""

linecss = """line {
        padding: 0px;
        margin: 0px;
        stroke: black;
        stroke-width: .3;
}
polygon {
        padding: 0px;
        margin: 0px;
        stroke: black;
        stroke-width: .3;
}
"""

textcss = """text {
        dy: .3em;
        text-anchor: middle;
        fill: white;
        font-size: .3;
        font-weight: 400;
        font-family: 'Anton', sans-serif;

}

.linetext {
        fill: rgb(58, 166, 221);
        font-size: 4;
}

.circletext {
        fill: black;
}"""
################################################################################


#############################JS Code Templates##################################
jsopen = "function load() {\n"
 
jsclose = "\n}"

nodes = {} #to maintain set of node objects

class Position:
        def __init__(self, x, y):
                self.x = x
                self.y = y

class Node:
        def __init__(self, x, y, r, label):
                self.x = x
                self.y = y
                self.r = r
                self.label = label

def circle_JS(x, y, r, label):
        circlestring  = "<g>"
        circlestring += "<circle id='" + label + "' " + "cx='" + str(x) + "' cy='" + str(y) + "' r='" + str(r) + "' id='" + label + "'/>"
        circlestring += "<text x='" + str(x) + "' y='" + str(y + 1) + "' font-size='" + str(r / 18) + "vw' class='circletext'>" + label + "</text>"
        circlestring += "</g>"
        return circlestring

def add_node_color(nodeID, color):
        return "#" + nodeID + "{\n" + "stroke: " + color + ";\n}\n"

#Coords of line
def arrow_JS(x1, y1, x2, y2):
        arrowSize = .70#((y2 - y1) ** 2 +  (x2 - x1) ** 2) ** .5
        slope = (y2 - y1) / (x2 - x1)
        tangent = -1 / slope

        arrow = '<polygon points="'
        arrow += str(x1) + ',' + str(y1) + " "
        if x2 < x1:
            newX = x1 - arrowSize
            newY = y1 - arrowSize * slope
            arrow += str(newX + arrowSize) + ',' + str(newY + arrowSize * tangent) + " "
            arrow += str(newX - arrowSize) + ',' + str(newY - arrowSize * tangent)
        else:
            newX = x1 + arrowSize
            newY = y1 + arrowSize * slope
            arrow += str(newX + arrowSize) + ',' + str(newY + arrowSize * tangent) + " "
            arrow += str(newX - arrowSize) + ',' + str(newY - arrowSize * tangent)
        arrow += '"/>'
        return arrow

def line_JS(x1, y1, x2, y2, label):
        linestring  = "<g>" 
        linestring += "<line x1='" + str(x1) + "' y1='" + str(y1) + "' x2='" + str(x2) + "' y2='" + str(y2) + "'/>"
        linestring += "</g>"

        if (x2 < x1):
                x1, x2 = x2, x1
        if (y2 < y1):
                y1, y2 = y2, y1

        linestring += "<text x='" + str(x1 + abs(x2 - x1) / 2.0) + \
                         "' y='" + str(y1 + abs(y2 - y1) / 2.0) + "'  font-size='" + str(4) + "' class='linetext'>" + label + "</text>"
        
        return linestring

def node_JS(node):
        nodejs = circle_JS(node.x, node.y, node.r, node.label)  
        return nodejs

def vertex_JS(node1, node2, weight, direction):
        if weight == "0":
                return ""
        
        if node1 == node2:
                print('warning: self-loops not yet supported')
                return "" 

        deltaX = node1.x - node2.x
        deltaY = node1.y - node2.y

        angle = abs(atan2(deltaY, deltaX))

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

        vertexjs = line_JS(x1, y1, x2, y2, weight)
        if direction:
            vertexjs += arrow_JS(x1, y1, x2, y2)

        return vertexjs

################################################################################