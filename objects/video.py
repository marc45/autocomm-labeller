from objects.json_serializable import JSer
from objects.image import Image


class Video(JSer):
    def __init__(self, images: list=None, json_dict: dict=None):
        """
        :param images: [optional] <list<Image>>, a list of images that make up the video
        :param json_dict: [optional] <dict>, json dictionary to load from
        """
        assert not (images and json_dict), 'Do not give both <images> and <json_dict>'
        self.images = images
        self.json_dict = json_dict
    def serialized(self):
        video_dict = {
            'images': [image.serialized() for image in self.images]
        }
        return video_dict
    def deserialized(self, json_dict: dict):
        self.images =
