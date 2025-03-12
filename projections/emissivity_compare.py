import yt
import numpy as np
import os
import copy

# Change timestep range to outputs of interest or run over a full simulation (computationally expensive)
timesteps = np.arange(118,181)

for timestep in timesteps:

    os.chdir('/beegfs/car/mayaahorton/PLUTO/problems/precessing/visuals/VHR/45_100_1_VHR')

    print('Reading the data')
    emissivity=np.load('emissivity_%04i.npy' % timestep)
    new_emissivity=np.load('emissivity_new2_%04i.npy' % timestep)
    tracer=np.load('tracer_%04i.npy' % timestep)
    vx=np.load('vx_%04i.npy' % timestep)
    vy=np.load('vy_%04i.npy' % timestep)
    vz=np.load('vz_%04i.npy' % timestep)

    print('Making the YT structure')
    bbox = np.array([[-0.3, 0.3], [-0.3, 0.3], [-0.3, 0.3]])
    ds = yt.load_uniform_grid({'old_emissivity':emissivity,'new_emissivity':new_emissivity,'velocity_x':vx,'velocity_y':vy,'velocity_z':vz,'tracer':tracer}, vx.shape, 3.08e24, bbox=bbox, nprocs=64)

    os.chdir('/beegfs/car/mayaahorton/PLUTO/problems/precessing/visuals/VHR/45_100_1_VHR') # change me
    print('Now making plots, hurrah!')

    # OLD EMISSIVITY
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
    old_new_coords=np.array(np.unravel_index(masked_bottom_octant.argmax(),masked_bottom_octant.shape))
    masked_maxloc=ds.arr((old_new_coords-512)*0.30/512,'code_length') 

    # NEW EMISSIVITY
    new_bottom_octant=new_emissivity[:513,:513,:513]
    new_coords=np.array(np.unravel_index(new_bottom_octant.argmax(),new_bottom_octant.shape))
    new_maxloc=ds.arr((new_coords-512)*0.30/512,'code_length')

    #pvalues=np.linspace(0,1024,1025)
    #yv,xv,zv=np.meshgrid(pvalues,pvalues,pvalues,copy=True) #WTF!
    new_masked_emissivity=copy.copy(new_emissivity)

    r2=(xv-new_coords[0])**2 + (yv-new_coords[1])**2 + (zv-new_coords[2])**2
    new_masked_emissivity[r2<400]=0 # very sensitive to this number (200-400 for doubles, or 100)

    new_masked_bottom_octant=new_masked_emissivity[:513,:513,:513]
    new_new_coords=np.array(np.unravel_index(new_masked_bottom_octant.argmax(),new_masked_bottom_octant.shape))
    new_masked_maxloc=ds.arr((new_new_coords-512)*0.30/512,'code_length')

    # BOTH PLOTS
    #fig, axes, colorbars = get_multi_plot(2,1, colorbar=orient, bw = 4) 

    #grid_axes = [axes[0], axes[1]]
    #grid_axes.yaxis.set_visible(False)

    #s=yt.OffAxisSlicePlot(ds, np.cross(maxloc,masked_maxloc), ["old_emissivity","tracer"], center=(maxloc+masked_maxloc)/2.0,width=(50,'kpc'),north_vector=maxloc)
    #s.annotate_cquiver('cutting_plane_velocity_x', 'cutting_plane_velocity_y',factor=16) #put me back for vectors
    #s.set_zlim('tracer',1e-12,1)
    #s.save(name='newtracer12_%04i' % timestep)
   
    s2=yt.OffAxisSlicePlot(ds, np.cross(new_maxloc,new_masked_maxloc), ["new_emissivity"], center=(new_maxloc+new_masked_maxloc)/2.0,width=(50,'kpc'),north_vector=new_maxloc)
    #s.annotate_cquiver('cutting_plane_velocity_x', 'cutting_plane_velocity_y',factor=16) #put me back for vectors
    s2.save(name='newtracer_2_%04i' % timestep)
