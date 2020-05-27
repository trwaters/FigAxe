# FigAxe
*FigAxe* has allowed me to overcome a few hurdles that tended to make plotting feel like a chore, even as a rather experienced user of *Matplotlib*:
1. Habitually having to copy the same code to "finalize" figures (e.g., hiding tick labels, tweaking subplots_adjust etc.)
2. Repeatedly struggling to place colorbars in colormap plots correctly
3. Remembering how *GridSpec* works to make a custom subplot layout

*FigAxe* takes a somewhat brute-force approach by providing functionality to make fine-adjustments and decide on colorbar placement up front, resulting in a collection of pre-defined figure *layouts*.  A simple hack to *GridSpec* makes it very easy to add new layouts to suit the specific needs of a given project.

Designed to provide automatated figure generation for [club4am](https://github.com/trwaters/club4am), an analysis and visualization package for the MHD code [Athena++](https://github.com/PrincetonUniversity/athena-public-version), I have begun using *FigAxe* as a productivity aid in all of my projects.  I'd be thrilled if it became useful to others too!

## Getting Started ##
No installation required-- this is just a module.  Simply clone or download a zip of the repo, open an ipython window, type `import figaxe` followed by `figaxe.show_layouts()`, and you should see the following:

![FigAxe_screenshot2](https://user-images.githubusercontent.com/3180046/82995206-8c069400-9fc0-11ea-9e3e-b979309fb848.png)

### Previewing layouts ###
The helper function `figaxe.plot_layout()` is provided to show the skeleton figure corresponding to each layout name.  Try for example,

    figaxe.plot_layout('h3')
 
### Using *FigAxe* in place of *GridSpec* or *subplots* ###
Just like these modules, *FigAxe* is used to return figure and axes handles:

    fig,axs =  figaxe.custom_layout('h2')
In this example, `axs` is the following dictionary

```
In [4]: axs                                                                                          
Out[4]: 
{'1': <matplotlib.axes._subplots.AxesSubplot at 0x7f1a15db4050>,
 '2': <matplotlib.axes._subplots.AxesSubplot at 0x7f1a15de8490>,
 '1cb': 1,
 '2cb': 1}
```
In addition to the two axes handles `axs['1']` and `axs['2']`, there are the two colorbar handles `axs['1b']` and `axs['2b']`.  That is, this custom layout was pre-designed to have handles and room for two horizontal colorbars.  By contrast,

    fig,axs =  figaxe.custom_layout('h2cb1')
has instead a single vertical colorbar and thus only one colorbar handle:

```
In [4]: axs                                                                                          
Out[4]: 
{'1': <matplotlib.axes._subplots.AxesSubplot at 0x7f1a187903d0>,
 '2': <matplotlib.axes._subplots.AxesSubplot at 0x7f1a1876f910>,
 '2cb': 1}

```
*FigAxe* supports both vertical and horizontal colorbar placement.  The choice can be specified for each layout defined in `gridspec_helper.custom_layouts()`, with the default being to place horizontal colorbars on *single row layouts* (layout names beginning with *h* in the screenshot above) and vertical colorbars on *single column layouts* (layout names beginning with *v*) **unless** the layout name ends with `cb1`.  Colorbar placement is indicated by the position of the `c` in the ascii-art representations when issuing `figaxe.show_layouts()`.  

## Adding new layouts ##
The module `figaxe.py` contains the methods for making the actual *fig,axes* handles given a layout defined in `gridspec_helper.py`.  Normal usage of *FigAxe* should only require editing `gridspec_helper.py` in order to add new instances of the classes `FigAxe` and `LiteFigAxe` to the functions `custom_layouts()` and `lite_layouts()`, respectively.  Both methods utilize *GridSpec* to generate axes handles, but the *lite*-variety are designed for quickly adding a new custom layout.  Specifically, the instances of `LiteFigAxe` in `lite_layouts()` ultimately use `tight_layout` (see `make_lite_figure()` in `figaxe.py`), while the more flexible `FigAxe` class uses `subplots_adjust`.  

If you forget how *FigAxe*'s *Gridspec*-hack for defining new layouts, simply type

    figaxe.lite_layout()
which will issue an error since no `layout name` was passed.  This error shows the following instructions for defining a new layout:

![lite_layout](https://user-images.githubusercontent.com/3180046/83005637-4781f500-9fce-11ea-9885-9d8af07eec4d.png)

This layout is actually the one used as [a demonstration](https://matplotlib.org/3.2.1/gallery/subplots_axes_and_figures/gridspec_multicolumn.html#sphx-glr-gallery-subplots-axes-and-figures-gridspec-multicolumn-py) for *GridSpec* and corresponds to the following less intuitve statements

````
gs = GridSpec(3, 3, figure=fig)
ax1 = fig.add_subplot(gs[0, :])
ax2 = fig.add_subplot(gs[1, :-1])
ax3 = fig.add_subplot(gs[1:, -1])
ax4 = fig.add_subplot(gs[-1, 0])
ax5 = fig.add_subplot(gs[-1, -2])
````
