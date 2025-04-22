
import streamlit as st
from google.cloud import storage
import uuid
import json
import time
import os

PROJECT_ID = "your-gcp-project-id"
BUCKET_NAME = "job-title-predict-bucket"
INPUT_PATH = "job-description-inputs"
OUTPUT_PATH = "job-results"

st.title("🔍 Job Title Prediction")
desc = st.text_area("📝 Enter job description:", "Looking for a backend developer with cloud experience")

if st.button("🚀 Predict Job Title"):
    uid = uuid.uuid4().hex[:8]
    input_file = f"{INPUT_PATH}/input_{uid}.txt"
    output_file = f"{OUTPUT_PATH}/output_{uid}.json"
    local_input = f"/tmp/input_{uid}.txt"

    with open(local_input, "w") as f:
        f.write(desc)

    client = storage.Client(project=PROJECT_ID)
    bucket = client.bucket(BUCKET_NAME)
    bucket.blob(input_file).upload_from_filename(local_input)

    st.info("📡 Waiting for prediction result...")
    for _ in range(30):
        if storage.Blob(bucket=bucket, name=output_file).exists(client):
            content = bucket.blob(output_file).download_as_text()
            result = json.loads(content)
            st.success(f"🔮 Predicted Title: {result['predicted_title']}")
            for i, job in enumerate(result["top_similar"], 1):
                st.markdown(f"**{i}. {job['job_title']}** — {job['company']} ({job['sector']} > {job['industry']})<br>"
                            f"📍 {job['location']}, {job['country']} | 💰 {job['salary_range']}<br>"
                            f"🎓 {job['qualifications']} | 🔗 Similarity: {job['cosine']}", unsafe_allow_html=True)
            break
        time.sleep(3)
    else:
        st.error("❌ Prediction result not found.")

    os.remove(local_input)
