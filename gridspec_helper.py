from dataclasses import dataclass
# import numpy as np

### Classes defining layouts
### ==================================================

@dataclass
class LiteFigAxe:
    size    : list
    layout  : list


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

    # by default, do not share limits of hide axes tick labels
    def __post_init__(self, debug=False):
        Npanels = max(max(self.layout))
        zero_array = [0 for val in range(Npanels)]
        if self.share_x is None:
            self.share_x = zero_array
        if self.share_y is None:
            self.share_y = zero_array
        if self.hide_x is None:
            self.hide_x = zero_array
        if self.hide_y is None:
            self.hide_y = zero_array

        if debug:
            print("[__post_init__]:")
            print(self.share_x)
            print(self.hide_x)


### methods utilzing above classes
### ==================================================

# use to quickly try out a new layout
def lite_layouts():
    """
    Add your own custom figure size and layout below
    for immediate use.  

    Below is an example for how to make the following 
    5-axes plot window 
    +-------+---+-------+
    |       |   2   | 3 |
    +   1   +---+-------+
    |       |   4   | 5 |
    +-------+---+-------+

    This layout is represented by an array of two arrays, 
    - row 1 array is [1,1,2,2,3]
    - row 2 array is [1,1,4,4,5]

    Here's a different 5-axes plot window, which comes from
    the matplotlib gallery for Gridspec
    (google "Using Gridspec to make multi-column/row subplot layouts")

    +-----------------+
    |        1        |
    +-----------------+
    |      2    |     |
    +-----+-----+  3  +
    |  4  |  5  |     |
    +-----+---+-------+

    This layout is represented by an array of three arrays, 
    - row 1 array is [1,1,1]
    - row 2 array is [2,2,3]
    - row 3 array is [4,5,3]   

    Then quick_figure() will return the fig handle along
    with a dictionary containing handles to these 5 axes.
    """

    layout_dic = {
    'demo5a' : LiteFigAxe((10.,6.),
        [
        [1,1,2,2,3],
        [1,1,4,4,5]
        ]
        ),
    'demo5b' : LiteFigAxe((8.,6.),
        [
        [1,1,1],
        [2,2,3],
        [4,5,3]
        ]
        ),
    }

    return layout_dic
        

# use to add your frequently used layouts 
def custom_layouts():

    layout_dic = {
    'default' : FigAxe((7.,7.),
        [
        [1]
        ],
        str("""
        +---+
        | 1 |
        +---+
        """),
        [0],    # colorbars
        [0.08,0.99,0.07,0.94,0.02,0.03]  # params: L,R,bot,top,wspace,hspace
        ),
    'h1' : FigAxe((7.,7.),
        [
        [1]
        ],
        str("""
        +---+
        | 1 |c
        +---+
        """),
        [1],    # colorbars
        [0.08,0.99,0.07,0.94,0.02,0.03]  # params: L,R,bot,top,wspace,hspace
        ),
    'h2' : FigAxe((8.5,5.1),
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
    'h2cb1' : FigAxe((8.,5.),
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
    'h3' : FigAxe((10.,4.2),
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
    'h3cb1' : FigAxe((10.5,3.7),
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
    'h4' : FigAxe((12.,4.2),
        [         # layout_array
        [1,2,3,4]
        ],
        str("""
          c   c   c   c
        +---+---+---+---+
        | 1 | 2 | 3 | 4 |
        +---+---+---+---+
        """),
        [1,1,1],  # colorbars
        [0.04,0.99,0.06,0.91,0.02,0.03],  # params: L,R,bot,top,wspace,hspace

        # enable these optionals
        head    = 2,          # make panel 2 the head axes 
        share_x = [0,0,1,1],  # panels 2,3 share xlim of panel 1
        share_y = [0,0,1,1],  # panels 2,3 share ylim of panel 1
        hide_y =  [0,0,1,1],  # hide y-tick labels on panels 2 and 3
        ),
    'h4cb1' : FigAxe((10.5,3.7),
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
    'v3cb1' : FigAxe((4.,10.5),
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
        [0.12,0.98,0.05,0.95,0.02,0.05],  # params: L,R,bot,top,wspace,hspace

        # enable these optionals 
        share_x = [0,1,1],  # panels 2,3 share xlim of panel 1
        share_y = [0,1,1],  # panels 2,3 share ylim of panel 1
        hide_x =  [1,1,0],  # hide x-tick labels on panels 1 and 2
        )
    } # close
                # club4am_layout('h4',          (10.,4.),
                #                               [
                #                               [1,2,3]
                #                               ],
                #                           str("""
                #                           +---+---+---+---+
                #                           | 1 | 2 | 3 | 4 |
                #                           +---+---+---+---+
                #                           """)
                #                               ),
                # club4am_layout('h5',          (12.,4.),
                #                               [
                #                               [1,2,3]
                #                               ],
                #                           str("""
                #                           +---+---+---+---+---+
                #                           | 1 | 2 | 3 | 4 | 5 |
                #                           +---+---+---+---+---+
                #                           """)
                #                               ),
                # club4am_layout('h6',          (14.,4.),
                #                               [
                #                               [1,2,3]
                #                               ],
                #                           str("""
                #                           +---+---+---+---+---+---+
                #                           | 1 | 2 | 3 | 4 | 5 | 6 |
                #                           +---+---+---+---+---+---+
                #                           """)
                #                               ),
                # club4am_layout('g3',          (6.,4.),
                #                               [
                #                               [1, 1, 3],
                #                       [2, 2, 3],
                #                       [2, 2, 3],
                #                               ],
                #                           str("""
                #                           +------------+----+
                #                           |     1      |    |
                #                           | ---------- |    |
                #                           |            |  3 |
                #                           |     2      |    |
                #                           |            |    |
                #                           +------------+----+
                #                           """)
                                           # )

    return layout_dic


### implementation of a case-switch to choose a layout
### ==================================================

def lite(name):
    # if name is None:
    #     name = 'demo5b'
    layout_dic = lite_layouts()
    return layout_dic.get(name, '[quick_layout]: layout {} not found.'.format(name))


def custom(name):
    layout_dic = custom_layouts()
    return layout_dic.get(name, '[custom_layout]: layout {} not found.'.format(name))