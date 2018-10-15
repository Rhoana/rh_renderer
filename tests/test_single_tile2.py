from __future__ import print_function
import pylab
from rh_renderer.single_tile_affine_renderer import SingleTileAffineRenderer
import math
import numpy as np

if __name__ == '__main__':
    renderer = SingleTileAffineRenderer('images/tile1.bmp', 3348, 2976, compute_mask=True)

    img, start_point = renderer.render()
    print("Before transformations: Start point is at:", start_point, "image shape:", img.shape)
    pylab.figure()
    pylab.imshow(img, cmap='gray', vmin=0., vmax=255.)

    #transform_45 = np.array([[math.cos(math.pi/4), -math.sin(math.pi/4), 1000.0], [math.sin(math.pi/4), math.cos(math.pi/4), 1500.0]])
    transform_45 = np.array([[math.cos(math.pi/4), -math.sin(math.pi/4), 10.0], [math.sin(math.pi/4), math.cos(math.pi/4), 15.0]])

    transforms = [transform_45] * 4
    for t in transforms:
        print("Adding transformation:", t)
        renderer.add_transformation(t)
        img, start_point = renderer.render()

        print("Start point is at:", start_point, "image shape:", img.shape)
        pylab.figure()
        pylab.imshow(img, cmap='gray', vmin=0., vmax=255.)

        bbox = renderer.get_bbox()
        from_x = (bbox[0] + bbox[1]) / 2.0 - 500
        to_x = from_x + 1000
        from_y = (bbox[2] + bbox[3]) / 2.0 - 500
        to_y = from_y + 1000
        cropped_img, start_point, _ = renderer.crop(from_x, from_y, to_x, to_y)
        print("cropped Start point is at:", start_point, "image shape:", cropped_img.shape)
        pylab.figure()
        pylab.imshow(cropped_img, cmap='gray', vmin=0., vmax=255.)
        

    

    pylab.show()


