from ultralytics import YOLO
from pathlib import Path

Model_Path = 'runs/train3/weights/last.pt'
Class_Names = ["buffalo", "cattle"]

model = YOLO(Model_Path)

def classify_img (img_path):
    
    img_path = str(img_path)

    result = model(img_path)[0]

    class_id = int(result.probs.top1)
    confidence = float(result.probs.top1conf)

    pred_class = Class_Names[class_id]

    return pred_class, confidence
