import yt
import numpy as np
from yt.visualization.volume_rendering.api import VolumeSource
import sys

bbox = np.array([[-0.3, 0.3], [-0.3, 0.3], [-0.3, 0.3]])

timestep=int(sys.argv[1])

# Adjust inputs as needed; use .npy cubes created previously

data=np.load('emissivity_%04i.npy' % timestep)
mach=np.load('mach_%04i.npy' % timestep)
ds = yt.load_uniform_grid({'emissivity':data,'radial_mach_number':mach}, data.shape, 3.08e24, bbox=bbox, nprocs=32)
sc = yt.create_scene(ds, lens_type='perspective', field='emissivity') 
sc.camera.resolution = (1024, 1024)
source = sc[0]
source.tfh.grey_opacity = False
source.tfh.set_log(True)
source.tfh.set_bounds((0.1,5e3))
#source.tfh.plot('transfer_function.png', profile_field='emissivity')

ms=VolumeSource(ds, field='radial_mach_number')
ms.tfh.set_log(False)
sc.add_source(ms)
sc[1].transfer_function.map_to_colormap(1,120, scale=3.0, colormap='Purples')

# now pick a camera position

#position=np.array([0,-0.3,-0.5]) # in Mpc
position=np.array([0,0.9,0]) #experimenting 

sc.camera.position = ds.arr(position, 'code_length')

normal_vector=-position # look back towards the centre
north_vector = [0., 0., 1.] # z axis is upwards
sc.camera.switch_orientation(normal_vector=normal_vector,
                             north_vector=north_vector)

sc.save('zoom_test%04i.png' % timestep, sigma_clip=3)
