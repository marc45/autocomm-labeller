import json
import hashlib
from PyQt5.QtGui import QImage, QPixmap
from objects.json_serializable import JSer
from objects.box import Box


class Image(JSer):
    def __init__(self, imgpath: str='', jsonpath: str='', json_dict: dict=None):
        """
        :param img_path: [optional] <str>, path to original img
        :param json_path: [optional] <str>, path to json annotations
        :param json_dict: [optional] <dict>, json dictionary to load from
        """
        if not json_dict:
            assert bool(imgpath) ^ bool(jsonpath), 'Specify exactly one of <img_path> or <json_path>'
            self.q_image = None
            self.imgpath = imgpath
            self.jsonpath = jsonpath
            self.boxes = []
            self.active_box = None

            if imgpath:
                pass
            else:
                self.deserialize(jsonpath)
        else:
            self.deserialized(json_dict)

    def serialized(self) -> dict:
        image_dict = {
            'boxes': [box.serialized() for box in self.boxes],
            'imgpath': self.imgpath
        }
        return image_dict

    def deserialized(self, json_dict: dict) -> object:
        self.boxes = [Box(box_dict) for box_dict in json_dict['boxes']]
        self.imgpath = json_dict['imgpath']
        return self

    def get_box(self, point: tuple=None) -> Box:
        """
        Returns the smallest box among all the boxes that contain the point
        :param point: [optional] <tuple<float, float>>, a coordinate in (x, y) notation
        """
        if tuple:
            filtered_boxes = filter(lambda box: box.intersects(point), self.boxes)
            if filtered_boxes:
                sorted_boxes = sorted(filtered_boxes, key=lambda box: box.get_area())
                return sorted_boxes[0]
            else:
                return None
        else:
            return None

    def add_box(self, box: Box) -> None:
        """
        Adds a box to the image
        :param box: <Box>, the box that is added to the image
        """
        self.boxes.append(box)

    def remove_box(self, box: Box=None, point: tuple=None) -> None:
        """
        Removes a box from the image, or removes the smallest box that contains the point
        :param box: [optional] <Box>, the box that is removed from the image
        :param point: [optional] <tuple<float, float>>, the point where the smallest box that contains it is removed
        """
        assert bool(box) ^ bool(point), 'Please provide exactly one of <box> or <point>.'
        if box:
            self.boxes.remove(box)
        else:
            self.boxes.remove(self.get_box(point))

    def set_active_box(self, box: Box=None, point: tuple=None) -> None:
        """
        Sets the image's active box to be the box parameter or the smallest box that contains the point
        :param box: the box that is set as the image's active box
        :param point: the point where the smallest box that contains it will be set as the image's active box
        """
        assert bool(box) ^ bool(point), 'Please provide exactly one of <box> or <point>.'
        if box:
            self.active_box = box
        else:
            self.active_box = self.get_box(point)

    def get_active_box(self) -> Box:
        """
        Returns the image's active box
        """
        return self.active_box

    def render(self, size: tuple) -> QPixmap:
        """

        :param size: <tuple<int, int>>, size of image formatted as (x, y) in pixels
        :return: QPixmap of image render
        """
        pass
