from math import floor
from typing import Tuple, Callable, Union, List
from numbers import Number
from numpy import (matrix, arange)
from numpy.linalg import matrix_rank

from mesp.utilities.mesp_data import MespData

class BoundChooser:

    def __init__(self, C: matrix, default_algo):
        self.C : MespData = MespData(C)
        # self.rule_checker(default_algo)
        self.default_algo = default_algo
        self.algorithm_dict = None

    def rule_checker(self, bounding_algo):
        """
        Ensures the provided bounding algorithm can accept a MespData object and an integer
        and that it returns either a tuple of the bound value, associated relaxed solution,
        and runtime, or a tuple with those three ojects and the two dual vectors associated 
        with the relaxed approximation.
        """
        s = floor(self.C.n / 2)
        try:
            # returned = bounding_algo(self.C, s)
            if len(returned) != 3 or len(returned) != 5:
                raise ValueError("The provided bounding algorithm didn't return the required number of arguments")
            elif len(returned) == 3 or len(returned) == 5:
                if not isinstance(returned[0], Number):
                    raise ValueError("The first returned argument (the bound) is not a Number.")
                if not isinstance(returned[1], List[float]):
                    raise ValueError("The second returned argument (x) is not a list of floats.")
                if not isinstance(returned[2], Number):
                    raise ValueError("The third returned argument (runtime) is not a Number.")
            if len(returned) == 5:
                if not isinstance(returned[3], List[float]):
                    raise ValueError("The fourth returned argument (w) is not a list of floats.")
                if not isinstance(returned[5], List[float]):
                    raise ValueError("The fifth returned argument (v) is not a list of floats.")
        except:
            raise ValueError("The provided bounding algorithm could not accept the required arguments")

    

    def get_bound(self, s: int) -> Callable[
                      ...,
                       Union[Tuple[float, List[float], float],
                            Tuple[float, List[float], float, List[float], List[float]]
                       ]]:
        if s == 0 or s > min(self.C.d, self.C.n - 1):
            raise ValueError("Improper s value. Please choose an s value according to 0 < s <= min\{rank C, n - 1\}")
        
        if self.algorithm_dict == None:
            return self.default_algo
        else:
            try:
                algo = self.algorithm_dict[self.C.n][s]
                return algo
            except:
                return self.default_algo
