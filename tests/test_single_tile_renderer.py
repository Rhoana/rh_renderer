from __future__ import print_function
import numpy as np
import unittest
from rh_renderer.single_tile_renderer import SingleTileDynamicRendererBase
from rh_renderer.models import TranslationModel, AffineModel


class STR(SingleTileDynamicRendererBase):
    
    def __init__(self, img, compute_mask=False, 
                compute_distances=True):
        super(STR, self).__init__(
            img.shape[1], img.shape[0], compute_mask=compute_mask, compute_distances=compute_distances)
        self.__img = img
    
    def load(self):
        return self.__img


class TestSingleTileRenderer(unittest.TestCase):
    def test_01_01_render(self):
        r = np.random.RandomState(1234)
        img = r.uniform(high=255, size=(35, 42)).astype(np.uint8)
        renderer = STR(img, False, False)
        img_out, start = renderer.render()
        np.testing.assert_array_equal(img, img_out)
        np.testing.assert_array_equal(start, (0, 0))
    
    def test_01_02_translation(self):
        r = np.random.RandomState(456)
        img = r.uniform(high=255, size=(35, 42)).astype(np.uint8)
        renderer = STR(img, False, False)
        t = TranslationModel(np.array([14, 25]))
        renderer.add_transformation(t)
        img_out, start = renderer.render()
        np.testing.assert_array_equal(img, img_out)
        np.testing.assert_array_equal(start, (14, 25))

    def test_01_03_affine(self):
        r = np.random.RandomState(325)
        img = r.uniform(high=255, size=(35, 42)).astype(np.uint8)
        renderer = STR(img, False, False)
        a = AffineModel(m=np.array([[0, 1, 0],
                                    [1, 0, 0],
                                    [0, 0, 1]]))
        renderer.add_transformation(a)
        img_out, start = renderer.render()
        self.assertSequenceEqual(img_out.shape, (42, 35))
        np.testing.assert_array_almost_equal(img, img_out.transpose())

    def test_02_01_bbox(self):
        r = np.random.RandomState(456)
        img = r.uniform(high=255, size=(35, 42)).astype(np.uint8)
        for transform, bbox in (
            (TranslationModel(np.array([14, 25])), [14, 55, 25, 59]),
            (AffineModel(np.array([[0, 1, 0],
                                   [1, 0, 0],
                                   [0, 0, 1]])), [0, 34, 0, 41])):
            renderer = STR(img, False, False)
            renderer.add_transformation(transform)
            self.assertSequenceEqual(renderer.bbox, bbox)
    
    def test_03_01_mask(self):
        r = np.random.RandomState(231)
        img = np.zeros((20, 20), np.uint8)
        renderer = STR(img, True, False)
        renderer.add_transformation(AffineModel(
            np.array([[np.cos(np.pi/4), -np.sin(np.pi/4), 0],
                      [np.sin(np.pi/4), np.cos(np.pi/4), 0],
                      [0, 0, 1]])))
        renderer.render()
        mask, start = renderer.fetch_mask()
        self.assertEqual(mask[0, 0], 0)
        self.assertEqual(mask[-1, -1], 0)
        self.assertTrue(np.all(mask[int(mask.shape[0]/2)] == 1))
        self.assertTrue(np.all(mask[:, int(mask.shape[1]/2)] == 1))
    
    def test_04_01_crop(self):
        r = np.random.RandomState(12345)
        img = r.uniform(high=255, size=(35, 42)).astype(np.uint8)
        renderer = STR(img, False, False)
        img_out, start, mask = renderer.crop(1, 2, 10, 15)
        np.testing.assert_array_equal(img[2:16, 1:11], img_out)
        self.assertSequenceEqual(start, [1, 2])
    
    def test_04_02_crop_with_transform(self):
        r = np.random.RandomState(12345)
        img = r.uniform(high=255, size=(35, 42)).astype(np.uint8)
        renderer = STR(img, False, False)
        a = AffineModel(np.array([[0, 1, 0],
                                  [1, 0, 0],
                                  [0, 0, 1]]))
        renderer.add_transformation(a)
        img_out, start, mask = renderer.crop(5, 10, 20, 30)
        np.testing.assert_array_equal(img_out, img.transpose()[10:31, 5:21])

    def test_05_01_crop_with_distances(self):
        r = np.random.RandomState(12345)
        img = r.uniform(high=255, size=(35, 42)).astype(np.uint8)
        renderer = STR(img, False, True)
        img_out, (x, y), cropped_distances = renderer.crop_with_distances(
            0, 0, 42, 35)
        np.testing.assert_array_equal(img, img_out)
        self.assertEqual(cropped_distances[0, 5], .5)
        self.assertEqual(cropped_distances[5, 10], 5.5)
        
    def test_05_02_crop_with_distances_affine(self):
        r = np.random.RandomState(12345)
        img = r.uniform(high=255, size=(42, 42)).astype(np.uint8)
        renderer = STR(img, False, True)
        renderer.add_transformation(AffineModel(
            np.array([[np.cos(np.pi/4), -np.sin(np.pi/4), 0],
                      [np.sin(np.pi/4), np.cos(np.pi/4), 0],
                      [0, 0, 1]])))
        d = int(42 * np.sqrt(2) + 1)
        img_out, (x, y), cropped_distances = renderer.crop_with_distances(
            -d, 0, d, d)
        self.assertEqual(cropped_distances[1, 1], 0)
        self.assertEqual(cropped_distances[-2, -2], 0)
        self.assertGreater(
            cropped_distances[1, int(cropped_distances.shape[1]/2)], .5)
        self.assertLessEqual(
            cropped_distances[1, int(cropped_distances.shape[1]/2)], 1.5)
        

if __name__ == "__main__":
    unittest.main()
