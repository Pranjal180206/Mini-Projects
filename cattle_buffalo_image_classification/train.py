from ultralytics import YOLO

def main():
    model = YOLO('yolov8n-cls.pt')
    model.train(
        data = 'dataset',
        epochs = 30,
        device = '0',
        project = 'runs'
    )

if __name__ == "__main__":
    main()  
