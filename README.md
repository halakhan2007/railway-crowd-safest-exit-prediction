# 🚆 Railway Crowd and Safest Exit Prediction

A Semester 3 B.Sc. Data Science group project that explores railway platform crowd prediction, train-platform assignment, and exit-route recommendations using Python.

## 📌 Project Overview

The **Smart Railway Crowd Monitor** is an educational prototype that combines crowd forecasting and route-cost calculations in an interactive Streamlit dashboard.

The project aims to estimate future crowd levels across railway platforms and zones, demonstrate example train-platform assignments, and recommend routes based on manually defined distance and congestion weights.

## 🌐 Live Demo

Try the Railway Crowd and Safest Exit Prediction web app:

**[Open Live Web App](https://railway-crowd-safest-exit-prediction-fcunu3n9kqsdpiztgukw38.streamlit.app/)**

*Note: This is an educational prototype. Crowd predictions and route recommendations are based on illustrative assumptions and are not verified railway safety guidance.*

## ✨ Features

- Platform and zone selection
- Crowd predictions for 10, 20, and 45 minutes
- Crowd-status classification and alerts
- Interactive crowd prediction chart
- Example train-platform assignments based on predicted crowd scores
- Route recommendations involving Exit A, Exit B, and Exit C
- CSV-based prediction outputs
- Interactive dashboard built with Streamlit

## 🛠️ Technologies Used

- **Python** for data processing and calculations
- **Streamlit** for the interactive dashboard
- **Pandas** for dataset manipulation
- **NumPy** for numerical operations

## 📂 Project Structure

```text
Railway-Crowd-and-Safest-Exit-Prediction/
│
├── app.py
├── crowd_prediction.py
├── route_prediction.py
├── crowd_prediction_output.csv
├── route_prediction_output.csv
├── requirements.txt
├── .gitignore
└── README.md
```

**Note:** The input dataset is not intended for public distribution until its source and sharing permissions have been verified. If it is excluded from the repository, users will need an authorized input dataset at the expected file path to regenerate the predictions.

## 🚀 Installation and Setup

### Prerequisites

- Python 3.10 or a compatible version
- pip, Python's package installer
- The required input dataset, when regenerating predictions

### 1. Clone the repository

```bash
git clone https://github.com/halakhan2007/railway-crowd-safest-exit-prediction.git
cd <YOUR_REPOSITORY_FOLDER>
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Generate crowd predictions

Ensure the authorized input dataset is available in the project directory, then run:

```bash
python crowd_prediction.py
```

This generates `crowd_prediction_output.csv`.

### 4. Generate route recommendations

```bash
python route_prediction.py
```

This generates `route_prediction_output.csv`.

### 5. Launch the dashboard

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal to use the dashboard.

**Execution order:** Run `crowd_prediction.py` first, then `route_prediction.py`, and finally `app.py`.

If the generated output CSV files are already included in the repository, the dashboard can display those saved results without rerunning the prediction scripts, provided the files match the expected format.

## 📊 Dataset and Attribution

The dataset was prepared by extracting numerical observations from publicly available videos showing conditions on railway platforms at Kalyan station at particular points in time.

The observations were organized into a structured dataset for educational and academic project purposes. The dataset is not an official railway dataset, and the observations may not represent current platform conditions.

The original video links and complete source details are unavailable, so the sources and redistribution permissions have not been independently verified.

**Note:** This project is an educational prototype. Its crowd predictions and route recommendations are based on simplified assumptions and should not be used for real-world railway safety or travel decisions.

**Dataset transparency:**

- The dataset is not claimed to be official railway data.
- **Demo Junction** is a hypothetical display name used by the application; it does not establish the actual location shown in the source footage.
- The original extracted dataset should not be publicly distributed until the relevant source terms and permissions have been checked.
- Any synthetic demonstration data added in the future will be clearly identified as synthetic and kept distinct from observations extracted from footage.

## ⚠️ Limitations

- This is an educational prototype, not an operational railway safety system.
- Crowd-status thresholds are predefined assumptions, not official railway crowd-safety standards.
- Crowd predictions depend on the available observations and the logic implemented in the prediction script.
- Example train schedules and platform assignments are illustrative and do not represent verified live railway operations.
- Route recommendations use manually defined costs and congestion weights.
- A route with the lowest calculated cost is not necessarily the safest route in real-world conditions.
- The system does not replace official railway announcements, station staff, or emergency instructions.
- Predictions and recommendations must not be used for actual travel, evacuation, or emergency decisions.

## 🔮 Future Improvements

- Evaluate prediction accuracy using additional verified datasets.
- Explore and compare suitable machine-learning models.
- Improve handling of missing, inconsistent, and time-dependent observations.
- Calibrate crowd thresholds using appropriate validated evidence.
- Use verified platform layouts, route distances, and accessibility information.
- Evaluate route recommendations against realistic congestion and safety conditions.
- Add more robust input validation and error handling.
- Improve dashboard visualizations and reporting.

## 👥 Contributors

This project was developed collaboratively as part of a Semester 3 B.Sc. Data Science group project.

- **Abrelicia Fernandes**
- **Hani Gazi**
- **Sanjana Gupta**
- **Hala Khan**

## 🎓 Project Context

Developed as a Semester 3 B.Sc. Data Science group project to explore practical applications of Python, data processing, crowd prediction, and route-cost analysis.

---

*This project is intended for educational and demonstration purposes only.*
