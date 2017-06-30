import numpy as np
import numpy.random
import matplotlib.pyplot as plt

def heat_map_graph(x_value, y_value):
    # x = [0, x_value, x_value*2]
    # y = [y_value/2, y_value, y_value*2]

    # heatmap, xedges, yedges = np.histogram2d(x, y, bins=(64,64))
    heatmap = []
    # x_step = x_value*2.0/64
    # xedges = np.arange(0, x_value*2+x_step, x_step)
    # y_step = y_value*2.0/64
    # yedges = np.arange(y_value/2, y_value*2+y_step, y_step)
    # import pdb;pdb.set_trace()
    xedges = np.arange(1, 2, 0.25)
    yedges = np.arange(1, 6, 1)
    import pdb;pdb.set_trace()
    heatmap = np.zeros(shape=(len(yedges),len(xedges)))
    for x_count, x in enumerate(xedges):
        for y_count, y in enumerate(yedges):
            heatmap[len(yedges)-y_count][x_count] = float(y)*x

    
    heatmap = np.flipud(np.transpose(heatmap))
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    import pdb;pdb.set_trace()
    plt.clf()
    plt.title('Residual risk')
    plt.xlabel('Incidence in donar population')
    plt.ylabel('Window of residual risk')
    plt.imshow(heatmap, extent=extent)
    plt.show()

    return plt
