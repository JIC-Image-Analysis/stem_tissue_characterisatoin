from jicbioimage.illustrate import Canvas


def get_normalised_rgb(cell_intensity, imin, imax):
    norm_area = ((cell_intensity - imin) / float(imax - imin)) * 255
    norm_area = int(round(norm_area))
    assert norm_area >= 0
    assert norm_area < 256
    return (255 - norm_area, 255 - norm_area, 255)


def generate_annotation(segmentation):
    areas = [segmentation.region_by_identifier(i).area
             for i in segmentation.identifiers]
    imin = min(areas)
    imax = max(areas)
    ydim, xdim = segmentation.shape
    canvas = Canvas.blank_canvas(width=xdim, height=ydim)
    for i in segmentation.identifiers:
        region = segmentation.region_by_identifier(i)
        area = region.area
        color = get_normalised_rgb(area, imin, imax)
        canvas.mask_region(region.inner.inner, color)

    return canvas
