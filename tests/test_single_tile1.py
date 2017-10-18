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
    #transform_45 = np.array([[math.cos(math.pi/4), -math.sin(math.pi/4), 10.0], [math.sin(math.pi/4), math.cos(math.pi/4), 15.0], [0., 0., 1.]])

    transforms = [transform_45] * 4
    for t in transforms:
        print("Adding transformation:", t)
        renderer.add_transformation(t)
        img, start_point = renderer.render()

        print("Start point is at:", start_point, "image shape:", img.shape)
        pylab.figure()
        pylab.imshow(img, cmap='gray', vmin=0., vmax=255.)

    
#    renderer2 = SingleTileAffineRenderer('images/tile1.bmp', 3348, 2976, compute_mask=True)
#    transform_identity = np.array([[1.0, -0.0, 1000.0], [0, 1.0, 1500.0]])
#    renderer2.add_transformation(transform_identity)
#    img, start_point = renderer2.render()
#    print("After a single identitytransformation: Start point is at:", start_point, "image shape:", img.shape)
#    pylab.figure()
#    pylab.imshow(img, cmap='gray')

#    renderer3 = SingleTileAffineRenderer('images/tile1.bmp', 3348, 2976, compute_mask=True)
#    transform_180 = np.array([[math.cos(math.pi), -math.sin(math.pi), 1000.0], [math.sin(math.pi), math.cos(math.pi), 1500.0]])
#    renderer3.add_transformation(transform_180)
#    img, start_point = renderer3.render()
#    print("After single 180 transformation: Start point is at:", start_point, "image shape:", img.shape)
#    pylab.figure()
#    pylab.imshow(img, cmap='gray')


    renderer4 = SingleTileAffineRenderer('images/tile1.bmp', 3348, 2976, compute_mask=True)
    transform_90 = np.array([[math.cos(math.pi/2), -math.sin(math.pi/2), 10.0], [math.sin(math.pi/2), math.cos(math.pi/2), 15.0]])
    #transform_90 = np.array([[math.cos(math.pi/2), -math.sin(math.pi/2), 10.0], [math.sin(math.pi/2), math.cos(math.pi/2), 15.0], [0., 0., 1.]])
    transforms = [transform_90] * 2
    for t in transforms:
        print("Adding transformation:", t)
        renderer4.add_transformation(t)
        img, start_point = renderer4.render()

        print("Start point is at:", start_point, "image shape:", img.shape)
        pylab.figure()
        pylab.imshow(img, cmap='gray')


    pylab.show()


