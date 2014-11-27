"""
Each (new) function in this file dream to be side-effect-free:
 - does not change any of argument
 - copy image if it needed to be changed and then return copy
"""

from collections import namedtuple
import math
from PIL import Image


ImageDim = namedtuple('ImageDim', ['width', 'height'])
ImagePos = namedtuple('ImagePos', ['x', 'y'])


def squarify(original_img, result_size=ImageDim(width=1000, height=1000)):
    assert isinstance(original_img, Image.Image)

    image = original_img.copy()
    width, height = original_img.size

    if height != width:
        width_original, height_original = width, height

        # Adjust width and height, find the starting x and y coords
        if height > width:
            width = height
            height = height
            pos_x = int(math.floor(
                (math.floor(width) / 2) -
                (math.floor(width_original) / 2)
            ))
            pos_y = int(0)
        else:
            width = width
            height = width
            pos_x = int(0)
            pos_y = int(math.floor(
                (math.floor(height) / 2) -
                (math.floor(height_original) / 2)
            ))

        # Create a square image and paste our image on it
        square_image = Image.new('RGB', (width, height), 'White')
        square_image.paste(image, (pos_x, pos_y))

    else:
        square_image = image

    if width > result_size.width or height > result_size.height:
        square_image.thumbnail(result_size, Image.ANTIALIAS)

    return square_image


def overlay(original_img, overlay_img, position=ImagePos(x=0, y=0)):
    assert isinstance(original_img, Image.Image)

    res_image = original_img.copy()
    res_image.paste(overlay_img, position)

    return res_image


def thumbnail(original_img, thumbnail_size=ImageDim(width=100, height=100)):
    assert isinstance(original_img, Image.Image)

    res_image = original_img.copy()
    res_image.thumbnail(thumbnail_size, Image.ANTIALIAS)

    return res_image

