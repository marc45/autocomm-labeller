import json
import os
import random
import hashlib

"""
JSON Structure:
{
  "source": "",
  "boxes": [{"class": "", 
              "topLeft": [0, 0], 
              "bottomRight": [0, 0]}],
  "lanes": [{"class": "",
              "upper": [0, 0], 
              "lower": [0, 0]}]
}
"""

class AppState:
    def __init__(self):
        self.active_class = ''
        self.source_dir = ''
        self.images = ''
        self.classes = []
        self.classbar, self.toolbar, self.display = None, None, None
        self.boxes = []
        self.lanes = []
        self.load_state()

    def add_box(self, c, top_left, bottom_right):
        self.boxes.append({'class': c, 'topLeft': top_left, 'bottom_right': bottom_right})

    def add_lane(self, c, upper, lower):
        upper, lower = (upper, lower) if upper[1] >= lower[1] else (lower, upper)
        self.lanes.append({'class': c, 'upper': upper, 'lower': lower})

    def write_state(self):
        print(type(self.classes), type(self.source_dir))
        with open('./config.json', 'w') as f:
            json.dump({'classes': self.classes, 'sourceDir': self.source_dir}, f)

    def load_state(self):
        if os.path.exists('./config.json'):
            with open('./config.json', 'r') as f:
                json_dict = json.load(f)
                self.classes = json_dict['classes']
                self.source_dir = json_dict['sourceDir']

    def write_labels(self, source_name: str):
        hash = hashlib.sha256(source_name + str(random.randint(2e16))).hexdigest()
        json_dict = {
            'source': '../' + source_name,
            'boxes': self.boxes,
            'lanes': self.lanes,
        }
        label_dir_path = os.path.join(self.source_dir, '..', 'labels')
        if not os.path.exists(label_dir_path):
            os.makedirs(label_dir_path)
        with open(os.path.join(self.source_dir, '..', 'labels', hash + '.json'), 'w') as f:
            json.dump(f, json_dict)
