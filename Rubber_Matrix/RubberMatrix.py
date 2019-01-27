from math import sqrt
from collections import Iterable


class Matrix:
    MAX_SIZE = 1000

    def __init__(self, max_size=None):
        self.matrix = [None]
        self.size = len(self.matrix)
        self.size_n = int(sqrt(self.size))
        if max_size != None:
            self.MAX_SIZE = max_size

    def append(self, element=None):
        if element is not None:
            # Declare to facilitate reading the code
            matrix = self.matrix
            size = self.size
            size_n = self.size_n
            try:
                # Error condition
                if matrix.count(None) == 0:
                    raise IndexError
                new_el_pos = matrix.index(None)
                matrix[new_el_pos] = element
                # Condition for expanding matrix
                if (new_el_pos == size-size_n and
                        size_n < self.MAX_SIZE):
                    # Expanding matrix
                    matrix.extend(
                        [None for _ in range(2*self.size_n+1)]
                        )
                    # Update matrix data
                    self.size = len(matrix)
                    self.size_n = int(sqrt(self.size))
            except IndexError as err:
                # Print error message
                print(
                    'There is no place in the matrix!',
                    err
                    )
                raise

    def pop(self):
        # Declare to facilitate reading the code
        matrix = self.matrix
        size = self.size
        size_n = self.size_n
        try:
            # Error condition
            if size == 1 and matrix[0] == None:
                raise IndexError
            # Replace element
            if matrix.count(None) == 0:
                last_el_apd = matrix[-1]
                matrix[-1] = None
                return last_el_apd
            else:
                last_el_apd_pos = matrix.index(None)
                last_el_apd = matrix[last_el_apd_pos-1]
                matrix[last_el_apd_pos-1] = None
                # For constriction matrix
                size_new = (size_n-1)**2
                if size_new-(size-matrix.count(None)) == size_n-1:
                    for _ in range(size-size_new):
                        del matrix[-1]
                    # Update matrix data
                    self.size = len(matrix)
                    self.size_n = int(sqrt(self.size))
                return last_el_apd
        except IndexError as err:
            # Print error message
            print(
                'You can not delete the last element of the matrix',
                err
                )
            raise

    def __str__(self):
        matrix_string = ''
        for index, value in enumerate(self.matrix):
            if (index+1)%self.size_n == 0 and (index+1) != self.size:
                matrix_string += str(value)+'\n'
            else:
                matrix_string += str(value)+' '
        return matrix_string

    @classmethod
    def from_iter(cls, iter_obj, max_size=None):
        # Error condition
        isinstance(iter_obj, Iterable)
        matrix = cls(max_size=max_size)
        for i in iter_obj:
            matrix.append(i)
        return matrix
