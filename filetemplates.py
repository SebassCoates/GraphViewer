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
<body>
"""

htmlclose = """</body> 
</html>"""

def node_HTML(label):
        return '<div class="node" id="' + label + '">' + label + '</div>\n'
################################################################################


#############################CSS Code Templates#################################
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

################################################################################


#############################JS Code Templates##################################


################################################################################