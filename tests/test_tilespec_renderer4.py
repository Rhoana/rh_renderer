# Renders a given tilespec as is in full resolution
from __future__ import print_function
import pylab
from rh_renderer.tilespec_renderer import TilespecRenderer
import numpy as np
import time
import json
from rh_renderer import models
from rh_renderer.normalization.histogram_clahe import HistogramCLAHE


if __name__ == '__main__':
    ts_fname = 'tilespec_1tile.json'
    with open(ts_fname, 'r') as data:
        tilespec = json.load(data)


    # Create the tilespec renderer
    renderer1 = TilespecRenderer(tilespec, hist_adjuster=HistogramCLAHE())


    start_time = time.time()
    img1, start_point1 = renderer1.render()
    print("Start point is at:", start_point1, "image shape:", img1.shape, "took: {} seconds".format(time.time() - start_time))
    pylab.figure()
    pylab.imshow(img1, cmap='gray', vmin=0., vmax=255.)


    pylab.show()


