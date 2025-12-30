from ultralytics import YOLO 
from pathlib import Path

from db_recorder import init_db, record_classification

Model_Path = 'runs/train3/weights/last.pt'
Img_Path = 'C:/Users/Pranj/Downloads/c.jpg'

Class_Name = ["buffalo", "cattle"]

def main():

    init_db()
    
    model = YOLO(Model_Path)

    result = model(Img_Path)[0]

    class_id = int(result.probs.top1)
    confidence = float(result.probs.top1conf)
    pred_class = Class_Name[class_id]

    record_classification(
        img_name = Path(Img_Path).name,
        pred_class = pred_class,
        confidence = confidence
    )

    print("Classification Result")
    print("---------------------")
    print(f"Image       : {Img_Path}")
    print(f"Prediction  : {pred_class}")
    print(f"Confidence  : {confidence:.2f}")

if __name__ == "__main__":
    main()
