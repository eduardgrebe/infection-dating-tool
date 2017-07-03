import numpy as np
import numpy.random
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.axes_grid1 import make_axes_locatable

def heat_map_graph(x_value, y_value):
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111)
    x_step = x_value*2.0/64
    xedges = np.arange(0, x_value*2+x_step, x_step)
    y_step = y_value*2.0/64
    yedges = np.arange(y_value/2, y_value*2+y_step, y_step)

    heatmap = np.zeros(shape=(len(yedges),len(xedges)))
    # for x_count, x in enumerate(xedges):
    #     for y_count, y in enumerate(yedges):
    #         heatmap[len(yedges)-y_count-1][len(xedges)-x_count-1] = float(y)*x

    for x_count, x in enumerate(reversed(xedges)):
        for y_count, y in enumerate(reversed(yedges)):
            heatmap[y_count][x_count] = float(y)*x
    
    heatmap = np.flipud(np.transpose(heatmap))
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    # extent = [-3, 3, -3, 3]

    # ax.clf()
    plt.title('Residual risk')
    plt.xlabel('Incidence in donar population')
    plt.ylabel('Window of residual risk')
    
    im = ax.imshow(heatmap, extent=extent)
    ax.set_aspect('auto')

    divider = make_axes_locatable(ax)
    # cax = divider.append_axes("right", size="2.5%", pad=0.3)
    cb = plt.colorbar(im)
    # cb.set_label('')

    plt.show()

    return plt
