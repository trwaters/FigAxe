
import numpy as np
import pylab as plt
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
from importlib import reload
import figaxe; reload(figaxe)

"""
Here we consider a matplotlib example from 
https://matplotlib.org/3.1.0/gallery/images_contours_and_fields/image_demo.html
which makes subplots using
fig, axs = plt.subplots(1, 3, figsize=(10, 3)) 

Using the gridspec_helper module of FigAxe instead, fine adjustments to the 
layout are made in layouts.py, resulting in a publication quality plot.

In this example, we use the 'h3cb1' layout, which has just a single
colorbar, accomplished by adding 3 colorbars then deleting 2.  
"""

A = np.random.rand(5, 5)

layout = 'h3cb1'

fig,axs =  figaxe.custom_layout(layout)

# axs is a dictionary containing specificiation for colorbars;
# here's how to extract the colorbar handles
cbs = {k:v for (k,v) in axs.items() if 'cb' in k}


for ax_k,cb_k,interp in zip(axs.keys(), cbs.keys(), ['nearest', 'bilinear', 'bicubic']):
    ax = axs[ax_k]
    cb = cbs[cb_k]

    pim = ax.imshow(A, interpolation=interp)
    ax.set_title(interp.capitalize())
    ax.grid(True)

    # add colorbars according to layout
    if cb is not None:
        print('a2:cb = {}'.format(cbs[cb_k]))
        cbs[cb_k].update_normal(pim) 


    ax.set_xlabel(r'$x$')

axs['1'].set_ylabel(r'$y$')
cb.set_label('magnitude')

plt.show()

