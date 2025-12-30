import os
import numpy as np
from ultralytics import YOLO
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)
import matplotlib.pyplot as plt
import seaborn as sns

Model_Path = "runs/train3/weights/last.pt"
Test_Dir = "dataset/val"
Class_Names = sorted(os.listdir(Test_Dir))

model = YOLO(Model_Path)

y_true = []
y_pred = []

for class_idx, class_name in enumerate(Class_Names):
    class_path = os.path.join(Test_Dir, class_name)

    for img_name in os.listdir(class_path):
        img_path = os.path.join(class_path, img_name)

        result = model(img_path, verbose=False)[0]
        pred_class = result.probs.top1

        y_true.append(class_idx)
        y_pred.append(pred_class)

y_true = np.array(y_true)
y_pred = np.array(y_pred)

accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred, average='weighted')
recall = recall_score(y_true, y_pred, average='weighted')
f1 = f1_score(y_true, y_pred, average='weighted')

print("\n Evaluation Metrics")
print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1-Score  : {f1:.4f}")


print("\n Classification Report:")
print(classification_report(y_true, y_pred, target_names = Class_Names))

cm = confusion_matrix(y_true, y_pred)

plt.figure(figsize = (6, 5))
sns.heatmap(
    cm,
    annot = True,
    fmt = 'd',
    cmap = 'Blues',
    xticklabels = Class_Names,
    yticklabels = Class_Names
)

plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion Matrix")
plt.tight_layout()
plt.show()
