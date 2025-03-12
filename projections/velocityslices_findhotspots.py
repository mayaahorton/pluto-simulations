import yt
import numpy as np
import os
import copy

def divergence(f):
    """ 
    Computes the divergence of the vector field f, corresponding to dFx/dx + dFy/dy + ... 
    :param f: List of ndarrays, where every item of the list is one dimension of the vector field 
    :return: Single ndarray of the same shape as each of the items in f, which corresponds to a scalar field 
     """
    num_dims = len(f)
    return np.ufunc.reduce(np.add, [np.gradient(f[i], axis=i) for i in range(num_dims)])

os.chdir('/beegfs/car/mayaahorton/PLUTO/problems/precessing/visuals/events/splatter')

timestep=130

print('Reading the data')
density=np.load('density_%04i.npy' % timestep)
emissivity=np.load('emissivity_%04i.npy' % timestep)
prs=np.load('pressure_%04i.npy' % timestep)
vx=np.load('vx_%04i.npy' % timestep)
vy=np.load('vy_%04i.npy' % timestep)
vz=np.load('vz_%04i.npy' % timestep)
divergence=divergence([vx,vy,vz])

print('Making the YT structure')
bbox = np.array([[-0.3, 0.3], [-0.3, 0.3], [-0.3, 0.3]])
ds = yt.load_uniform_grid({'pressure':prs,'velocity_x':vx,'velocity_y':vy,'velocity_z':vz,'density':density,'emissivity':emissivity,'divergence':divergence}, vx.shape, 3.08e24, bbox=bbox, nprocs=64)

os.chdir('/beegfs/car/mayaahorton/PLUTO/problems/precessing/visuals/events/splatter') # change me
print('Now making plots, hurrah!')

#maxval, maxloc = ds.find_max('emissivity') 

# Find max for the whole region...
#coords=np.array(np.unravel_index(emissivity.argmax(),prs.shape))
#maxloc=ds.arr((coords-512)*0.30/512,'code_length')

# bottom octant
bottom_octant=emissivity[:513,:513,:513] 
coords=np.array(np.unravel_index(bottom_octant.argmax(),bottom_octant.shape))
maxloc=ds.arr((coords-512)*0.30/512,'code_length') 

print('Maxloc for primary hotspot is',maxloc)

# or for top octant
#top_octant=emissivity[512:,512:,512:] 
#coords=np.array(np.unravel_index(top_octant.argmax(),top_octant.shape))
#maxloc=ds.arr(coords*0.30/512,'code_length') 

# now try to find the next brightest one
# first blank the area around the hotspot

pvalues=np.linspace(0,1024,1025)

#xv,yv,zv=np.meshgrid(pvalues,pvalues,pvalues)
yv,xv,zv=np.meshgrid(pvalues,pvalues,pvalues,copy=True) #WTF!

masked_emissivity=copy.copy(emissivity)

r=(xv-coords[0])**2 + (yv-coords[1])**2 + (zv-coords[2])**2

masked_emissivity[r<400]=0 # very sensitive to this number (200-400 for doubles, or 100)

masked_bottom_octant=masked_emissivity[:513,:513,:513] 
new_coords=np.array(np.unravel_index(masked_bottom_octant.argmax(),masked_bottom_octant.shape))
masked_maxloc=ds.arr((new_coords-512)*0.30/512,'code_length') 

print('Maxloc for secondary hotspot is',masked_maxloc)

##s = yt.SlicePlot(ds, 'z', ['density','pressure','emissivity'], center=[0.22,0.07,-0.01], width=(60, 'kpc'))
#s = yt.SlicePlot(ds, 'z', ['density','pressure','emissivity'], center=maxloc, w#idth=(30, 'kpc'))
#s.annotate_velocity(factor=16) 
#s.save(name='timestep%04i' % timestep) 

s=yt.OffAxisSlicePlot(ds, np.cross(maxloc,masked_maxloc), ["density","pressure","emissivity","divergence"], center=(maxloc+masked_maxloc)/2.0,width=(50,'kpc'),north_vector=maxloc)
s.annotate_cquiver('cutting_plane_velocity_x', 'cutting_plane_velocity_y',factor=16)
s.save(name='offaxis_timestep%04i' % timestep)
