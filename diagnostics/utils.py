# diagnostics/utils.py
from PIL import Image
import numpy as np

img_height = 150
img_width = 150

def preprocess_image(image_file):
    image = Image.open(image_file).convert('RGB')
    image = image.resize((img_width, img_height))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image
