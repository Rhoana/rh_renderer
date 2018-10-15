# Renders a given tilespec that contains 2 tiles in 1/5 resolution
from __future__ import print_function
import pylab
from rh_renderer.tilespec_renderer import TilespecRenderer
import numpy as np
import time
import json
from rh_renderer import models


if __name__ == '__main__':
    ts_fname = 'tilespec_2tiles.json'
    with open(ts_fname, 'r') as data:
        tilespec = json.load(data)


    # Create the tilespec renderer
    renderer1 = TilespecRenderer(tilespec)

    downsample = models.AffineModel(np.array([
                                              [0.2, 0., 0.],
                                              [0., 0.2, 0.],
                                              [0., 0., 1.]
                                             ]))

    renderer1.add_transformation(downsample)

    start_time = time.time()
    img1, start_point1 = renderer1.render()
    print("Start point is at:", start_point1, "image shape:", img1.shape, "took: {} seconds".format(time.time() - start_time))
    pylab.figure()
    pylab.imshow(img1, cmap='gray', vmin=0., vmax=255.)


    pylab.show()


