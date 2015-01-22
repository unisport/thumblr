from PIL import Image
from thumblr.image_processing.basic_operations import ImagePos
from thumblr.tests.mocks import mock_for_tests


@mock_for_tests
def crop_image(image, left_up=ImagePos(x=0, y=0), right_down=ImagePos(x=0, y=0)):
    assert isinstance(image, Image.Image)

    return image.crop((left_up.x, left_up.y, right_down.x, right_down.y))
