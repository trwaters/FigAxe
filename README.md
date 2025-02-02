# FigAxe
*FigAxe* has allowed me to overcome a few hurdles that tended to make plotting feel like a chore, even as an experienced user of [*Matplotlib*](https://matplotlib.org/):
- Habitually having to copy the same code to "finalize" figures (e.g., hiding tick labels, tweaking subplots_adjust etc.)
- The struggle of finding a good placement of colorbars in a new subplot layout 
- Forgetting how *GridSpec* works when I need a custom subplot layout

*FigAxe* takes a somewhat brute-force approach by providing functionality to make fine-adjustments and decide on colorbar placement up front, resulting in a collection of pre-defined figure *layouts*.  A simple hack to *GridSpec* makes it very easy to add new layouts to suit the specific needs of a given project.

Designed to provide automatated figure generation for [club4am](https://github.com/trwaters/club4am), an analysis and visualization package being developed for the MHD code [Athena++](https://github.com/PrincetonUniversity/athena-public-version), I have begun using *FigAxe* as a productivity aid in all of my projects.  I'm sharing in hopes that it will be useful to others.

## Requirements ##
`Python` version 3.7 or later since *FigAxe* makes use of the `dataclasses` module that was introduced in `Python 3.7`.  I recommend using an [anaconda distribution](https://www.anaconda.com/), which will automatically install *ipython* and the dependencies, which are *Matplotlib*, *numpy*, and *pylab*.

## Quick start ##
No installation required --- this is just a module.  Simply clone the repo and then in an ipython window, enter

```
from pylab import *
import figaxe
fig,axs = figaxe.use_layout()
x = np.linspace(0,1,100)
axs['1'].plot(x)
axs['1'].plot(x**2)
show()
```
You should see the following plot
![Figure_1](https://user-images.githubusercontent.com/3180046/83253255-edb63200-a169-11ea-8ce5-4b03c4d643cc.png)

## Basic Usage ##
The following screenshot summarizes what FigAxe is all about: a collection of pre-defined layouts (the names 'cb1h', 'cb1v' etc.) that correspond to the figures given by the ascii-art.  To see a list of all layouts, use `figaxe.help()`.

![ipython_screen](https://user-images.githubusercontent.com/3180046/83346795-d21f6880-a2dc-11ea-8fd5-7ed105d5732b.png)

Colorbar placement is indicated by the position of the `c` in the ascii-art representations when issuing `figaxe.help()`.

### Previewing layouts ###
The helper function `figaxe.plot_layout()` is provided to show the skeleton figure corresponding to each layout name.  Try for example,

    figaxe.plot_layout('h3')
 
### Using *FigAxe* in place of *GridSpec* or *subplots* ###
Just like these modules, *FigAxe* is used to return figure and axes handles:

    fig,axs =  figaxe.use_layout('h2')
To allow for colorbar functionality, `axs` is a dictionary, not a list.  For the layout 'h2', we have 

```
In [30]: figaxe.use_layout('h2')                                                                  

          c   c 
        +---+---+
        | 1 | 2 |
        +---+---+
        
Out[30]: 
(<Figure size 1275x765 with 4 Axes>,
 {'1': <matplotlib.axes._subplots.AxesSubplot at 0x7f3479443dd0>,
  '2': <matplotlib.axes._subplots.AxesSubplot at 0x7f3479494990>,
  'cax1': <matplotlib.axes._axes.Axes at 0x7f349ea50610>,
  'hcb1': <matplotlib.colorbar.Colorbar at 0x7f34c2143810>,
  'cax2': <matplotlib.axes._axes.Axes at 0x7f3479313910>,
  'hcb2': <matplotlib.colorbar.Colorbar at 0x7f3479408f10>}
```
In addition to the two axes handles `axs['1']` and `axs['2']`, there are the two colorbar axes handles, `axs['cax1']` and `axs['cax2']`, and the two colorbars themselves, `axs['hcb1']` and `axs['hcb2']`.  The 'h' means these colorbars have a horizontal orientation.  That is, this custom layout was pre-designed to have handles and room for two horizontal colorbars.  By contrast, the layout 'h2cb1' has instead a single vertical colorbar, but it still has two colorbar axes handles:

```
In [31]: figaxe.use_layout('h2cb1')                                                               

        +---+---+ 
        | 1 | 2 |c
        +---+---+
        
Out[31]: 
(<Figure size 800x500 with 3 Axes>,
 {'1': <matplotlib.axes._subplots.AxesSubplot at 0x7f7aad2047d0>,
  '2': <matplotlib.axes._subplots.AxesSubplot at 0x7f7a950c3f50>,
  'cax1': None,
  'vcb1': None,
  'cax2': <matplotlib.axes._axes.Axes at 0x7f7a95c70710>,
  'vcb2': <matplotlib.colorbar.Colorbar at 0x7f7a95c24dd0>})
```
This was necessary so that adjacent panels have the same size upon using `mpl_toolkits.axes_grid1.axes_divider.make_axes_locatable` to add colorbars.  The example scripts `demo_cbars_h3.py` `demo_cbars_h3cb1.py` show how this functionality makes it easy to generate colormap plots. 

*FigAxe* supports both vertical and horizontal colorbar placement.  The choice can be specified for each layout defined in `gridspec_helper.custom_layouts()`, with the default being to place horizontal colorbars on *single row layouts* (layout names beginning with *h* in the list given by `figaxe.help()`) and vertical colorbars on *single column layouts* (layout names beginning with *v*) **unless** the layout name ends with `cb1`.    

### Examples ###
In the `demos` folder, a few examples of using *FigAxe* to make both line plots and colormap plots are provided.
The output of `demo_cbars_h3.py` adds colorbars to an example from [matplotlib's gallery](https://matplotlib.org/3.1.0/gallery/images_contours_and_fields/image_demo.html).

![figaxe_demo](https://user-images.githubusercontent.com/3180046/83251695-36b8b700-a167-11ea-809c-4537aaad21d7.png)


## Adding new layouts ##
The module `figaxe.py` contains the methods for making the actual *fig,axes* handles given a layout defined in `gridspec_helper.py`.  Normal usage of *FigAxe* should only require editing `gridspec_helper.py` in order to add new instances of the classes `FigAxe` and `LiteFigAxe`.  Both of these dataclasses utilize *GridSpec* to generate axes handles, but `LiteFigAxe` is designed for quickly adding a new layout, as it uses `tight_layout` instead of `subplots_adjust` for panel placement (see `make_lite_figure()` in `figaxe.py`).   

If you forget how *FigAxe*'s *Gridspec*-hack for defining new layouts works, `figaxe.help` shows the following instructions for defining a new layout:

![layout_help](https://user-images.githubusercontent.com/3180046/83347917-b10f4580-a2e5-11ea-9843-b4b63d174182.png)

This layout is actually the one used as [a demonstration](https://matplotlib.org/3.2.1/gallery/subplots_axes_and_figures/gridspec_multicolumn.html#sphx-glr-gallery-subplots-axes-and-figures-gridspec-multicolumn-py) for *GridSpec* and corresponds to the following less intuitve statements

````
gs = GridSpec(3, 3, figure=fig)
ax1 = fig.add_subplot(gs[0, :])
ax2 = fig.add_subplot(gs[1, :-1])
ax3 = fig.add_subplot(gs[1:, -1])
ax4 = fig.add_subplot(gs[-1, 0])
ax5 = fig.add_subplot(gs[-1, -2])
````
