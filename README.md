# FigAxe
*FigAxe* solves a few problems likely common to many computational scientists who use *Matplotlib*:
1. Habitually having to copy the same code to "finalize" figures (e.g., hiding tick labels, tweaking subplots_adjust etc.)
2. Repeatedly struggling to place colorbars in colormap plots correctly
3. Remembering how *GridSpec* works to make a custom subplot layout

*FigAxe* takes a somewhat brute-force approach by providing functionality to make fine-adjustments and decide on colorbar placement up front, resulting in a collection of pre-defined figure *layouts*.  A simple hack to *GridSpec* makes it very easy to add new layouts to suit the specific needs of your project.

Designed to provide automatated figure generation for [club4am](https://github.com/trwaters/club4am), an analysis and visualization package for the MHD code [Athena++](https://github.com/PrincetonUniversity/athena-public-version), I have begun using *FigAxe* as a productivity aid in all of my projects.  I'd be thrilled if you put it to use as well!

## Getting Started ##
No installation required-- this is just a module.  Simply clone or download a zip of the repo, open an ipython window, type `import figaxe` followed by `figaxe.show_layouts()`, and you should see the following:

![FigAxe_screenshot2](https://user-images.githubusercontent.com/3180046/82995206-8c069400-9fc0-11ea-9e3e-b979309fb848.png)

### Previewing layouts ###
The helper function `figaxe.plot_layout()` is provided to show the skeleton figure corresponding to each layout name.  Try for example,

    figaxe.plot_layout('h3')
    
## Adding new layouts ##
The module `figaxe.py` contains the methods for making the actual *fig,axes* handles given a layout defined in `gridspec_helper.py`.  Normal usage of *FigAxe* should only require editing `gridspec_helper.py` in order to add new instances of the classes `FigAxe` and `LiteFigAxe` to the functions `custom_layouts()` and `lite_layouts()`, respectively.  Both methods utilize *GridSpec* to generate axes handles, but the *lite*-variety are designed for quickly adding a new custom layout.  Specifically, the instances of `LiteFigAxe` in `lite_layouts()` ultimately use `tight_layout` (see `make_lite_figure()` in `figaxe.py`), while the more flexible `FigAxe` class uses `subplots_adjust`.  
