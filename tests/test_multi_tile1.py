from __future__ import print_function
import pylab
from rh_renderer.multiple_tiles_affine_renderer import MultipleTilesAffineRenderer
from rh_renderer.single_tile_affine_renderer import SingleTileAffineRenderer
import math
import numpy as np
import time

def get_rigid_matrix(t):
    splitted = t.split()
    r = float(splitted[0])
    cos_val = np.cos(r)
    sin_val = np.sin(r)
    delta = np.array([float(d) for d in splitted[1:]])
    return np.vstack([
            [cos_val, -sin_val, delta[0]],
            [sin_val, cos_val, delta[1]]
    ])



if __name__ == '__main__':

    img_paths = [
            'images/tile1.bmp',
            'images/tile2.bmp'
        ]
    img_shapes = [
            (2976, 3348),
            (2976, 3348)
        ]
    # Rigid transforms
    transform_models = [
            '0.000385855181988 15014.2735713 11052.6315792',
            '0.000472672980423 18213.433402 11034.7113096'
        ]

    transform_matrices = [get_rigid_matrix(t) for t in transform_models]

    # Create all single tiles, and add their transformations
    single_tiles = [SingleTileAffineRenderer(img_path, img_shape[1], img_shape[0], compute_mask=True, compute_distances=True) for
                        img_path, img_shape in zip(img_paths, img_shapes)]
    for single_tile, matrix in zip(single_tiles, transform_matrices):
        single_tile.add_transformation(matrix)

    # Create multiple tiles renderer using different blending techniques
    renderer1 = MultipleTilesAffineRenderer(single_tiles, blend_type="NO_BLENDING")
    renderer2 = MultipleTilesAffineRenderer(single_tiles, blend_type="AVERAGING")
    renderer3 = MultipleTilesAffineRenderer(single_tiles, blend_type="LINEAR")


    start_time = time.time()
    img1, start_point1 = renderer1.render()
    print("NO_BLENDING Before transformations: Start point is at:", start_point1, "image shape:", img1.shape, "took: {} seconds".format(time.time() - start_time))
    pylab.figure()
    pylab.imshow(img1, cmap='gray', vmin=0., vmax=255.)


    start_time = time.time()
    img2, start_point2 = renderer2.render()
    print("AVERAGING Before transformations: Start point is at:", start_point2, "image shape:", img2.shape, "took: {} seconds".format(time.time() - start_time))
    pylab.figure()
    pylab.imshow(img2, cmap='gray', vmin=0., vmax=255.)

    start_time = time.time()
    img3, start_point3 = renderer3.render()
    print("LINEAR Before transformations: Start point is at:", start_point3, "image shape:", img3.shape, "took: {} seconds".format(time.time() - start_time))
    pylab.figure()
    pylab.imshow(img3, cmap='gray', vmin=0., vmax=255.)

    #transform_45 = np.array([[math.cos(math.pi/4), -math.sin(math.pi/4), 1000.0], [math.sin(math.pi/4), math.cos(math.pi/4), 1500.0]])
#    transform_45 = np.array([[math.cos(math.pi/4), -math.sin(math.pi/4), 10.0], [math.sin(math.pi/4), math.cos(math.pi/4), 15.0]])
#
#    transforms = [transform_45] * 4
#    for t in transforms:
#        print "Adding transformation:", t
#        renderer.add_transformation(t)
#        img, start_point = renderer.render()
#
#        print "Start point is at:", start_point, "image shape:", img.shape
#        pylab.figure()
#        pylab.imshow(img, cmap='gray', vmin=0., vmax=255.)

    


    pylab.show()


