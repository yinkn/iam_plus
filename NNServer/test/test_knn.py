import unittest
import sys

import numpy
from numpy import *

sys.path.append("../src")

from knn import calc_distance

class TestKNN(unittest.TestCase):
    def test_calc_distance_1(self):
        a = array([2,2,2,2])
        b = array([1,1,1,1])
        c = calc_distance(a, b)
        self.assertEqual(c, 2)

    def test_calc_distance_1(self):
        x1 = array([-52, -101, -30, 955, 172, 185, 1297])
        x2 = array([-32, -151, -48, 700, 164, 169, 191])
        x3 = array([-5, -52, -32, 765, 173, 195, 200])
        x4 = array([163, 345, 319, 478, 163, 170, 142])
        print(calc_distance(x1, x2))
        print(calc_distance(x2, x3))
        print(calc_distance(x3, x4))
        print(calc_distance(x4, x1))

        print(calc_distance(x1, x2))
        print(calc_distance(x1, x3))
        print(calc_distance(x1, x4))
       

if __name__ == '__main__':
    unittest.main()