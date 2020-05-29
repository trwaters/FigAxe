from dataclasses import dataclass


### classes defining layouts
### ==================================================

@dataclass
class LiteFigAxe:
    size    : list
    layout  : list

    # optional parameters
    cbars   : list = None   # list of 1s,0s for cbar or no cbar
    caxloc  : list = None   # list of strings specifying the location of the 
                            # colorbar (choices are 't','b','l','r')
    caxori  : list = None   # list of strings, either 'v' or 'h', specifying 
                            # a vertical or horizontal orientation
    
    def __post_init__(self):
        Npanels = max(max(self.layout))
        panels = range(Npanels)

        # set no colorbars by default
        if self.cbars is None:
            self.cbars = [0 for val in panels]

        # set default caxloc and caxori
        if self.caxloc is None:
            self.caxloc = [None for val in panels]
        if self.caxori is None:
            self.caxori = [None for val in panels]


@dataclass
class FigAxe:
    size    : list  # array of fig_size, e.g. [5,4] (row,col)
    layout  : list  # arrays specifying gridspec layout
    art     : str   # ascii art representing the layout
    cbars   : list  # list of 1s,0s for cbar or no cbar
    adjust  : list  # subplots_adjust params

    # optional parameters
    head    : int = 1       # specifies main plot in layout_array 
    share_x : list = None   # list of 1s,0s; 1 means share head's x-axis
    share_y : list = None   # list of 1s,0s; 1 means share head's y-axis
    hide_x  : list = None   # list of 1s,0s; 1 means hide x-axis tick labels
    hide_y  : list = None   # list of 1s,0s; 1 means hide y-axis tick labels
    caxloc  : list = None   # list of strings specifying the location of the 
                            # colorbar (choices are 't','b','l','r')
    caxori  : list = None   # list of strings, either 'v' or 'h', specifying 
                            # a vertical or horizontal orientation
    
    def __post_init__(self):
        Npanels = max(max(self.layout))
        panels = range(Npanels)

        # by default, do not share limits of hide axes tick labels
        zero_array = [0 for val in panels]
        if self.share_x is None:
            self.share_x = zero_array
        if self.share_y is None:
            self.share_y = zero_array
        if self.hide_x is None:
            self.hide_x = zero_array
        if self.hide_y is None:
            self.hide_y = zero_array

        # set default caxloc and caxori
        if self.caxloc is None:
            self.caxloc = [None for val in panels]
        if self.caxori is None:
            self.caxori = [None for val in panels]



### methods utilzing above classes
### ==================================================

# use to quickly try out a new layout
def lite_layouts():
    """
    Add your own custom figure size and layout below
    for immediate use.  

    Here's a different 5-axes plot window, which comes from
    the matplotlib gallery for Gridspec
    (google "Using Gridspec to make multi-column/row subplot layouts")

    +-----------------+
    |        1        |
    +-----------+-----+
    |      2    |     |
    +-----+-----+  3  +
    |  4  |  5  |     |
    +-----+-----+-----+

    This layout is represented by an array of three arrays, 
    - row 1 array is [1,1,1]
    - row 2 array is [2,2,3]
    - row 3 array is [4,5,3]   

    Run figaxe.plot_layout('demo5a') to see the plot.

    As a 2nd example, the following 5-axes plot layout
    +-------+-------+---+
    |       |   2   | 3 |
    +   1   +-------+---+
    |       |   4   | 5 |
    +-------+-------+---+

    is represented by an array of two arrays, 
    - row 1 array is [1,1,2,2,3]
    - row 2 array is [1,1,4,4,5]

    Run figaxe.lite_layout('demo5b') to see the fig handle along
    with a dictionary containing handles to these 5 axes.

    Run figaxe.plot_layout('demo5b') to preview.
    Run also figaxe.plot_layout('demo5c') and compare with
    that made with the FigAxe class, figaxe.plot_layout('g5a')
    """

    layout_dic = {

    'demo5a' : LiteFigAxe( (8.,6.),
        [
        [1,1,1],
        [2,2,3],
        [4,5,3]
        ]
        ),
    'demo5b' : LiteFigAxe( (10.,6.),
        [
        [1,1,2,2,3],
        [1,1,4,4,5]
        ]
        ),
    'demo5c' : LiteFigAxe( (9.5,3.4),
        [
        [1,1,2,2,3],
        [1,1,4,4,5]
        ],
        cbars = [1,0,1,0,1],                # add colors to axes 1,3,& 5
        caxloc = ['t',None,'r',None,'r'],   # place on top, right & right
        caxori = ['h',None,'v',None,'v']    # horiz, vert, & vert orientation
        ),
    }

    return layout_dic
        

# use to add new layouts and edit existing ones 
def custom_layouts():

    layout_dic = {

    ##  SINGLE PANEL LAYOUTS
    ### ==================================================

    'default' : FigAxe( (7.,7.),
        [
        [1]
        ],
        str("""
        +---+
        | 1 |
        +---+
        """),
        [0],    # no colorbar
        [0.1,0.98,0.08,0.94,0.02,0.03]  # params: L,R,bot,top,wspace,hspace
        ),
    'cb1h' : FigAxe( (6.7,7.), # naming convention specifies horizontal cbar
        [
        [1]
        ],
        str("""
          c
        +---+
        | 1 |
        +---+
        """),
        [1],    # 1 colorbar
        [0.1,0.99,0.07,0.92,0.02,0.03]  # params: L,R,bot,top,wspace,hspace
        ),
    'cb1v' : FigAxe( (8.,7.),  # naming convention specifies vertical cbar
        [
        [1]
        ],
        str("""
        +---+
        | 1 |c
        +---+
        """),
        [1],    # colorbars
        [0.05,0.96,0.07,0.94,0.02,0.03]  # params: L,R,bot,top,wspace,hspace
        ),

    ##  MULTI-PANEL LAYOUTS WITHOUT COLORBARS
    ### ==================================================

    '1by2a' : FigAxe( (9.,5.),
        [
        [1,2]
        ],
        str("""
        +---+---+
        | 1 | 2 |
        +---+---+
        """),
        [0,0],    # no colorbars
        [0.07,0.98,0.1,0.92,0.03,0.03],  # params: L,R,bot,top,wspace,hspace

        # enable these optionals
        share_x = [0,1],  # panel 2 shares xlim of panel 1
        share_y = [0,1],  # panel 2 shares ylim of panel 1
        hide_y =  [0,1],  # hide y-tick labels on panel 2
        ),

    '1by2b' : FigAxe( (10.,5.),
        [
        [1,1,2]
        ],
        str("""
        +-------+---+
        |   1   | 2 |
        +-------+---+
        """),
        [0,0],    # no colorbars
        [0.07,0.98,0.1,0.92,0.03,0.03],  # params: L,R,bot,top,wspace,hspace

        # enable these optionals
        share_y = [0,1],  # panel 2 shares ylim of panel 1
        hide_y =  [0,1],  # hide y-tick labels on panel 2
        ),

    '2by1a' : FigAxe( (5.,6.5),
        [
        [1],
        [2],
        ],
        str("""
        +---+
        | 1 |
        +---+
        | 2 |
        +---+
        """),
        [0,0],    # no colorbars
        [0.12,0.97,0.08,0.94,0.03,0.03],  # params: L,R,bot,top,wspace,hspace

        # enable these optionals
        share_x = [0,1],  # panel 2 shares xlim of panel 1
        share_y = [0,1],  # panel 2 shares ylim of panel 1
        hide_x =  [1,0],  # hide y-tick labels on panel 2
        ),
    '2by1b' : FigAxe( (5.,6.5),
        [
        [1],
        [1],
        [2],
        ],
        str("""
        +---+
        |   |
        | 1 |
        |   |
        +---+
        | 2 |
        +---+
        """),
        [0,0],    # no colorbars
        [0.12,0.97,0.08,0.94,0.03,0.03],  # params: L,R,bot,top,wspace,hspace

        # enable these optionals
        share_x = [0,1],  # panel 2 shares xlim of panel 1
        share_y = [0,1],  # panel 2 shares ylim of panel 1
        hide_x =  [1,0],  # hide y-tick labels on panel 2
        ),

    ##  HORIZONTAL LAYOUTS WITH COLORBARS
    ### ==================================================

    'h2' : FigAxe( (8.5,5.1),
        [
        [1,2]
        ],
        str("""
          c   c 
        +---+---+
        | 1 | 2 |
        +---+---+
        """),
        [1,1],  # colorbars
        [0.05,0.99,0.07,0.9,0.02,0.03],  # params: L,R,bot,top,wspace,hspace

        # enable these optionals
        share_x = [0,1],  # panel 2 shares xlim of panel 1
        share_y = [0,1],  # panel 2 shares ylim of panel 1
        hide_y =  [0,1],  # hide y-tick labels on panel 2
        ),
    'h2cb1' : FigAxe( (8.,5.),
        [
        [1,2]
        ],
        str("""
        +---+---+ 
        | 1 | 2 |c
        +---+---+
        """),
        [0,1],  # colorbars
        [0.05,0.99,0.07,0.9,0.02,0.03],  # params: L,R,bot,top,wspace,hspace

        # enable these optionals
        share_x = [0,1],  # panel 2 shares xlim of panel 1
        share_y = [0,1],  # panel 2 shares ylim of panel 1
        hide_y =  [0,1],  # hide y-tick labels on panel 2
        ),
    'h3' : FigAxe( (10.,4.2),
        [         # layout_array
        [1,2,3]
        ],
        str("""
          c   c   c  
        +---+---+---+
        | 1 | 2 | 3 |
        +---+---+---+
        """),
        [1,1,1],  # colorbars
        [0.04,0.99,0.06,0.91,0.02,0.03],  # params: L,R,bot,top,wspace,hspace

        # enable these optionals
        share_x = [0,1,1],  # panels 2,3 share xlim of panel 1
        share_y = [0,1,1],  # panels 2,3 share ylim of panel 1
        hide_y =  [0,1,1],  # hide y-tick labels on panels 2 and 3
        ),
    'h3cb1' : FigAxe( (10.5,3.7),
        [         # layout_array
        [1,2,3]
        ],
        str("""
        +---+---+---+
        | 1 | 2 | 3 |c
        +---+---+---+
        """),
        [0,0,1],  # colorbars
        [0.04,0.94,0.06,0.98,0.01,0.03],  # params: L,R,bot,top,wspace,hspace

        # enable these optionals
        share_x = [0,1,1],  # panels 2,3 share xlim of panel 1
        share_y = [0,1,1],  # panels 2,3 share ylim of panel 1
        hide_y =  [0,1,1],  # hide y-tick labels on panels 2 and 3
        ),
    'h4' : FigAxe( (12.,4.),
        [         # layout_array
        [1,2,3,4]
        ],
        str("""
          c   c   c   c
        +---+---+---+---+
        | 1 | 2 | 3 | 4 |
        +---+---+---+---+
        """),
        [1,1,1,1],  # colorbars
        [0.06,0.99,0.06,0.91,0.02,0.03],  # params: L,R,bot,top,wspace,hspace

        # enable these optionals
        share_x = [0,1,1,1],  # panels 2,3 share xlim of panel 1
        share_y = [0,1,1,1],  # panels 2,3 share ylim of panel 1
        hide_y =  [0,1,1,1],  # hide y-tick labels on panels 2 and 3
        ),
    'h4cb1' : FigAxe( (13.5,3.4),
        [         # layout_array
        [1,2,3,4]
        ],
        str("""
        +---+---+---+---+
        | 1 | 2 | 3 | 4 |c
        +---+---+---+---+
        """),
        [0,0,0,1],  # colorbars
        [0.05,0.94,0.05,0.98,0.01,0.03],  # params: L,R,bot,top,wspace,hspace

        # enable these optionals
        share_x = [0,1,1,1],  # panels 2,3 share xlim of panel 1
        share_y = [0,1,1,1],  # panels 2,3 share ylim of panel 1
        hide_y =  [0,1,1,1],  # hide y-tick labels on panels 2 and 3
        ),

    ### VERTICAL LAYOUTS WITH COLORBARS
    ### ==================================================

    'v2' : FigAxe( (4.7,7.),
        [         # layout_array
        [1],
        [2]
        ],
        str("""
        +---+
        | 1 |c
        +---+
        | 2 |c
        +---+
        """),
        [1,1],  # colorbars
        [0.06,0.95,0.06,0.95,0.02,0.05],  # params: L,R,bot,top,wspace,hspace

        # enable these optionals 
        share_x = [0,1],  # panels 2,3 share xlim of panel 1
        hide_x =  [1,0],  # hide x-tick labels on panels 1 and 2
        ),
    'v2cb1' : FigAxe( (3.8,6.5),
        [         # layout_array
        [1],
        [2]
        ],
        str("""
          c  
        +---+
        | 1 | 
        +---+
        | 2 |
        +---+
        """),
        [1,0],  # colorbars
        [0.1,0.99,0.06,0.92,0.02,0.05],  # params: L,R,bot,top,wspace,hspace

        # enable these optionals 
        share_x = [0,1],  # panels 2,3 share xlim of panel 1
        share_y = [0,1],  # panels 2,3 share ylim of panel 1
        hide_x =  [1,0],  # hide x-tick labels on panels 1 and 2
        ),
    'v3' : FigAxe( (3.5,10.),
        [         # layout_array
        [1],
        [2],
        [3]
        ],
        str("""
        +---+
        | 1 |c
        +---+
        | 2 |c
        +---+
        | 3 |c
        +---+
        """),
        [1,1,1],  # colorbars
        [0.06,0.93,0.06,0.95,0.02,0.05],  # params: L,R,bot,top,wspace,hspace

        # enable these optionals 
        share_x = [0,1,1],  # panels 2,3 share xlim of panel 1
        hide_x =  [1,1,0],  # hide x-tick labels on panels 1 and 2
        ),
    'v3cb1' : FigAxe( (3.,10.),
        [         # layout_array
        [1],
        [2],
        [3]
        ],
        str("""
          c  
        +---+
        | 1 | 
        +---+
        | 2 |
        +---+
        | 3 |
        +---+
        """),
        [1,0,0],  # colorbars
        [0.1,0.99,0.06,0.92,0.02,0.05],  # params: L,R,bot,top,wspace,hspace

        # enable these optionals 
        share_x = [0,1,1],  # panels 2,3 share xlim of panel 1
        share_y = [0,1,1],  # panels 2,3 share ylim of panel 1
        hide_x =  [1,1,0],  # hide x-tick labels on panels 1 and 2
        ),

    ##  GRID LAYOUTS WITH COLORBARS
    ### ==================================================

    'g3a' : FigAxe( (8.5,5.),
        [         # layout_array
        [1,1,2],
        [1,1,3],
        ],
        str(""" 
        +-------+---+  
        |       | 2 |c  
        |   1   +---+   
        |       | 3 |c 
        +-------+---+ 
        """),
        [0,1,1],  # colorbars
        [0.08,0.92,0.1,0.92,0.2,0.05],  # params: L,R,bot,top,wspace,hspace

        # enable these optionals 
        head    = 2,
        share_x = [0,0,1],  # panel 3 shares xlim of panel 2
        share_y = [0,0,1],  # panel 3 shares ylim of panel 2
        hide_x =  [0,1,0],  # hide x-tick labels on panel 2
        caxloc =  [None,'r','r'],
        caxori =  [None,'v','v'],
        ),

    'g5a' : FigAxe( (10.5,3.4),
        [         # layout_array
        [1,1,2,2,3],
        [1,1,4,4,5],
        ],
        str(""" 
            c  
        +-------+-------+---+  
        |       |   2   | 3 |c 
        +   1   +-------+---+  
        |       |   4   | 5 |c  
        +-------+-------+---+   
        """),
        [1,0,1,0,1],  # colorbars
        [0.05,0.92,0.12,0.92,0.3,0.05],  # params: L,R,bot,top,wspace,hspace

        # enable these optionals 
        head    = 2,            # change head axis (for sharing)
        share_x = [0,0,0,1,0],  # panel 4 shares xlim of panel 2
        share_y = [0,0,1,1,1],  # panels 3,4,5 share ylim of panel 2
        hide_x =  [0,1,1,0,0],  # hide x-tick labels on head & panel 3 
        caxloc =  ['t',None,'r',None,'r'],
        caxori =  ['h',None,'v',None,'v'],
        ),

    } # close dictionary


    return layout_dic



### case-switches to choose a layout
### ==================================================

def lite(name):
    layout_dic = lite_layouts()
    return layout_dic.get(name, '[quick_layout]: layout {} not found.'.format(name))


def custom(name):
    layout_dic = custom_layouts()
    return layout_dic.get(name, '[custom_layout]: layout {} not found.'.format(name))