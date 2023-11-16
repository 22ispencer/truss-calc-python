import numpy as np
import scipy as sp
#                 AB   AD   BC   BD   CD   Ax   Ay   Cy
left = np.array([[4/5,  1,   0,    0,   0,   1,   0,   0],  # AX
                 [3/5,  0,   0,    0,   0,   0,   1,   0],  # AY
                 [-4/5, 0,   4/5,  0,   0,   0,   0,   0],  # BX
                 [-3/5, 0,   -3/5, -1,  0,   0,   0,   0],  # BY
                 [0,    0,   -4/5, 0,   -1,  0,   0,   0],  # CX
                 [0,    0,   3/5,  0,   0,   0,   0,   1],  # CY
                 [0,    -1,  0,    0,   1,   0,   0,   0],  # DX
                 [0,    0,   0,    1,   0,   0,   0,   0]])  # DY

right = np.array([0, 0, -12, -20, 0, 0, 0, 0])

solu = np.linalg.solve(left, right)
print(solu)
