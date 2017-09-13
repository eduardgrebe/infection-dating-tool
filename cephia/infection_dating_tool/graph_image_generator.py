import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
matplotlib.use('Agg')

def heat_map_graph(x_value, y_value, upper_limit, number_of_donations=None):
    fig = plt.figure(figsize=(15, 15))
    ax = fig.add_subplot(111)

    if not upper_limit:
        x_step = x_value*2.0/64
        xedges = np.arange(0, x_value*2+x_step, x_step)
        y_step = y_value*2.0/64
        yedges = np.arange(0, y_value*2+y_step, y_step)
    else:
        x_step = upper_limit/64
        xedges = np.arange(0, upper_limit+x_step, x_step)
        y_step = y_value*upper_limit/64
        yedges = np.arange(0, y_value*2+y_step, y_step)

    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(20)

    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(20)

    heatmap = np.zeros(shape=(len(yedges), len(xedges)))

    for x_count, x in enumerate(xedges):
        for y_count, y in enumerate(yedges):
            if not number_of_donations:
                # (window/365)*(incidence) # risk per donation in %
                heatmap[y_count][x_count] = float(y/365)*x
            else:
                # (float(y/365)*x)/100 * num_donations
                heatmap[y_count][x_count] = (float(y/365)*x)/100 * number_of_donations

    heatmap = np.flipud(np.transpose(heatmap))
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    plt.xlabel('Incidence in donor population (% p.a.)', fontsize=30)
    plt.ylabel('Window of residual risk (days)', fontsize=30)

    im = ax.imshow(heatmap, extent=extent, cmap='jet')
    ax.set_aspect('auto')

    divider = make_axes_locatable(ax)
    cb = plt.colorbar(im)
    cb.ax.tick_params(labelsize=20)
    if not number_of_donations:
        title = plt.title('Residual risk per donation\n(incidence x infectious window)', fontsize=35)
        cb.set_label('Probability per donation (%)', fontsize=30)
    else:
        title = plt.title('Expected number of infectious donations\n(incidence x infectious window)', fontsize=35)
        cb.set_label('Expected number of infectious donations', fontsize=30)
    title.set_position([0.5, 1.02])

    plt.show()
    return plt
