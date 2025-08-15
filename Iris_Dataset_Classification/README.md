# Iris Dataset Classification

This project demonstrates a **machine learning classification pipeline** using the classic [Iris dataset](https://archive.ics.uci.edu/ml/datasets/iris).  
It includes **data loading, visualization, model training, and evaluation** using popular algorithms.

---

## 📌 Project Overview
The Iris dataset contains 150 samples of iris flowers with four features:
- **Sepal length**
- **Sepal width**
- **Petal length**
- **Petal width**

The task is to classify each flower into one of three species:
- *Iris-setosa*
- *Iris-versicolor*
- *Iris-virginica*

This project:
1. Loads and explores the dataset
2. Visualizes feature relationships
3. Splits the dataset into training and validation sets
4. Trains multiple classification models
5. Compares performance using evaluation metrics

---

## 🛠 Technologies Used
- **Python 3**
- **Pandas** – data handling
- **Matplotlib** – visualization
- **Scikit-learn** – model building & evaluation

---

## 📂 Project Structure
```
.
├── iris_classification.ipynb   # Main Jupyter Notebook
├── iris.data                   # Dataset (CSV format)
├── README.md                   # Project documentation
```

---

## ⚙️ Installation & Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/iris-classification.git
   cd iris-classification
   ```
2. Install dependencies:
   ```bash
   pip install pandas matplotlib scikit-learn
   ```
3. Open the notebook:
   ```bash
   jupyter notebook iris_classification.ipynb
   ```

---

## 📊 Models Implemented
- Logistic Regression
- Decision Tree Classifier
- K-Nearest Neighbors (KNN)
- Random Forest Classifier

---

## 🧪 Evaluation Metrics
- Accuracy Score
- Confusion Matrix
- Classification Report (Precision, Recall, F1-score)

---

## 🔮 Results
The models were compared, and **Random Forest** achieved the highest accuracy on the validation set.

---

## 📜 License
This project is open source and available under the [MIT License](LICENSE).
