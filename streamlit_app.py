import streamlit as st
import os
import zipfile
import requests
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel

# Setup Spark session
spark = SparkSession.builder.appName("JobTitlePredictor").getOrCreate()

# Download model zip from GitHub
MODEL_URL = "https://github.com/your-repo/job_title_classification_model.zip?raw=true"
MODEL_DIR = "job_title_classification_model"
ZIP_PATH = "model.zip"

if not os.path.exists(MODEL_DIR):
    st.info("📥 Downloading model from GitHub...")
    r = requests.get(MODEL_URL)
    with open(ZIP_PATH, "wb") as f:
        f.write(r.content)
    with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
        zip_ref.extractall(".")
    st.success("✅ Model ready!")

# Load model
model = PipelineModel.load(MODEL_DIR)

# Streamlit UI
st.title("🧠 Job Title Predictor")
desc = st.text_area("✍️ Enter Job Description:", height=200)

if st.button("Predict"):
    df = spark.createDataFrame([(desc, "placeholder")], ["Job Description", "Job Title"])
    result = model.transform(df).select("prediction").collect()[0][0]
    st.success(f"🎯 Predicted Job Title Index: {result}")
