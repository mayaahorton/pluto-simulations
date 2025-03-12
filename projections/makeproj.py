import yt
import numpy as np

bbox = np.array([[-0.3, 0.3], [-0.3, 0.3], [-0.3, 0.3]])
data=np.load('/beegfs/car/mjh/PLUTO/cube/emissivity_0200.npy')
ds = yt.load_uniform_grid({'emissivity':data}, data.shape, 3.08e24, bbox=bbox, nprocs=32)
vector=[0.1,0,1]
prj=yt.off_axis_projection(ds,[0,0,0],vector,0.5,512,'emissivity',north_vector=[0,1,0])
#prj.save('projection.png')
print('max is',np.max(np.log10(prj)))
minv=22.5
maxv=26.5
yt.write_image(np.log10(prj), cmap_name='Blues',color_bounds=(minv,maxv),filename="offaxis_projection.png",func=lambda n:np.where(n>maxv,maxv,n))
