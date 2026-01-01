from flask import Flask, render_template, request, send_from_directory, url_for
from werkzeug.utils import secure_filename
from pathlib import Path
import os
 
from classify_service import classify_img
from db_recorder import init_db, record_classification, fetch_all

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

Path(UPLOAD_FOLDER).mkdir(exist_ok=True)
init_db()

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():

    if "file" not in request.files:
        return "No file uploaded", 400

    file = request.files["file"]

    if file.filename == "":
        return "No file selected", 400

    if not allowed_file(file.filename):
        return "Invalid file type. Upload JPG or PNG", 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    # Run inference
    pred_class, confidence = classify_img(file_path)

    # Save to SQLite
    record_classification(
        img_name=filename,
        pred_class=pred_class,
        confidence=confidence
    )

    return render_template(
        "index.html",
        prediction=pred_class,
        confidence=f"{confidence:.2f}",
        image_path=url_for("uploaded_file", filename=filename)
    )

@app.route("/upload/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/records")
def records():
    records = fetch_all()
    return render_template("records.html", records = records)

if __name__ == "__main__":
    app.run(debug=True)
