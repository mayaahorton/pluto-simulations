import yt
from yt.units import kpc
import numpy as np

bbox = np.array([[-0.3,0.3], [-0.3,0.3], [-0.3,0.3]])
data = np.load('/beegfs/car/mayaahorton/PLUTO/problems/precessing/visuals/VHR/45_100_1_VHR/emissivity_0045.npy')
ds = yt.load_uniform_grid({'emissivity':data}, data.shape, 3.08e24, bbox = bbox, nprocs = 32)
#slc = yt.SlicePlot(ds, 'z', 'emissivity',origin='native')
L = [1,1,0]
north_vector = [5,0,0]
cut = yt.SlicePlot(ds, L, 'emissivity', north_vector=north_vector)

cut.save('slice_test.png')

# Old versions are included below for future reference

#slc.set_width(10*kpc)
#slc.zoom(6)
#slc.save('slice_test.png')

#sc = yt.create_scene(ds, lens_type='perspective', field='emissivity')
#sc.camera.resolution = (1024, 1024)
#source = sc[0]
#source.tfh.grey_opacity = False
#source.tfh.set_log(True)
#source.tfh.plot('transfer_function.png', profile_field='emissivity')
#sc.save('em_test_0.png')
