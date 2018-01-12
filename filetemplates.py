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
}"""

circlecss = """circle {
        stroke: black;
        fill: white;   
}"""

linecss = """line {
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

def circle_JS(x, y, r, label):
        circlestring  = "<g>"
        circlestring += "<circle cx='" + str(x) + "' cy='" + str(y) + "' r='" + str(r) + "' id='" + label + "'/>"
        circlestring += "<text x='" + str(x) + "' y='" + str(y) + "'>" + label + "</text>"
        circlestring += "</g>"
        return "circle = " + '"' + circlestring + '"' + ';\n'


def line_JS(x1, y1, x2, y2, label):
        linestring  = "<g>" 
        linestring += "<line x1='0' y1='0' x2='200' y2='200'/>"
        linestring += "</g>"
        linestring += "<text x='" + str(x2 / 2) + \
                         "' y='" + str(y2 / 2 - 5) + "'>" + label + "</text>"
        
        return "line = " + '"' + linestring + '"' + ';\n'

def node_JS(x, y, r, label):
        nodejs = ""
        nodejs += circle_JS(x, y, r, label)
        nodejs += "document.getElementById('pane').innerHTML += circle;\n"
        return nodejs

def vertex_JS(node1ID, node2ID, weight, direction):
        vertexjs  = ""
        vertexjs += "element1 = document.getElementById('" + node1ID + "');\n"
        vertexjs += "element2 = document.getElementById('" + node2ID + "');\n"
        vertexjs += "console.log(element1);\n"
        vertexjs += "rect1 = element1.getBoundingClientRect();\n"
        vertexjs += "rect2 = element2.getBoundingClientRect();\n"
        vertexjs += "console.log(rect2);\n"
        vertexjs += "console.log(document.body.textContent);\n"
        vertexjs += line_JS(0, 0, 200, 200, weight)
        vertexjs += "document.getElementById('pane').innerHTML += line;\n"

        return vertexjs

################################################################################