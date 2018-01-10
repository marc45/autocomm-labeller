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
        filtered_boxes = filter(lambda box: box.intersects(point), self.boxes)
        pass

    def add_box(self, box: Box) -> None:
        pass

    def remove_box(self, box: Box=None, point: tuple=None) -> None:
        assert bool(box) ^ bool(point), 'Please provide exactly one of <box> or <point>.'
        pass

    def set_active_box(self, box: Box=None, point: tuple=None) -> None:
        assert bool(box) ^ bool(point), 'Please provide exactly one of <box> or <point>.'
        pass

    def get_active_box(self) -> Box:
        return self.active_box

    def render(self, size: tuple) -> QPixmap:
        """

        :param size: <tuple<int, int>>, size of image formatted as (x, y) in pixels
        :return: QPixmap of image render
        """
        pass
