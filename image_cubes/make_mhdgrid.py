from pluto_output import Pluto_Output
import numpy as np
from multiprocessing import Pool
import psutil
import os
import sys

def get_physical_cpus():
    return psutil.cpu_count(logical=False)

def getcpus():
    nodefile=os.getenv('PBS_NODEFILE')
    if nodefile:
        lines=len(open(nodefile).readlines())
        return lines
    else:
        return get_physical_cpus()

def convert_pos(xy):
    # assume here that we do all of the z for a given x,y
    # thus we calculate r,phi,theta for all x,y,z
    # and use these to index into the pluto array
    # for the chosen projection the equator is in the x,y plane and so we are looking down on the pole
    # theta is the polar angle, phi is the azimuthal angle
    
    # input x and y are pixel co-ordinates and so first convert to WCS
    x,y=xy # unpack xy tuple
    rbound_l,rbound_h=p.bounds[1]
    xd=(x-pixels)*p.spacing[0]
    yd=(y-pixels)*p.spacing[0]
    maxz=pixels*p.spacing[0]
    zd=np.linspace(-maxz,maxz,vsize)
    r=np.sqrt(xd**2.0+yd**2.0+zd**2.0)
    theta=np.arccos(zd/r)
    phi=np.arctan2(yd,xd)
    rindex=np.rint((r-rbound_l)/p.spacing[0]).astype(int)
    mask=(rindex>=0) & (rindex<d.shape[2])
    rindex[~mask]=0
    thindex=np.rint(theta/p.spacing[1]).astype(int)
    thindex=np.where(thindex<d.shape[1],thindex,d.shape[1]-1)
    thindex=np.where(thindex>=0,thindex,0)
    phindex=np.rint(phi/p.spacing[2]).astype(int)
    nslice=d[phindex,thindex,rindex]
    #return np.where(mask,nslice,0)
    return x,y,np.where(mask,nslice,nullvalue)

# work round cluster affinity bug, should have no effect elsewhere
os.system("taskset -p 0xFFFFFFFF %d" % os.getpid())

p=Pluto_Output('/beegfs/car/mayaahorton/PLUTO/problems/precessing/parameter_study/45_100_1_MHD')

if ':' in sys.argv[1]:
    bits=sys.argv[1].split(':')
    mini=int(bits[0])
    maxi=int(bits[1])
else:
    mini=int(sys.argv[1])
    maxi=mini+1
for i in range(mini,maxi):
    for v in sys.argv[2:]:
        v=int(v)
        name={0:'density',1:'mach',7:'pressure',8:'tracer'}[v]
        nullvalues={0:1,1:0,7:0,8:0}
        outfile='/beegfs/car/mayaahorton/PLUTO/problems/precessing/visuals/VHR/45_100_1_MHD/%s_%04i.npy' % (name,i)
        if os.path.isfile(outfile): continue
        multi=True
        print i,v
        d=p.map_dbl(i,v)
        print d.shape
        pixels=512
        vsize=2*pixels+1
        nullvalue=nullvalues[v]
        volume=np.zeros((vsize,vsize,vsize),dtype=np.float32)
        if multi:
            xy=[]
        else:
            results=[]

        for x in range(vsize):
            if not(multi):
                print x
            for y in range(vsize):
                if multi:
                    xy.append((x,y))
                else:
                    results.append(convert_pos((x,y)))
        if multi:
            pool=Pool(getcpus())
            results=pool.map(convert_pos,xy)

        for x,y,v in results:
                volume[:,y,x]=v

        np.save(outfile,volume)
        del(d)
        if multi:
            del(pool)
        
