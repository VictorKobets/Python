from sys import stdin
from copy import deepcopy
from functools import reduce


class MatrixError(BaseException):

    def __init__(self, matrix1, matrix2):
        self.matrix1 = matrix1
        self.matrix2 = matrix2


class Matrix:

    def __init__(self, list_of_list):
        self.matrix = deepcopy(list_of_list)

    def __str__(self):
        return('\n'.join(
            [reduce(
                lambda x, y: x + '\t' + y,
                map(
                    str,
                    line
                    )
                ) for line in self.matrix]
            )
        )

    def size(self):
        return(
            len(
                self.matrix
                ),
            len(
                self.matrix[0]
            )
        )

    def transpose(self):
        self.matrix = list(
            map(
                list,
                zip(*self.matrix)
                )
            )
        return(
            Matrix(
                self.matrix
                )
            )

    @staticmethod
    def transposed(x):
        return(
            Matrix(
                list(
                    map(
                        list,
                        zip(
                            *x.matrix
                            )
                        )
                    )
                )
            )

    def __add__(self, other):
        if self.size() == other.size():
            return(
                Matrix(
                    [
                        [
                            (self.matrix[i][j] + other.matrix[i][j])
                            for j in range(other.size()[1])
                            ]
                        for i in range(other.size()[0])
                        ]
                    )
                )
        else:
            raise MatrixError(self, other)

    def __mul__(self, k):
        return(
            Matrix(
                [
                    [
                        (self.matrix[i][j]*k)
                        for j in range(self.size()[1])
                        ]
                    for i in range(self.size()[0])
                    ]
                )
            )

    __rmul__ = __mul__


exec(stdin.read())
