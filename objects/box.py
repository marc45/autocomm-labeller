from objects.json_serializable import JSer


class Box(JSer):
    """
    Specifies boxes in images and their corresponding labels
    """
    def __init__(self, label: str='', top_left: tuple=(0,0), size: tuple=(0,0), json_dict=None):
        """
        :param label: <str>, label of box
        :param top_left: <tuple<float, float>>, coordinates of top-left point in (x, y) notation
        :param size: <tuple<float, float>>, size of box in <width, height> notation
        """
        if not json_dict:
            assert len(top_left) == 2 and len(size) == 2, 'Make sure <top_left> and <size> both have 2 dimensions.'
            assert 0 <= top_left[0] <= 1 and 0 <= top_left[1] <= 1, \
                'Please express coordinates in ratio form as (x in pix / width in pix, y in pix / height in pix).'
            assert size[0] >= 0 and size[0] >= 0, \
                'Size must be positive.'
            assert 0 <= top_left[0] + size[0] <= 1 and 0 <= top_left[1] + size[1] <= 1, \
                'Please express coordinates in ratio form as (x in pix / width in pix, y in pix / height in pix).'

            self.label = label
            self.top_left = top_left
            self.size = size
        else:
            self.deserialized(json_dict)

    def serialized(self) -> dict:
        box_dict = {
            'label': self.label,
            'top_left': self.top_left,
            'size': self.size
        }
        return box_dict

    def deserialized(self, json_dict: dict) -> object:
        self.label = json_dict['label']
        self.top_left = json_dict['top_left']
        self.size = json_dict['size']
        return self

    def get_area(self) -> float:
        """Get area of box as a ratio."""
        return self.size[0] * self.size[1]

    def intersects(self, point: tuple) -> bool:
        """
        Determines if the point is inside the box
        :param point: <tuple<float, float>>, a coordinate in (x, y) notation
        """
        assert 0 <= point[0] <= 1 and 0 <= point[1] <= 1, \
            'Please express coordinates in ratio form as (x in pix / width in pix, y in pix / height in pix).'
        return (self.top_left[0] <= point[0] <= self.top_left[0] + self.size[0]) and (self.top_left[1] <= point[1] <= self.top_left[1] + self.size[1])

    def set_label(self, label: str) -> None:
        """
        Sets the box's label to be the label parameter
        :param label: <str>, a label for the box
        """
        self.label = label
