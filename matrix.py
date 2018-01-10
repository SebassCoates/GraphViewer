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



