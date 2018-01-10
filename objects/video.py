from objects.json_serializable import JSer
from objects.image import Image


class Video(JSer):
    def __init__(self, vidpath: str='', json_dict: dict=None):
        """
        :param vidpath: [optional] <str>, path to the video
        :param json_dict: [optional] <dict>, json dictionary to load from
        """
        assert bool(vidpath) ^ bool(json_dict)
        if not json_dict:
            self.images = load_images
            self.json_dict = None
        else:
            self.deserialized(json_dict)


    def serialized(self) -> dict:
        video_dict = {
            'images': [image.serialized() for image in self.images]
        }
        return video_dict

    def deserialized(self, json_dict: dict) -> object:
        self.images = [Image(video_dict) for video_dict in json_dict['images']]
        return self

    def load_images(self) -> list:
        """
        Returns a list of the images that make up the video
        """
