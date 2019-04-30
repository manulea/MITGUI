#from IPython.html.widgets import interact, ButtonWidget
from IPython.display import display, clear_output

import ipywidgets as widgets

from sklearn import datasets
faces = datasets.fetch_olivetti_faces()


import numpy as np
import matplotlib.pyplot as plt

class Trainer:
    def __init__(self):
        self.results = {}
        self.imgs = faces.images
        self.index = 0
        
    def increment_face(self):
        if self.index + 1 >= len(self.imgs):
            return self.index
        else:
            while str(self.index) in self.results:
                print(self.index)
                self.index += 1
            return self.index
    
    def record_result(self, smile=True):
        self.results[str(self.index)] = smile
        
        
trainer = Trainer()

button_smile = widgets.Button(description='smile')
button_no_smile = widgets.Button(description='sad face')

display(button_smile)
display(button_no_smile)


def display_face(face):
    clear_output()
    plt.imshow(face, cmap='gray')
    plt.axis('off')

def update_smile(b):
    trainer.record_result(smile=True)
    trainer.increment_face()
    display_face(trainer.imgs[trainer.index])

def update_no_smile(b):
    trainer.record_result(smile=False)
    trainer.increment_face()
    display_face(trainer.imgs[trainer.index])


button_no_smile.on_click(update_no_smile)
button_smile.on_click(update_smile)


display_face(trainer.imgs[trainer.index])