
import numpy as np
import pylab as plt
from matplotlib.gridspec import GridSpec
from importlib import reload
import gridspec_helper; reload(gridspec_helper)

# import style file
plt.style.use(r"custom.mplstyle")



### methods for lite layouts
### ==================================================

# use to choose among lite layouts in gridspec_helper
def lite_layout(name=None, fig_size=None):
    """
    input: a string specifying the layout
    returns: fig,axes handles
    """

    try:
        layout = gridspec_helper.lite(name)
        fig,axes = make_lite_figure(layout,fig_size)
        return fig,axes
    except:
        print('[lite_layout]: exception thrown for layout {}.')
        print("""
            Example of a FigAxe layout array:
            layout= [
                    [1,1,1],
                    [2,2,3],
                    [4,5,3]
                    ])

            This corresponds to a 5-axes plot window like 

            +-----------------+
            |        1        |
            +-----------------+
            |      2    |     |
            +-----+-----+  3  +
            |  4  |  5  |     |
            +-----+---+-------+
 
            - row 1 layout is [1,1,1]
            - row 2 layout is [2,2,3]
            - row 3 layout is [4,5,3]   
        """)



# called by lite_layout() 
def make_lite_figure(layout,fig_size=None):
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
        axes_dic[str(i)] = fig.add_subplot(gridspec)


    # add inward-pointing ticks on all 4 sides and set their visibility
    for idx,key in enumerate(axes_dic.keys()):
        ax = axes_dic[key]
        ax.minorticks_on()
        ax.xaxis.set_ticks_position('both')
        ax.yaxis.set_ticks_position('both')
        ax.tick_params(axis='both', direction='in',width=1.) 
        ax.tick_params(which='minor',axis='both',direction='in',width=1.) 


    # add cbar axes
    Nax = len(gridspecs)
    for n in range(Nax):
        cbar_key = str(n+1) + 'cb'
        axes_dic[cbar_key] = 1


    plt.tight_layout()

    return fig,axes_dic




### methods for custom layouts
### ==================================================

# use to choose among lite layouts in gridspec_helper
def custom_layout(name='default', fig_size=None):
    """
    input: a string specifying the layout
    returns: fig,axes handles
    """

    try:
        layout = gridspec_helper.custom(name)
        fig,axes = make_figure(layout,fig_size)
        return fig,axes
    except:
        print('Layout {} not found. Choose from these names:'.format(name))
        show_layouts(show_art=False)



# called by custom_layout()
def make_figure(layout,fig_size=None):
    """
    input: an instance of LiteFigAxe 
    returns: fig,axes handles
    """

    if fig_size == None:
        fig_size = tuple(layout.size)

    fig = plt.figure(figsize=fig_size)
    gridspecs = gridspec_converter(layout.layout)
    ax1 = fig.add_subplot(gridspecs[layout.head-1])

    axes_dic = {str(layout.head): ax1}
    # The axes are stored in gridspec in the order specified in the layout_array
    # so we just need to fill a dic with keys named '1','2','3',etc.
    # Here we do that while accounting for the shared axes specification
    idx = 1
    for gridspec,share_x,share_y in zip(gridspecs,layout.share_x,layout.share_y):
        if gridspec != gridspecs[layout.head-1]:
            if share_x > 0 and share_y > 0:
                axes_dic[str(idx)] = fig.add_subplot(gridspec,sharex=ax1,sharey=ax1)
            elif share_x > 0:
                axes_dic[str(idx)] = fig.add_subplot(gridspec,sharex=ax1)
            elif share_y > 0:
                axes_dic[str(idx)] = fig.add_subplot(gridspec,sharey=ax1)
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


    # add cbar axes
    Nax = len(gridspecs)
    for n in range(Nax):
        if layout.cbars[n] == 1:
            cbar_key = str(n+1) + 'cb'
            axes_dic[cbar_key] = layout.cbars[n]


    # finally, apply specifications defined in the layout
    plt.subplots_adjust(left=layout.adjust[0], right=layout.adjust[1],
                        bottom=layout.adjust[2],top=layout.adjust[3],
                        wspace=layout.adjust[4],hspace=layout.adjust[5])

    return fig,axes_dic




### general methods
### ==================================================

# helper function to plot any layout in gridspec_helper
def plot_layout(name='default'):

    layouts_custom = gridspec_helper.custom_layouts()
    layouts_lite = gridspec_helper.lite_layouts()

    if name in layouts_custom.keys():
        layout = gridspec_helper.custom(name)
    elif name in layouts_lite.keys():
        layout = gridspec_helper.lite(name)
    else:
        print('Layout {} not found. Choose from these names:'.format(name))
        show_layouts(show_art=False)
        import sys
        sys.exit()

    fig,axes = make_figure(layout)             
    plt.show()



# helper function to show layout names in gridspec_helper
def show_layouts(show_art=True):

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

    print('\nQuick layouts:\n======================')
    for key in layouts_lite.keys():
        print('{}'.format(key))



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