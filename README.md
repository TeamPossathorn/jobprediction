
# Job Title Prediction Web Interface

## 🔧 How to Deploy with Streamlit Cloud

1. Clone this repository and add your `app.py`, `requirements.txt`, and `job_title_pipeline.py`.
2. Update the `PROJECT_ID`, `BUCKET_NAME`, and paths in `app.py`.
3. Ensure the following are uploaded to GCS:
   - `job_title_pipeline.py` (PySpark job script)
   - Trained model directory: `job_title_classification_model/`
4. Trigger PySpark jobs using Dataproc (can be automated or scheduled).
5. Deploy to [https://streamlit.io/cloud](https://streamlit.io/cloud).

## 📦 Requirements

- Streamlit Cloud account
- GCP with:
  - GCS bucket to hold model, input, output
  - Dataproc cluster to run prediction job

## Example Usage

Paste a job description in the input box, click "Predict", and wait for the job title prediction and similar job insights.
