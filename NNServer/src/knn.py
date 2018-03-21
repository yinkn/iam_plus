import math
import numpy as np

def calc_distance(a, b):
    c = np.power(a - b, 2)
    #print c
    d2 = np.sum(c)
    #print d2
    return math.sqrt(d2)
