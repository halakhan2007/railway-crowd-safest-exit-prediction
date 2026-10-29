import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Smart Railway Monitor",
    page_icon="🚆",
    layout="wide"
)

# Page title
st.title("🚆 Demo Junction Crowd Monitor")
st.caption("Educational prototype using railway-platform crowd observations.")

# Load Member 2's prediction data
df = pd.read_csv("crowd_prediction_output.csv")

# Rename the platform column
if "Platform" not in df.columns and "Unnamed: 0" in df.columns:
    df = df.rename(columns={"Unnamed: 0": "Platform"})

if "Platform" not in df.columns:
    st.error("Platform column is missing from the prediction file.")
    st.stop()

# Platform selection
platforms = sorted(df["Platform"].unique())

selected_platform = st.selectbox(
    "Select Platform",
    platforms
)

# Filter data for selected platform
platform_data = df[df["Platform"] == selected_platform]

# Zone selection
zones = sorted(platform_data["Zone"].unique())

selected_zone = st.selectbox(
    "Select Zone",
    zones
)

# Get selected zone's data
selected_data = platform_data[
    platform_data["Zone"] == selected_zone
]

st.subheader(f"{selected_platform} — {selected_zone}")

# Get the selected row
if selected_data.empty:
    st.warning("No prediction data is available for this zone.")
    st.stop()

row = selected_data.iloc[0]

# Current information
st.write("### 👥 Current Crowd")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Current Crowd",
        int(row["Current_Crowd"])
    )

with col2:
    st.metric(
        "Trend / Minute",
        row["Trend_Per_Minute"]
    )

with col3:
    st.metric(
        "Train Impact",
        int(row["Train_Impact"])
    )

# Prediction section
st.write("### 📈 Crowd Prediction")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Next 10 Minutes",
        int(row["Prediction_10_Min"])
    )
    st.write(f"Status: **{row['Status_10_Min']}**")

with col2:
    st.metric(
        "Next 20 Minutes",
        int(row["Prediction_20_Min"])
    )
    st.write(f"Status: **{row['Status_20_Min']}**")

with col3:
    st.metric(
        "Next 45 Minutes",
        int(row["Prediction_45_Min"])
    )
    st.write(f"Status: **{row['Status_45_Min']}**")

# Alert section
statuses = [
    row["Status_10_Min"],
    row["Status_20_Min"],
    row["Status_45_Min"]
]

if "CRITICAL" in statuses:
    st.error(
        f"🚨 CRITICAL CROWD ALERT: "
        f"Critical crowd is predicted in {selected_zone}."
    )

elif "HIGH" in statuses:
    st.warning(
        f"⚠️ HIGH CROWD ALERT: "
        f"High crowd is predicted in {selected_zone}."
    )

elif "MODERATE" in statuses:
    st.info(
        f"ℹ️ MODERATE CROWD: "
        f"Moderate crowd is predicted in {selected_zone}."
    )

else:
    st.success(
        f"✅ No HIGH or CRITICAL crowd level is predicted "
        f"in {selected_zone} for the selected forecast periods."
    )
    
# Prediction graph
st.write("### 📈 Crowd Prediction Graph")

chart_data = pd.DataFrame({
    "Time": ["Current", "10 min", "20 min", "45 min"],
    "Crowd": [
        int(row["Current_Crowd"]),
        int(row["Prediction_10_Min"]),
        int(row["Prediction_20_Min"]),
        int(row["Prediction_45_Min"])
    ]
})

st.line_chart(
    chart_data.set_index("Time")
)    

# --------------------------------------------------
# Member 3 - Train & Route Recommendation
# --------------------------------------------------

st.write("### 🚆 Train & Route Recommendation")

# Load Member 3's output
route_df = pd.read_csv("route_prediction_output.csv")

# Select a train
train_numbers = route_df["Train_No"].astype(str).tolist()

selected_train = st.selectbox(
    "Select Train",
    train_numbers
)

# Get selected train's information
train_data = route_df[
    route_df["Train_No"].astype(str) == selected_train
].iloc[0]

# Display train information
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Train",
        str(train_data["Train_No"])
    )

with col2:
    st.metric(
        "Arrival",
        str(train_data["Arrival"])
    )

with col3:
    st.metric(
        "Departure",
        str(train_data["Departure"])
    )

st.write("#### Platform & Crowd")

col1, col2 = st.columns(2)

with col1:
    st.info(
        f"🚉 Assigned Platform: "
        f"**{train_data['Assigned_Platform']}**"
    )

with col2:
    st.info(
        f"👥 Predicted Crowd: "
        f"**{train_data['Predicted_Crowd']}**"
    )

st.write("#### 🧭 Route Recommendation")

st.success(
    f"Recommended Exit: **{train_data['Recommended_Exit']}**"
)

st.write(
    f"**Route:** {train_data['Recommended_Route']}"
)

st.write(
    f"**Route Cost:** {train_data['Route_Cost']}"
)