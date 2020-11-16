import warnings
import numpy as np
import pylab as plt
from matplotlib.gridspec import GridSpec
from matplotlib.cbook import mplDeprecation
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable

# always reload gridspec_helper.py
from importlib import reload
import gridspec_helper; reload(gridspec_helper)



### fig generator method using LiteFigAxe class
### ==================================================

# called by lite_layout() 
def make_lite_figure(layout,name,fig_size=None):
    """
    input: an instance of LiteFigAxe 
    returns: fig,axes handles
    """

    if fig_size == None:
        fig_size = tuple(layout.size)

    fig = plt.figure(figsize=fig_size)
    gridspecs = gridspec_converter(layout.layout)
    ax1 = fig.add_subplot(gridspecs[0])

    axes_dic = {}
    # The axes are stored in gridspec in the order specified in the layout_array
    # so we just need to fill a dic with keys named '1','2','3',etc.
    # Here we do that while accounting for the shared axes specification
    for i,gridspec in enumerate(gridspecs):
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore',category=mplDeprecation)

            axes_dic[str(1+i)] = fig.add_subplot(gridspec)


    # add inward-pointing ticks on all 4 sides and set their visibility
    for idx,key in enumerate(axes_dic.keys()):
        ax = axes_dic[key]
        ax.minorticks_on()
        ax.xaxis.set_ticks_position('both')
        ax.yaxis.set_ticks_position('both')
        ax.tick_params(axis='both', direction='in',width=1.) 
        ax.tick_params(which='minor',axis='both',direction='in',width=1.) 

    # add any cbar axes
    if max(layout.cbars) > 0:
        Nax = len(gridspecs)
        for n in range(Nax):

            ax = axes_dic[str(1+n)]
            
            # first encode the vertical or horizontal orientation
            # into the colorbar key
            ori_tag = get_cax_orientation(name,layout.caxori[n])
            cax_key = 'cax' + str(n+1)  

            # now make the cbar axis
            cax_divider = make_axes_locatable(ax)
            location = get_cax_location(name,layout.caxloc[n])
            if location is not None:
                cax = cax_divider.append_axes(location, size="3%", pad="2%")
                axes_dic[cax_key] = cax 

            if ori_tag is not None: # add colorbar using dummy data
                cb_key = ori_tag + 'cb' + str(n+1)
                A = np.array([[1., 2.],[3., 4.]])
                pim = ax.imshow(A)
                if ori_tag=='v':
                    ori = "vertical"
                else:
                    ori = "horizontal"
                cb = fig.colorbar(pim, cax=cax, orientation=ori, extend='both')
                axes_dic[cb_key] = cb
                if ori_tag=='v':
                    ori = "vertical"
                else:
                    ori = "horizontal"
                    cax.xaxis.set_ticks_position("top")

            else:
                axes_dic[cax_key] = None


    plt.tight_layout()

    return fig,axes_dic




### fig generator method using FigAxe class
### ==================================================

# called by custom_layout()
def make_figure(layout,name,fig_size=None):
    """
    input: an instance of LiteFigAxe 
    returns: fig,axes handles
    """

    if fig_size == None:
        fig_size = tuple(layout.size)

    fig = plt.figure(figsize=fig_size)
    gridspecs = gridspec_converter(layout.layout)
    
    # head axis (panel 1 by default)
    hax = fig.add_subplot(gridspecs[layout.head-1])

    axes_dic = {}
    # The axes are stored in gridspec in the order specified in the layout_array
    # so we just need to fill a dic with keys named '1','2','3',etc.
    # Here we do that while accounting for the shared axes specification
    idx = 1
    for gridspec,share_x,share_y in zip(gridspecs,layout.share_x,layout.share_y):
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore',category=mplDeprecation)
            if gridspec != gridspecs[layout.head-1]:
                if share_x > 0 and share_y > 0:
                    axes_dic[str(idx)] = fig.add_subplot(gridspec,sharex=hax,sharey=hax)
                elif share_x > 0:
                    axes_dic[str(idx)] = fig.add_subplot(gridspec,sharex=hax)
                elif share_y > 0:
                    axes_dic[str(idx)] = fig.add_subplot(gridspec,sharey=hax)
                else:
                    axes_dic[str(idx)] = fig.add_subplot(gridspec)
            else:
                axes_dic[str(idx)] = fig.add_subplot(gridspec)
            idx += 1


    # add inward-pointing ticks on all 4 sides and set their visibility
    for idx,key in enumerate(axes_dic.keys()):
        ax = axes_dic[key]
        ax.minorticks_on()
        ax.xaxis.set_ticks_position('both')
        ax.yaxis.set_ticks_position('both')
        ax.tick_params(axis='both', direction='in',width=1.) 
        ax.tick_params(which='minor',axis='both',direction='in',width=1.) 

        # hide axis tick labels
        plt.setp(ax.get_xticklabels(), visible=not(layout.hide_x[idx]))
        plt.setp(ax.get_yticklabels(), visible=not(layout.hide_y[idx]))


    # add any cbar axes
    if max(layout.cbars) > 0:
        Nax = len(gridspecs)
        for n in range(Nax):
            ax = axes_dic[str(1+n)]
            
            # first encode the vertical or horizontal orientation
            # into the colorbar key
            ori_tag = get_cax_orientation(name,layout.caxori[n])
            cax_key = 'cax' + str(n+1)  

            # now make the cbar axis
            cax_divider = make_axes_locatable(ax)
            location = get_cax_location(name,layout.caxloc[n])
            if location is not None:
                cax = cax_divider.append_axes(location, size="3%", pad="2%")
                axes_dic[cax_key] = cax 

            if ori_tag is not None: # add colorbar using dummy data
                cb_key = ori_tag + 'cb' + str(n+1)
                A = np.array([[1., 2.],[3., 4.]])
                pim = ax.imshow(A)
                if ori_tag=='v':
                    ori = "vertical"
                else:
                    ori = "horizontal"
                cb = fig.colorbar(pim, cax=cax, orientation=ori, extend='both')
                axes_dic[cb_key] = cb
                if ori_tag=='v':
                    ori = "vertical"
                else:
                    ori = "horizontal"
                    cax.xaxis.set_ticks_position("top")

				# remove cbar if not specified in layout
                if layout.cbars[n] == 0:
                    axes_dic[cax_key] = None
                    axes_dic[cb_key] = None
                    cb.remove()
            else:
                axes_dic[cax_key] = None

    # lastly, apply specifications defined in the layout
    plt.subplots_adjust(left=layout.adjust[0], right=layout.adjust[1],
                        bottom=layout.adjust[2],top=layout.adjust[3],
                        wspace=layout.adjust[4],hspace=layout.adjust[5])

    return fig,axes_dic




### general methods
### ==================================================

# use to choose among layouts in gridspec_helper
def use_layout(name='default', fig_size=None):
    """
    input: a string specifying the layout
    returns: fig,axes handles
    """

    layouts_custom = gridspec_helper.custom_layouts()
    layouts_lite = gridspec_helper.lite_layouts()

    if name in layouts_custom.keys():
        layout = gridspec_helper.custom(name)
        print('{}'.format(layout.art))
        fig,axes = make_figure(layout,name,fig_size)
        return fig,axes
    elif name in layouts_lite.keys():
        layout = gridspec_helper.lite(name)
        fig,axes = make_lite_figure(layout,name,fig_size)
        return fig,axes
    else:
        print('Layout {} not found. Choose from these names:'.format(name))
        help(show_art=False)
        import sys
        sys.exit()


# helper function to plot any layout in gridspec_helper
def plot_layout(name='default'):
    layouts_custom = gridspec_helper.custom_layouts()
    layouts_lite = gridspec_helper.lite_layouts()


    if name in layouts_custom.keys():
        layout = gridspec_helper.custom(name)
        print('{}'.format(layout.art))
        fig,axes = make_figure(layout,name) 
    elif name in layouts_lite.keys():
        layout = gridspec_helper.lite(name)
        fig,axes = make_lite_figure(layout,name) 
    else:
        print('Layout {} not found. Choose from these names:'.format(name))
        help(show_art=False)
        import sys
        sys.exit()
            
    plt.show()



# helper function to show layout names in gridspec_helper
def help(show_art=True):

    layouts_custom = gridspec_helper.custom_layouts()
    layouts_lite = gridspec_helper.lite_layouts()

    if show_art:
        show_logo()

    print('Custom layouts:\n======================')
    for key in layouts_custom.keys():
        layout = layouts_custom[key]
        if show_art:
            print('{}\n{}'.format(key,layout.art))
        else:
            print('{}'.format(key))

    print('\nLite layouts:\n======================')
    for key in layouts_lite.keys():
        print('{}'.format(key))

    print("""\n
    Example of a FigAxe layout array:
    layout= [
            [1,1,1],
            [2,2,3],
            [4,5,3]
            ])

    This corresponds to a 5-axes plot window like 

    +-----------------+
    |        1        |
    +-----------+-----+
    |      2    |     |
    +-----+-----+  3  +
    |  4  |  5  |     |
    +-----+-----+-----+

    - row 1 layout is [1,1,1]
    - row 2 layout is [2,2,3]
    - row 3 layout is [4,5,3]   
    """)

    print('\nUsage:\n======================')
    print('\n-Preview a layout:')
    print('> figaxe.plot_layout(name)')
    print('\n-Use a layout:')
    print('> fig,axs = figaxe.use_layout(name)')
    print('\n-Add new layouts by editing gridspec_helper.py.')



# core method for utilizing gridspec with a layout array
def gridspec_converter(layout):
    layout = np.array(layout)
    h, w = layout.shape
    values_in_arr = sorted(set(layout.flatten()))
    result = []
    grid = GridSpec(h, w)
    for v in values_in_arr:
        xx, yy = ((layout - v) == 0).nonzero()
        result.append(grid[xx.min(): xx.max() + 1,
                           yy.min(): yy.max() + 1])
    return result



# method to assign location of colorbar
def get_cax_location(name,choice):

    choices = {}
    choices['t'] = "top"
    choices['b'] = "bottom"
    choices['l'] = "left"
    choices['r'] = "right"

    err_msg = '[get_cax_location]: %s is an invalid colorbar location. '%choice
    err_msg += 'Choose from:\n {}'.format(choices.keys())

    if choice is None: # then use one of these defaults:
        # put single colorbar for horizontal layouts on the right
        if name[0]=='h' and name[-1]=='1':
            location = "right"
        # for other horizontal layouts, put colorbar on top
        elif name[0]=='h':
            location = "top"
        # for single colorbar vertical layouts, put colorbar on top
        elif name[0]=='v' and name[-1]=='1':
            location = "top"
        # for other vertical layouts, put colorbar on right
        elif name[0]=='v':
            location = "right"
        # for single-panel layouts, use naming convention
        elif name[-1]=='v':
            location = "right"
        elif name[-1]=='h':
            location = "top"
        else: # need the specification array but none given
            location = None #print(err_msg)
    else: # choice must be specified in FigAxe instance
        location = choices.get(choice,err_msg)

    return location



# method to assign orientation of colorbar
def get_cax_orientation(name,choice):

    err_msg = '[get_cax_orientation]: incorrect specification of' 
    err_msg +='FigAxe.caxori for layout %s'%name

    # set default vertical or horizontal orientation
    # based on naming convention
    if choice is None:
        # vertical colorbar for horizontal layouts with 1 cb
        if name[0]=='h' and name[-1]=='1':
            ori_tag = 'v'
        # otherwise horizontal colorbar for horizontal layouts 
        elif name[0]=='h':
            ori_tag = 'h'
        # horizontal colorbar for vertical layouts with 1 cb
        elif name[0]=='v' and name[-1]=='1':
            ori_tag = 'h'
        # otherwise vertical colorbar for vertical layouts 
        elif name[0]=='v':
            ori_tag = 'v'
        # for single-panel layouts, use naming convention
        elif name[-1]=='v':
            ori_tag = 'v'
        elif name[-1]=='h':
            ori_tag = 'h'
        else: # need the specification array but none given
            ori_tag = None #print(err_msg)
    else:
        ori_tag = choice

    return ori_tag



def show_logo():
    print(str("""
     ______  _                                  
    (______)(_)         _______                 
    (_)__    _   ____ ___    |___  ______       
    (____)  (_) |    |__  /| |_  |/_/  _ \      
    (_)     (_) |    |_  ___ |_>  < /  __/      
    (_)     (_) |____|/_/  |_/_/|_| \___/ 
                   (_)                      
                   (_)                      
                   (_)                      
        """))