################################################################################
#  Graph Viewer                                                                #
#  a lightweight graph visualizer for adjacency matrix data                    #
#  created by Sebastian Coates                                                 #
#                                                                              #
#  matrix.py                                                                   #           
#  Contains Class for abstracting matrix data                                  #
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

class Matrix:
        def __init__(self, datalist):
                dimen = int(len(datalist) ** (.5))

                if dimen * dimen != len(datalist):
                        raise ValueError("Data for matrix is non-square")

                self.dimen = dimen
                self.matrix = np.zeros((dimen, dimen), dtype='int32')
                col = 0
                row = 0

                for val in datalist:
                        self.matrix[row][col] = int(val)
                        col += 1
                        if col == dimen:
                                col = 0
                                row += 1

        def get_dimen(self):
                return self.dimen

        def print(self):
                for i in range(self.dimen):
                        for j in range(self.dimen):
                                print(self.matrix[i][j], end=' ')
                        print()

        def map(self, function):
                for i in range(self.dimen):
                        for j in range(self.dimen):
                                function(i, j, self.matrix[i][j])



