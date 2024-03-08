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
  
class TrafficTrackerYoloV3:
    def __init__(self, confidence=0.5):
        self.loader = ImagePipeline()
        self.threshold=confidence
        dir = os.path.dirname(__file__)
        weights_path = os.path.join(dir, "resources/yolov3.weights")
        cfg_path = os.path.join(dir, "resources/yolov3.cfg")
        names_path = os.path.join(dir, "resources/coco.names")
        self.model = cv2.dnn.readNet(model=weights_path, config=cfg_path)
        with open(names_path, "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
        layer_names = self.model.getLayerNames()
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))
        self.output_layers = [layer_names[i - 1] for i in self.model.getUnconnectedOutLayers()]

    def get_count(self):
        img = self.loader.get_data_as_user()
        img = np.array(img)
        img = cv2.resize(img, None, fx=0.4, fy=0.4)
        h, w, c = img.shape
        blob = cv2.dnn.blobFromImage(img, scalefactor=0.00392, 
                                     size=(320, 320), mean=(0, 0, 0), 
                                     swapRB=True, crop=False)
        self.model.setInput(blob)
        out = self.model.forward(self.output_layers)
        bev_bounds = []
        confs = []
        ids = []
        for output in out:
            for det in output:
                scores = det[5:]
                id_curr = np.argmax(scores)
                conf = scores[id_curr]
                if conf >= self.threshold:
                    cx, cy, width, height = [int(a*b) for a, b in zip(det[0 : 4], [w, h, w, h])]
                    x, y = int(cx - (width/2)), int(cy - (height/2))
                    ids.append(id_curr)
                    confs.append(conf)
                    bev_bounds.append([x, y, width, height])
        indices = cv2.dnn.NMSBoxes(bev_bounds, confs, self.threshold, 0.5)
        if indices == ():
            return 0, None
        indices = indices.flatten()
        count = 0
        for i in indices:
            (x, y, w, h) = bev_bounds[i][0], bev_bounds[i][1], bev_bounds[i][2], bev_bounds[i][3]
            color = self.colors[i]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            text = f"{ids[i]}: {confs[i] * 100:.2f}%"
            cv2.putText(img, text, (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
            if ids[i] in [2, 3, 5, 6, 7]:
                count += 1
        return count, Image.fromarray(img)
