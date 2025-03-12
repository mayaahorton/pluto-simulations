import yt
import numpy as np
import os
import copy

# This code is similar to the "findhotspots" code which also uses 
# feature tracking within velocity slices. However this is used for tracking
# a region of interest through the whole image cube. It can be quite memory 
# intensive and produces a lot of output that can take time to interpret.

def divergence(f):
    num_dims=len(f)
    return np.ufunc.reduce(np.add, [np.gradient(f[i], axis=i) for i in range(num_dims)])


os.chdir('events/chevron')

timestep=100

density=np.load('density_%04i.npy' % timestep)
emissivity=np.load('emissivity_%04i.npy' % timestep)
prs=np.load('pressure_%04i.npy' % timestep)
vx=np.load('vx_%04i.npy' % timestep)
vy=np.load('vy_%04i.npy' % timestep)
vz=np.load('vz_%04i.npy' % timestep)
div=divergence([vx,vy,vz])

bbox = np.array([[-0.3, 0.3], [-0.3, 0.3], [-0.3, 0.3]])
ds = yt.load_uniform_grid({'pressure':prs,'velocity_x':vx,'velocity_y':vy,'velocity_z':vz,'density':density,'emissivity':emissivity,'divergence':div}, vx.shape, 3.08e24, bbox=bbox, nprocs=64)

maxval, maxloc = ds.find_max('emissivity') 
print('Emissivity max is',maxloc)

for i in range(0,20):
#s = yt.SlicePlot(ds, 'z', ['density','pressure','emissivity'], center=[0.22,0.07,-0.01], width=(60, 'kpc'))
    depth=i*2e-3
    s = yt.SlicePlot(ds, 'z', ['density','pressure','emissivity','divergence'], center=[-0.025,-0.025,depth], width=(80, 'kpc'))
    s.annotate_velocity(factor=16) 
    s.save('t83_slice_z=%+f' % (1000*depth)) 


    s=yt.OffAxisSlicePlot(ds, np.cross(np.array([0.025,0.025,-depth]),np.array([1,0,0])), ["density","pressure","emissivity","divergence"], center=[-0.025,-0.025,depth],width=(80,'kpc'),north_vector=[0,1,0])
    s.annotate_cquiver('cutting_plane_velocity_x', 'cutting_plane_velocity_y',factor=16)
    s.save('t83_offax_z=%+f' % (1000*depth))
    
