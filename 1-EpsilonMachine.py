import math
import numpy as np

N = 60

for i in np.arange(1, N, 1):
	y = 1/2**(i)
	print("Puissance = "+ str(-i))
	print("Difference 1 et 1 + 2^{-i} = " + str(-1 + (1 + y)))
	print("--------------------------------------")
