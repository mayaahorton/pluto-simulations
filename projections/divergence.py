def divergence(f): 
    """ 
    Computes the divergence of the vector field f, corresponding to dFx/dx + dFy/dy + ... 
    :param f: List of ndarrays, where every item of the list is one dimension of the vector field 
    :return: Single ndarray of the same shape as each of the items in f, which corresponds to a scalar field 
     """ 

    num_dims = len(f) 
    return np.ufunc.reduce(np.add, [np.gradient(f[i], axis=i) for i in range(num_dims)])

# compute

divergence=divergence([vx,vy,vz])

then do e.g.

ds = yt.load_uniform_grid({'pressure':prs,'velocity_x':vx,'velocity_y':vy,'velocity_z':vz,'density':density,'emissivity':emissivity,'divergence':divergence}, vx.shape, 3.08e24, bbox=bbox, nprocs=64) 
