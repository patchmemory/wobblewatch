import os, sys
import matplotlib
from matplotlib import cm
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Wedge, Rectangle

FC_1 = 'w'
FC_2 = 'w'
FC_3 = 'w'
ALPHA_METER = 0.9

class RiskMeter:

    def __init__(self, val, val_max = 1):
        if val < 0:
            self.val = 0
        elif val > val_max:
            self.val = val_max
        else:
            self.val = val
        
        self.fname='web/assets/meter.png'

        self.cat_names = [  'Very\nLow',
                            'Low',
                            'Medium',
                            'High',
                            'Very\nHigh'    ]

        self.cat_color = [  "#349F93",
                            "#F6DD79",
                            "#EBA447",
                            "#FF7C0A",
                            "#E00000"   ]

        self.gauge()

    def update(self, val):
        self.val = val
        self.gauge()

    def degree_range(self, n):
        start = np.linspace(0,180,n+1, endpoint=True)[0:-1]
        end = np.linspace(0,180,n+1, endpoint=True)[1::]
        mid_points = start + ((end-start)/2.)
        return np.c_[start, end], mid_points

    def rot_position(self, val, val_max=1):
        return 180 * ( 1 - val/val_max )

    def rot_text(self, ang):
        rotation = np.degrees(np.radians(ang) * np.pi / np.pi - np.radians(90))
        return rotation

    def gauge(self, val_max = 1, title='Fall Risk'):

        """
        some sanity checks first

        """

        labels = self.cat_names
        N = len(labels)

        #if arrow > N:
        #    raise Exception("\n\nThe category ({}) is greated than \
        #    the length\nof the labels ({})".format(arrow, N))


        """
        if colors is a string, we assume it's a matplotlib colormap
        and we discretize in N discrete colors
        """
        colors = self.cat_color
        if isinstance(colors, str):
            cmap = cm.get_cmap(colors, N)
            cmap = cmap(np.arange(N))
            colors = cmap[::-1,:].tolist()
        if isinstance(colors, list):
            if len(colors) == N:
                colors = colors[::-1]
            else:
                raise Exception("\n\nnumber of colors {} not equal \
                to number of categories{}\n".format(len(colors), N))

        """
        begins the plotting
        """

        fig, ax = plt.subplots(facecolor=FC_1)

        ang_range, mid_points = self.degree_range(N)

        labels = labels[::-1]

        """
        plots the sectors and the arcs
        """
        patches = []
        for ang, c in zip(ang_range, colors):
            # sectors
            patches.append(Wedge((0.,0.), .4, *ang, facecolor=FC_2, lw=2))
            # arcs
            patches.append(Wedge((0.,0.), .43, *ang, width=0.17, facecolor=c, lw=2, alpha=ALPHA_METER))

        [ax.add_patch(p) for p in patches]


        """
        set the labels (e.g. 'LOW','MEDIUM',...)
        """

        for mid, lab in zip(mid_points, labels):

            ax.text(0.35 * np.cos(np.radians(mid)), 0.35 * np.sin(np.radians(mid)), lab, \
                horizontalalignment='center', verticalalignment='center', fontsize=19, \
                fontweight='bold', rotation = self.rot_text(mid))

        """
        set the bottom banner and the title
        """
        r = Rectangle((-0.4,-0.1),0.8,0.1, facecolor=FC_3, lw=2, alpha=0.5)
        ax.add_patch(r)

        ax.text(0, -0.13, title, horizontalalignment='center', \
             verticalalignment='center', fontsize=36, fontweight='bold')

        """
        plots the arrow now
        """

        #pos = mid_points[abs(arrow - N)]
        pos = self.rot_position(self.val,val_max)

        l_arrow = 0.23
        ax.arrow(0, 0,
                 l_arrow * np.cos(np.radians(pos)),
                 l_arrow * np.sin(np.radians(pos)),
                 width=0.07, head_width=0.13, head_length=0.07,
                 fc='k', ec='k')

        ax.add_patch(Circle((0, 0), radius=0.035, facecolor='k'))
        #ax.add_patch(Circle((0, 0), radius=0.01, facecolor='w', zorder=11))

        """
        removes frame and ticks, and makes axis equal and tight
        """

        ax.set_frame_on(False)
        ax.axes.set_xticks([])
        ax.axes.set_yticks([])
        ax.axis('equal')
        plt.tight_layout()
        if self.fname:
            fig.savefig(self.fname, dpi=200)
        else:
            plt.show()

        plt.clf()
