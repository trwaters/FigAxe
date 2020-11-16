import sys
import numpy as np
import pylab as plt
from importlib import reload

# make figaxe module visible in path
sys.path.insert(0,'..')
import figaxe; reload(figaxe)

# import style file
plt.style.use(r"../figaxe.mplstyle")



"""
Here we consider a matplotlib example from 
https://matplotlib.org/3.1.0/gallery/images_contours_and_fields/image_demo.html
which makes subplots using
fig, axs = plt.subplots(1, 3, figsize=(10, 3)) 

Using the gridspec_helper module of FigAxe instead, fine adjustments to the 
layout are made in gridspec_helper.py, resulting in a publication quality plot.

In this example, we use the 'h3cb1' layout, which has just a single
colorbar, accomplished by adding 3 colorbars then deleting 2.  
"""

A = np.random.rand(5, 5)

layout = 'h3'

fig,axs =  figaxe.use_layout(layout)

# axs is a dictionary containing specificiation for colorbars;
# here's how to extract the colorbar handles
cbs = {k:v for (k,v) in axs.items() if 'cb' in k}
caxs = {k:v for (k,v) in axs.items() if 'cax' in k}

for ax_k,cax_k,cb_k,interp in zip(axs.keys(), caxs.keys(), cbs.keys(), ['nearest', 'bilinear', 'bicubic']):
    ax = axs[ax_k]
    cax = caxs[cax_k]
    cb = cbs[cb_k]

    pim = ax.imshow(A, interpolation=interp)
    # ax.set_title(interp.capitalize())
    ax.grid(True)

    # add colorbars according to layout
    if cb is not None:
        print('a2:cb = {}'.format(cbs[cb_k]))
        cbs[cb_k].update_normal(pim) 
        cax.xaxis.set_ticks_position("top")
        cax.set_title(interp.capitalize())


    ax.set_xlabel(r'$x$')

axs['1'].set_ylabel(r'$y$')

plt.savefig('figaxe_demo.png', dpi=160)
plt.show()

