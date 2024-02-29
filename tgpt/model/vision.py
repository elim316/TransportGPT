from ..data import ImagePipeline
import cv2, os
import numpy as np
from PIL import Image

class TrafficTracker:
    def __init__(self):
        self.loader = ImagePipeline()
        dir = os.path.dirname(__file__)
        xml_path = os.path.join(dir, "resources/car-cascade.xml")
        self.model = cv2.CascadeClassifier(xml_path)

    def get_count(self):
        img = self.loader.get_data_as_user()
        img = np.array(img.resize((450, 250)))
        grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(grey_img,(5,5),0)
        dilated = cv2.dilate(blur,np.ones((3,3)))
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
        closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel) 
        cars = self.model.detectMultiScale(closing, 1.1, 1)
        ret = 0
        for x, y, w, h in cars:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            ret += 1
        return ret, Image.fromarray(img)