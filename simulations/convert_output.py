import numpy as np
import re
import os

# Takes output from PLUTO and plots a data slice. This example reprojects spherical polar data onto a Cartesian grid. The Pluto_Output class is used to reads grid.out and .dbl files.

# This stage is required for all further visualisations and projections. 

class Pluto_Output:
    def __init__(self,wd):
        os.chdir(wd)
        self.dims=[]
        self.spacing=[]
        self.bounds={}
        print "Reading grid.out"
        with open('grid.out') as f:
            gridout = f.readlines()
            for line in gridout:
                m=re.search('^# DIMENSIONS: (\d+)',line)
                if m:
                    self.dimensions=int(m.group(1))
                    print 'Found dimensions:',self.dimensions
                if line[0:3]=='# X':
                    print 'Found bounds line',line
                    bits=line.split()
                    print bits[3],bits[4]
                    lower=float(bits[3].replace(',',''))
                    upper=float(bits[4].replace(']','').replace(',',''))
                    dim=int(bits[1][1])
                    print dim,lower,upper
                    self.bounds[dim]=(lower,upper)
                if re.search('^(\d+)\s+$',line):
                    self.dims.append(int(line))
                m=re.search('^ 1\s+(\S+)\s+(\S+)',line)
                if m:
                    self.spacing.append(float(m.group(2))-float(m.group(1)))

        print self.dims, self.spacing

    def map_dbl(self,num,value):
        filename='data.%04i.dbl' % num
        fpr = np.memmap(filename, dtype='float64', mode='r', shape=tuple(reversed(self.dims)),offset=value*8*self.dims[0]*self.dims[1]*self.dims[2])
        return fpr
        
    def read_slice(self,num,value,sl=-1):
        if sl<0:
            sl=self.dims[2]/2
        return self.map_dbl(num,value)[sl,:,:]

    def plot_slice(self,grid,slice,dolog=False,cbar=False,cmap='Blues',crange=None,cax=None,pscale=1.0,xlabel=None,ylabel=None,cblabel=None,polar=False,outer=-1,slice2=None):
        import matplotlib.pyplot as plt
        spacing=self.spacing
        dims=self.dims
        doslice2=(slice2 is not None)
        (ydim,xdim)=slice.shape
        if polar:
            # slice is in r, phi
            # we need to regrid onto a Cartesian grid

            if outer<0:
                outer=xdim
            else:
                outer=int(outer)
            rbound_l,rbound_h=self.bounds[1]
            if doslice2:
                cgrid=np.ones((2*outer,2*outer),dtype=np.float32)
                xzero=-outer
                xoffset=outer
            else:
                cgrid=np.ones((2*outer,outer),dtype=np.float32)
                xzero=xoffset=0
            for y in range(-outer,outer):
                for x in range(xzero,outer):
                    xd=(x+0.5)*spacing[0]
                    yd=(y+0.5)*spacing[0]
                    r=np.sqrt(xd**2.0+yd**2.0)
                    theta=np.arctan2(xd,yd)
                    ri=int(0.5+(r-rbound_l)/spacing[0])
                    ti=int(0.5+theta/spacing[1])
                    if ti<0:
                        ti=ydim+ti
                    if ti>=ydim:
                        continue
                    if ri<0 or ri>=outer:
                        continue
                    else:
                        if x<0:
                            index=ydim-ti
                            if index>=ydim:
                                continue
                            cgrid[outer+y,xoffset+x]=slice2[index,ri]
                        else:
                            cgrid[outer+y,xoffset+x]=slice[ti,ri]
            domain=cgrid
        else:
            domain=slice        
        

        min=np.min(domain)
        max=np.max(domain)
        if (min<0):
            cmap='RdBu'
            vmax=np.max([abs(min),abs(max)])
            vmin=-vmax
        else:                  
            if dolog:
                nonzero=domain>0
                domain=np.log10(domain)
                vmin=np.min(domain[nonzero])
                vmax=np.max(domain)
            else:
                vmin=min
                vmax=max

        if crange!=None:
            (vmin,vmax)=crange


        if not(polar):
        
            im=grid.imshow(domain,origin='lower',extent=(self.bounds[1][0],self.bounds[1][1],self.bounds[2][0],self.bounds[2][1]),cmap=cmap,vmin=vmin,vmax=vmax)
        else:
                
            im=grid.imshow(domain,origin='lower',cmap=cmap,vmin=vmin,vmax=vmax,extent=(xzero*spacing[0],outer*spacing[0],-outer*spacing[0],outer*spacing[0])) 
        if cbar:
            cbaro=cax.colorbar(im)
            if cblabel:
                print 'setting label to',cblabel
                cbaro.ax.set_xlabel(cblabel)
        if xlabel:
            grid.set_xlabel(xlabel)
        if ylabel:
            grid.set_ylabel(ylabel)

