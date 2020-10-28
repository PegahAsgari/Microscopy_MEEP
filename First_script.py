# first I want to make the geometry

import meep as mp
import math
import matplotlib
#matplotlib.use('agg')
import numpy as np
import matplotlib.pyplot as plt
from meep.materials import BK7

wvl_min = 0.760  # min wavelength
wvl_max = 0.940  # max wavelength
fmin = 1 / wvl_max  # min frequency
fmax = 1 / wvl_min  # max frequency
fcen = 0.5 * (fmin + fmax)  # center frequency
df = fmax - fmin  # frequency width
nfreq = 200  # number of frequency bins

s = 20
resolution = 50
dpml = 2

cell_size = mp.Vector3(s,s,0)

boundary_layers = [mp.PML(thickness=dpml)]

beam_x0 = mp.Vector3(0,4.0)    # beam focus (relative to source center)
rot_angle = 0  # CCW rotation angle about z axis (0: +y axis)
beam_kdir = mp.Vector3(0,1,0).rotate(mp.Vector3(0,0,1),math.radians(rot_angle))  # beam propagation direction
beam_w0 = 0.3  # beam waist radius
beam_E0 = mp.Vector3(0,0,1)

sources = [mp.GaussianBeamSource(src=mp.ContinuousSource(fcen,fwidth=df),
                                 center=mp.Vector3(0,-0.5*s+dpml+1.0),
                                 size=mp.Vector3(s),
                                 beam_x0=beam_x0,
                                 beam_kdir=beam_kdir,
                                 beam_w0=beam_w0,
                                 beam_E0=beam_E0)]


# cover slip
geometry = [mp.Block(mp.Vector3(mp.inf,40,mp.inf),
                     center=mp.Vector3(0,-20,0),
                     material=BK7),
            mp.Cylinder(radius=3,center=mp.Vector3(0,2.8,0),
                        axis=mp.Vector3(0,0,1),
                        material=BK7,
                        height=4),
            ]

sim = mp.Simulation(cell_size=cell_size,
                    boundary_layers=boundary_layers,
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution)


sim.run(until=20)

sim.plot2D(fields=mp.Ez,
           output_plane=mp.Volume(center=mp.Vector3(),
                                  size=mp.Vector3(s,s)))

plt.savefig('Ez_angle{}.png'.format(rot_angle),bbox_inches='tight',pad_inches=0)



eps_data = sim.get_array(center=mp.Vector3(), size=cell_size, component=mp.Dielectric)
ez_data = sim.get_array(center=mp.Vector3(), size=cell_size, component=mp.Ez)
plt.figure()
plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
plt.imshow(ez_data.transpose(), interpolation='spline36', cmap='RdBu', alpha=0.9)
plt.axis('off')
plt.show()
