import numpy as np

import skimage.filters
import skimage.morphology

from jicbioimage.core.io import AutoWrite
from jicbioimage.core.transform import transformation
from jicbioimage.transform import (
    invert,
    threshold_otsu,
    find_edges_sobel,
    dilate_binary,
    erode_binary,
    remove_small_objects,
)
from jicbioimage.segment import connected_components, watershed_with_seeds


@transformation
def threshold_adaptive_median(image, block_size):
    return skimage.filters.threshold_adaptive(image, block_size=block_size)


@transformation
def clip_mask(image, mask):
    image[np.where(mask == 0)] = 0
    return image


@transformation
def fill_holes(image, size):
    org_autowrite = AutoWrite.on
    AutoWrite.on = False
    image = invert(image)
    image = remove_small_objects(image, size)
    image = invert(image)
    AutoWrite.on = org_autowrite
    return image


def generate_cross_section_mask(image):
    image = find_edges_sobel(image)
    image = threshold_otsu(image)
    image = dilate_binary(image, selem=skimage.morphology.disk(5))
    image = remove_small_objects(image, 5000)
    image = fill_holes(image, 50000)
    image = erode_binary(image, selem=skimage.morphology.disk(10))
    image = remove_small_objects(image, 50000)
    return image


def segment(image):
    cross_section_mask = generate_cross_section_mask(image)

    seeds = threshold_adaptive_median(image, 51)
    seeds = clip_mask(seeds, cross_section_mask)
    seeds = fill_holes(seeds, 10000)
    seeds = erode_binary(seeds)
    seeds = remove_small_objects(seeds, 10)
    seeds = connected_components(
        seeds,
        connectivity=1,
        background=0
    )

    cells = watershed_with_seeds(
        image,
        seeds=seeds,
        mask=cross_section_mask
    )
    return cells
