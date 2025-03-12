import yt
import numpy as np
import os
import copy


timesteps = np.arange(43,65)

for timestep in timesteps:

    os.chdir('/beegfs/car/mayaahorton/PLUTO/problems/precessing/visuals/VHR/45_100_1_VHR')

    print('Reading the data')
    emissivity=np.load('emissivity_%04i.npy' % timestep)
    tracer=np.load('tracer_%04i.npy' % timestep)
#    density=np.load('density_%04i.npy' % timestep)
    vx=np.load('vx_%04i.npy' % timestep)
    vy=np.load('vy_%04i.npy' % timestep)
    vz=np.load('vz_%04i.npy' % timestep)
#    ts = np.load('total_speed_%04i.npy' % timestep)
#    lss = np.load('local_sound_speed_%04i.npy' % timestep)
#    lmn = np.load('local_mach_number_%04i.npy' % timestep)

    print('Making the YT structure')
    bbox = np.array([[-0.3, 0.3], [-0.3, 0.3], [-0.3, 0.3]])
    ds = yt.load_uniform_grid({'tracer':tracer,'velocity_x':vx,'velocity_y':vy,'velocity_z':vz,'emissivity':emissivity}, vx.shape, 3.08e24, bbox=bbox, nprocs=64)

    os.chdir('/beegfs/car/mayaahorton/PLUTO/problems/precessing/visuals/VHR/45_100_1_VHR') # change me
    print('Now making plots, hurrah!')

    # bottom octant
    bottom_octant=emissivity[:513,:513,:513] 
    coords=np.array(np.unravel_index(bottom_octant.argmax(),bottom_octant.shape))
    maxloc=ds.arr((coords-512)*0.30/512,'code_length') 

    print('Maxloc for primary hotspot is',maxloc)

    pvalues=np.linspace(0,1024,1025)

    yv,xv,zv=np.meshgrid(pvalues,pvalues,pvalues,copy=True) #WTF!

    masked_emissivity=copy.copy(emissivity)

    r=(xv-coords[0])**2 + (yv-coords[1])**2 + (zv-coords[2])**2

    masked_emissivity[r<400]=0 # very sensitive to this number (200-400 for doubles, or 100)

    masked_bottom_octant=masked_emissivity[:513,:513,:513] 
    new_coords=np.array(np.unravel_index(masked_bottom_octant.argmax(),masked_bottom_octant.shape))
    masked_maxloc=ds.arr((new_coords-512)*0.30/512,'code_length') 

    print('Maxloc for secondary hotspot is',masked_maxloc)

    s=yt.OffAxisSlicePlot(ds, np.cross(maxloc,masked_maxloc), ["tracer"], center=(maxloc+masked_maxloc)/2.0,width=(50,'kpc'),north_vector=maxloc)
    #s.set_zlim('local_sound_speed', 1, 100)
    #s.set_zlim('total_speed', 1, 100)
    #s.set_zlim('local_mach_number',0.1,10)
    s.set_zlim('tracer', 10e-6, 1)
    s.annotate_cquiver('cutting_plane_velocity_x', 'cutting_plane_velocity_y',factor=16) #put me back for vectors
    s.save(name='tracer_2scale_vec_timestep%04i' % timestep)
