# Image-Based Animal Type Classification System (Cattle & Buffalo)

This project implements an AI-based system for image-driven animal type classification, focusing on cattle and buffalo.  
The goal is to demonstrate how machine learning models can be integrated into a **reliable, auditable, and usable software system**, rather than existing as isolated experiments.

The system is designed as a **working prototype** aligned with real-world livestock data workflows, such as those used in government and dairy breeding programs.

---

## Problem Context

In dairy breeding programs, Animal Type Classification (ATC) is used to evaluate physical characteristics of animals to support decisions related to longevity, productivity, and breeding potential.  
Currently, this process relies heavily on manual visual inspection, which introduces subjectivity, fatigue-related errors, and inconsistent data recording.

This project explores how AI-based image analysis can assist this process by:
- Providing objective and repeatable classification
- Automatically recording results
- Enabling future data-driven refinement

---

## What This System Does

- Accepts an image of an animal through a web interface
- Classifies the image as **cattle** or **buffalo**
- Outputs a confidence score for each prediction
- Automatically logs every prediction into a structured database
- Provides a prediction history dashboard for review and analysis

The emphasis is on **system completeness and traceability**, not just model accuracy.

---

## Key Features

- Image-based cattle vs buffalo classification using a deep learning model
- Flask web application for interactive inference
- Automatic prediction logging with timestamp, class, and confidence
- SQLite-based persistence for offline-first operation
- Prediction history dashboard with low-confidence highlighting
- Clean separation between ML inference, database logic, and web layer

---

## System Architecture (High Level)

```bash
User Image Upload
        ↓
Flask Web Interface
        ↓
Inference Service (YOLOv8 Classifier)
        ↓
Prediction + Confidence
        ↓
SQLite Auto-Recording
        ↓
History & Review Dashboard
```

This modular design allows future extensions without destabilizing the core system.

---

## Project Structure

```bash
CATTLE_BUFFALO/
├── app.py # Flask application
├── classify_service.py # Model loading and inference
├── db_recorder.py # SQLite auto-recording logic
├── train.py # Model training pipeline
├── evaluate_model.py # Evaluation and metrics
├── augment_buffalo.py # Data augmentation (minority class)
├── records_fetch.py # CLI utility for viewing records
├── templates/
│ ├── index.html # Upload & prediction UI
│ └── records.html # Prediction history dashboard
```

Runtime artifacts such as datasets, trained weights, uploads, and databases are excluded from version control.

---

## Model Training and Evaluation

- Trained using a YOLOv8 classification architecture
- Dataset split into training and validation sets
- Targeted data augmentation applied to reduce class imbalance
- Evaluated using:
  - Accuracy
  - Precision
  - Recall
  - F1-score
  - Confusion matrix

Model selection prioritized **balanced performance and stability** rather than raw accuracy alone.

---

## Tier-2 Extension: Prediction History & Auditability

As a second-stage enhancement, the system includes a **prediction history dashboard**:

- Displays all past predictions from the database
- Shows timestamp, image name, predicted class, and confidence
- Highlights low-confidence predictions (< 0.8) for manual review

This feature reflects real-world decision-support workflows where AI outputs are reviewed rather than blindly accepted.

---

## Design Considerations & Future Extensions

Certain aspects of full Animal Type Classification — such as precise body measurements — require:
- Pose estimation and keypoint detection
- Camera calibration and reference objects
- Controlled data capture conditions

These are intentionally **proposed but not implemented** in this prototype to maintain scientific validity and system stability.

Future work may include:
- Pose-based trait extraction using keypoints
- Integration with external systems (e.g., BPA) via APIs
- Dataset expansion using logged real-world samples
- Cloud deployment on container-based platforms

---

## Limitations

- The model may misclassify visually ambiguous images due to similarity between cattle and buffalo
- Performance is constrained by dataset size and class imbalance
- The system is intended as a prototype and learning artifact, not a production deployment

These limitations are documented deliberately and inform future improvement paths.

---

## Technology Stack

- Python
- Ultralytics YOLOv8
- Flask
- SQLite
- OpenCV

---

## Notes

This repository represents a stable Tier-1 system with a safe Tier-2 extension.  
Further enhancements should prioritize data quality and system robustness over model complexity.
