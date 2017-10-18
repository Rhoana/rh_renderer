# executes some functions from the points transform model
from __future__ import print_function
from rh_renderer.models import PointsTransformModel
import numpy as np

def test_to_modelspec():
    # Create all source points in a 5x5 grid
    src_points = np.array(np.meshgrid(np.arange(5), np.arange(5))).T.reshape(-1,2)
    # Create all dest points in a 5x5 grid that starts at 10
    dest_points = np.array(np.meshgrid(np.arange(5), np.arange(5))).T.reshape(-1,2) + 10
    model1 = PointsTransformModel((src_points, dest_points))
    tilespec = model1.to_modelspec()
    assert(tilespec['className'] == 'mpicbg.trakem2.transform.PointsTransformModel')
    expected_data = []
    for p1, p2 in zip(src_points, dest_points):
        expected_data.append('{} {} {} {} 1.0'.format(float(p1[0]), float(p1[1]), float(p2[0]), float(p2[1])))
    assert(tilespec['dataString'] == ' '.join(expected_data))
    #print tilespec['dataString']
    return True
    

if __name__ == '__main__':
    print("test_to_modelspec:", test_to_modelspec())


