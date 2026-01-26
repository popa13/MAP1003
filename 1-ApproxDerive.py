import numpy as np
import math

##################################

# Create the variables
a = 0 
h = 0.1
f = math.e**a 
fph = math.e**(a + h)

#  Calculate the approximation
#    of the derivative
appD = (fph - f)/h

# Print the result 
print(appD)

print("------------------------")

# Print the results for multiple h
H = [10**(-k) for k in range(1, 20)]

for h in H:
	print("Valeur de h:" + str(h)) 
	appD = (math.e**(a + h) - math.e**a)/h
	print("Valeur approx. de la dérivée:" + str(appD))
	print("-----------------------------")
