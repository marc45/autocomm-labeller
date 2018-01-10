from objects.json_serializable import JSer
from objects.image import Image


class Video(JSer):
    def __init__(self, fps: float=1, vidpath: str='', json_dict: dict=None):
        """
        :param fps: [optional] <float>, the number of images per second
        :param vidpath: [optional] <str>, path to the video
        :param json_dict: [optional] <dict>, json dictionary to load from
        """
        assert bool(vidpath) ^ bool(json_dict)
        if not json_dict:
            self.fps = fps
            self.vidpath = vidpath
            self.json_dict = None
            self.images = self.load_images()
        else:
            self.deserialized(json_dict)


    def serialized(self) -> dict:
        video_dict = {
            'fps': self.fps,
            'vidpath': self.vidpath,
            'images': [image.serialized() for image in self.images]
        }
        return video_dict

    def deserialized(self, json_dict: dict) -> object:
        self.fps = json_dict['fps']
        self.vidpath = json_dict['vidpath']
        self.json_dict = None
        self.images = [Image(video_dict) for video_dict in json_dict['images']]
        return self

    def load_images(self) -> list:
        """
        Returns a list of the images that make up the video
        """
        pass

    def get_image(self, ind: int) -> Image:
        """
        Returns the image in the video that corresponds to the index in the images list
        :param ind: <int>, the index of the image that is taken from the images list
        """
        return self.images[ind]

    def get_fps(self) -> float:
        """
        Returns the video's images per second
        """
        return self.fps

    def set_fps(self, fps: float) -> None:
        """
        Sets the video's images per second to be fps
        :param fps: <float>, the value for the images per second
        """
        self.fps = fps
