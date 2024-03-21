from image import ImagePipeline
from EstTravelTimes import EstTimePipeline
from trafficFlow import TrafficFlowPipeline
from ..model import TrafficTrackerYoloV3

class Retrieval:
    def __init__(self, threshold=5):
        self.img = ImagePipeline()
        self.ett = EstTimePipeline()
        self.tf = TrafficFlowPipeline()
        self.yolo = TrafficTrackerYoloV3()
        self.threshold = threshold
    
    def generate_cc(self, user_lat, user_long):
        img_ = self.img.get_data(user_lat, user_long)
        count, _ = self.yolo.get_count(img_)
        if count >= self.threshold:
            return "high"
        else:
            return "low"
        
    def retrieve(self, user_lat, user_long, dest_lat, dest_long):
        cc = self.generate_cc(user_lat, user_long)
        return {
            "cc" : cc
        }