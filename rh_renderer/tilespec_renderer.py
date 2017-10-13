# Allows rendering a given tilespec
from multiple_tiles_renderer import MultipleTilesRenderer
from single_tile_renderer import SingleTileRenderer
import json
import numpy as np
import models


class TilespecRenderer:

    def __init__(self, tilespec, hist_adjuster=None):
#         self.single_tiles = [SingleTileRenderer(
#                                 tile_ts["mipmapLevels"]["0"]["imageUrl"].replace("file://", ""), tile_ts["width"], tile_ts["height"], compute_distances=True, hist_adjuster=hist_adjuster)
#                             for tile_ts in tilespec]
        self.single_tiles = [SingleTileRenderer(
                                tile_ts["mipmapLevels"]["0"]["imageUrl"].replace("file://", ""), tile_ts["width"], tile_ts["height"], compute_mask=True, compute_distances=False, hist_adjuster=hist_adjuster)
                            for tile_ts in tilespec]
#         self.single_tiles = [SingleTileRenderer(
#                                 tile_ts["mipmapLevels"]["0"]["imageUrl"].replace("file://", ""), tile_ts["width"], tile_ts["height"], compute_mask=True, compute_distances=False, hist_adjuster=hist_adjuster)
#                             for tile_ts in tilespec]
        # Add the corresponding transformation
        for tile_ts, tile in zip(tilespec, self.single_tiles):
            for t in tile_ts["transforms"]:
                model = models.Transforms.from_tilespec(t)
                tile.add_transformation(model)

        #self.multi_renderer = MultipleTilesRenderer(self.single_tiles, blend_type="LINEAR")
        self.multi_renderer = MultipleTilesRenderer(self.single_tiles, blend_type="MULTI_BAND_SEAM")
        #self.multi_renderer = MultipleTilesRenderer(self.single_tiles, blend_type="AVERAGING")
        

    def render(self):
        return self.multi_renderer.render()

    def crop(self, from_x, from_y, to_x, to_y):
        return self.multi_renderer.crop(from_x, from_y, to_x, to_y)

    def add_transformation(self, model):
        """Adds a transformation to all tiles"""
        self.multi_renderer.add_transformation(model)

