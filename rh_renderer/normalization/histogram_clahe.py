import numpy as np
import skimage.exposure


class HistogramCLAHE(object):

    def __init__(self):
        pass

    def adjust_histogram(self, img_path, img):
        img1_equ = ((skimage.exposure.equalize_adapthist(img)) * 255).astype(np.uint8)
        return img1_equ



