import numpy as np
import scipy.linalg as sla

a = np.array([
            [0,1,0,0,0,0,0,0,0],  
            [0,0,1,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0],
            [0,0,0,0,1,0,0,0,0],
            [0,0,0,0,0,1,0,0,0],
            [0,0,0,0,0,0,1,0,0],
            [1,0,0,0,0,0,0,1,0],
            [0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0]
            ])

d, p = sla.eig(a)
d = np.diag(d)

for i in range(len(d)):
    u, v = a.dot(p[:,i]), d[i][i]*p[:,i]
    print(np.allclose(u, v))

print((p.T) .dot(p))

