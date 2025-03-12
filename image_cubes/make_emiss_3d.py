import sys
import numpy as np

imin=int(sys.argv[1])
try:
    imax=int(sys.argv[2])
except:
    imax=imin+1

for i in range(imin,imax):
    
    p=np.load('pressure_%04i.npy' % i)
    t=np.load('tracer_%04i.npy' % i)

    e=np.where(t==0,0,p**(7.2/4.0))
    np.save('emissivity_%04i.npy' % i,e)
