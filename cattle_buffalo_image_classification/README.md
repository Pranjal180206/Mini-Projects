# Image-Based Breed Recognition (Cattle & Buffalo)

## Overview
An AI-based image classification system for identifying **cattle and buffalo breeds** using deep learning.  
This project is inspired by a **Smart India Hackathon (SIH)** problem statement on image-based livestock breed recognition.

The system uses a **YOLOv8 classification model** with a **Flask web interface** for image upload and prediction.

---

## Features
- Cattle vs buffalo breed classification from images  
- YOLOv8 deep learning model  
- Flask-based web application  
- Confidence score for predictions  
- SQLite database for logging results  

---

## Tech Stack
- Python  
- Ultralytics YOLOv8  
- Flask  
- SQLite  
- OpenCV / PIL  

---

## Project Structure
```
.
├── templates/              # HTML templates for Flask UI
├── app.py                  # Flask app for cattle & buffalo image classification
├── augment_buffalo.py      # Image augmentation script for buffalo images
├── classify_record.py      # Image classification + prediction recording
├── classify_service.py     # YOLO-based inference service for Flask
├── db_recorder.py          # SQLite database recording for predictions
├── evaluate_model.py       # Model evaluation and metrics
├── records_fetch.py        # Fetch and display stored classification records
└── train.py                # YOLOv8 model training script
```
---

## Setup Instructions

### 1️. Clone the repository
```bash
git clone <repo-url>
cd <project-folder>
```

### 2️. Create virtual environment (recommended)
```bash
python -m venv venv
venv\Scripts\activate
```

### 3️. Install dependencies
```bash
pip install -r requirements.txt
```

### 4️. Train the model (optional)
```bash
python train.py
```

### 5️. Run the Flask app
```bash
python app.py
```

### Open browser at:
```bash
http://127.0.0.1:5000
```

## Notes

- Not an official SIH submission
- Inspired by an SIH livestock breed recognition problem statement
- Designed for future scalability and deployment
