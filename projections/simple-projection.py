import yt
from yt.units import kpc
import numpy as np

# Simplest example of creating a projection plot in yt
# This code creates a projection plot of a single data cube in the y direction. It only requires one emissivity data cube to have been made; output is saved as a .png file in the same directory as the data cube.

bbox = np.array([[-0.3,0.3], [-0.3,0.3], [-0.3,0.3]])
data = np.load('/beegfs/car/mayaahorton/PLUTO/problems/precessing/visuals/VHR/45_100_1_VHR/emissivity_0285.npy')
ds = yt.load_uniform_grid({'emissivity':data}, data.shape, 3.08e24, bbox = bbox, nprocs = 32)

pr = yt.ProjectionPlot(ds, "y", "emissivity")
pr.set_background_color("emissivity",color="black")
pr.set_cmap(field = "emissivity", cmap = "dusk")
pr.set_zlim("emissivity", 1e26, 1e24)
pr.save("y_cmap.png")