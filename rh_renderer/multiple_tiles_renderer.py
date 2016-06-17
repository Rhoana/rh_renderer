from single_tile_renderer import AlphaTileRenderer
import numpy as np
from pyrtree import RTree,Rect


class MultipleTilesRenderer:
    BLEND_TYPE = {
            "NO_BLENDING" : 0,
            "AVERAGING" : 1,
            "LINEAR" : 2
        }
    def __init__(self, single_tiles, blend_type="NO_BLENDING"):
        """Receives a number of image paths, and for each a transformation matrix"""
        self.blend_type = self.BLEND_TYPE[blend_type]
        self.single_tiles = single_tiles
        # Create an RTree of the bounding boxes of the tiles
        self.rtree = RTree()
        for t in self.single_tiles:
            bbox = t.get_bbox()
            # pyrtree uses the (x_min, y_min, x_max, y_max) notation
            self.rtree.insert(t, Rect(bbox[0], bbox[2], bbox[1], bbox[3]))
        #should_compute_mask = False if self.blend_type == 0 else True
        #for i, matrix in enumerate(transform_matrices):
        #    self.single_tiles[i].add_transformation(matrix)

    def add_transformation(self, model):
        """Adds a transformation to all tiles"""
        self.rtree = RTree()
        for single_tile in self.single_tiles:
            single_tile.add_transformation(model)
            bbox = single_tile.get_bbox()
            # pyrtree uses the (x_min, y_min, x_max, y_max) notation
            self.rtree.insert(single_tile, Rect(bbox[0], bbox[2], bbox[1], bbox[3]))
 
        
    def render(self):
        if len(self.single_tiles) == 0:
            return None, None

        # Render all tiles by finding the bounding box, and using crop
        all_bboxes = np.array([t.get_bbox() for t in self.single_tiles]).T
        bbox = [np.min(all_bboxes[0]), np.max(all_bboxes[1]), np.min(all_bboxes[2]), np.max(all_bboxes[3])]
        crop, start_point = self.crop(bbox[0], bbox[2], bbox[1], bbox[3])
        return crop, start_point

    def crop(self, from_x, from_y, to_x, to_y):
        if len(self.single_tiles) == 0:
            return None, None

        # Distinguish between the different types of blending
        if self.blend_type == 0: # No blending
            res = np.zeros((round(to_y + 1 - from_y), round(to_x + 1 - from_x)), dtype=np.uint8)
            # render only relevant parts, and stitch them together
            # filter only relevant tiles using rtree
            rect_res = self.rtree.query_rect( Rect(from_x, from_y, to_x, to_y) )
            for rtree_node in rect_res:
                if not rtree_node.is_leaf():
                    continue
                t = rtree_node.leaf_obj()
                t_img, t_start_point, _ = t.crop(from_x, from_y, to_x, to_y)
                if t_img is not None:
                    res[t_start_point[1] - from_y: t_img.shape[0] + (t_start_point[1] - from_y),
                        t_start_point[0] - from_x: t_img.shape[1] + (t_start_point[0] - from_x)] = t_img

        elif self.blend_type == 1: # Averaging
            # Do the calculation on a uint16 image (for overlapping areas), and convert to uint8 at the end
            res = np.zeros(
                (round(to_y + 1 - from_y), round(to_x + 1 - from_x)), 
                np.float32)
            res_mask = np.zeros(
                (round(to_y + 1 - from_y), round(to_x + 1 - from_x)),
                np.float32)

            # render only relevant parts, and stitch them together
            # filter only relevant tiles using rtree
            rect_res = self.rtree.query_rect( Rect(from_x, from_y, to_x, to_y) )
            for rtree_node in rect_res:
                if not rtree_node.is_leaf():
                    continue
                t = rtree_node.leaf_obj()
                t_img, t_start_point, t_mask = t.crop(from_x, from_y, to_x, to_y)
                if t_img is not None:
                    t_mask, _, _ = AlphaTileRenderer(t).crop(
                        from_x, from_y, to_x, to_y)
                    res[t_start_point[1] - from_y: t_img.shape[0] + (t_start_point[1] - from_y),
                        t_start_point[0] - from_x: t_img.shape[1] + (t_start_point[0] - from_x)] += t_img
                    res_mask[t_start_point[1] - from_y: t_img.shape[0] + (t_start_point[1] - from_y),
                             t_start_point[0] - from_x: t_img.shape[1] + (t_start_point[0] - from_x)] += t_mask

            # Change the values of 0 in the mask to 1, to avoid division by 0
            res_mask[res_mask == 0] = 1
            res = res / res_mask
            res = np.maximum(0, np.minimum(255, res)).astype(np.uint8)

        elif self.blend_type == 2: # Linear averaging
            # Do the calculation on a uint32 image (for overlapping areas), and convert to uint8 at the end
            # For each pixel use the min-distance to an edge as a weight, and store the
            # average the outcome according to the weight
            res = np.zeros((round(to_y + 1 - from_y), round(to_x + 1 - from_x)), dtype=np.uint32)
            res_weights = np.zeros((round(to_y + 1 - from_y), round(to_x + 1 - from_x)), dtype=np.uint16)

            # render only relevant parts, and stitch them together
            # filter only relevant tiles using rtree
            rect_res = self.rtree.query_rect( Rect(from_x, from_y, to_x, to_y) )
            for rtree_node in rect_res:
                if not rtree_node.is_leaf():
                    continue
                t = rtree_node.leaf_obj()
                t_img, t_start_point, t_weights = t.crop_with_distances(from_x, from_y, to_x, to_y)
                if t_img is not None:
                    print "actual image start_point:", t_start_point, "and shape:", t_img.shape
                    res[t_start_point[1] - from_y: t_img.shape[0] + (t_start_point[1] - from_y),
                        t_start_point[0] - from_x: t_img.shape[1] + (t_start_point[0] - from_x)] += t_img * t_weights
                    res_weights[t_start_point[1] - from_y: t_img.shape[0] + (t_start_point[1] - from_y),
                                t_start_point[0] - from_x: t_img.shape[1] + (t_start_point[0] - from_x)] += t_weights

            # Change the weights that are 0 to 1, to avoid division by 0
            res_weights[res_weights < 1] = 1
            res = res / res_weights
            res = np.maximum(0, np.minimum(255, res)).astype(np.uint8)

        return res, (from_x, from_y)

