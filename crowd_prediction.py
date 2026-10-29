import pandas as pd
# 1. LOAD DATA

FILE_NAME = "Demo_Junction_Crowd_Dataset.csv"

df = pd.read_csv(FILE_NAME)

print("=" * 65)
print("SMART RAILWAY PLATFORM CROWD PREDICTION")
print("=" * 65)

print("\nDataset loaded successfully")
print("Total rows:", len(df))



# ============================================================
# 2. CLEAN DATA
# ============================================================

# Convert timestamps to datetime
df["Timestamp"] = pd.to_datetime(
    df["Timestamp"].astype(str),
    format="%H:%M:%S",
    errors="coerce"
)

# Convert numeric columns
numeric_columns = [
    "Crowd_Count",
    "Train_Arrival",
    "Train_delay"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column], errors="coerce"
    )

# Remove rows with invalid essential values
df = df.dropna(
    subset=[
        "Timestamp",
        "Platform",
        "Zone",
        "Crowd_Count"
    ]
).copy()

# Use zero only when train information is missing
df["Train_Arrival"] = df["Train_Arrival"].fillna(0)
df["Train_delay"] = df["Train_delay"].fillna(0)

# Ensure the arrival indicator is binary
df = df[df["Train_Arrival"].isin([0, 1])].copy()

print("Rows remaining after cleaning:", len(df))


# ============================================================
# 3. MERGE SORT
# ============================================================

def merge_sort(data):

    if len(data) <= 1:
        return data

    mid = len(data) // 2

    left = merge_sort(data[:mid])
    right = merge_sort(data[mid:])

    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):

        if left[i]["Timestamp"] <= right[j]["Timestamp"]:
            result.append(left[i])
            i += 1

        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


records = df.to_dict("records")

sorted_data = merge_sort(records)

print("Merge Sort completed.")


# ============================================================
# 4. BINARY SEARCH
# ============================================================

def binary_search(data, target):

    low = 0
    high = len(data) - 1

    while low <= high:

        mid = (low + high) // 2

        if data[mid]["Timestamp"] == target:
            return data[mid]

        elif data[mid]["Timestamp"] < target:
            low = mid + 1

        else:
            high = mid - 1

    return None


# ============================================================
# 5. CROWD STATUS
# ============================================================

def crowd_status(crowd):

    if crowd <= 100:
        return "SAFE"

    elif crowd <= 150:
        return "MODERATE"

    elif crowd <= 200:
        return "HIGH"

    else:
        return "CRITICAL"


# ============================================================
# 6. CALCULATE CROWD TREND
# ============================================================

def calculate_trend(data):

    if len(data) < 2:
        return 0

    # Use the latest 4 observations
    recent = data[-4:]

    rates = []

    for i in range(1, len(recent)):

        time_difference = (
            recent[i]["Timestamp"]
            - recent[i - 1]["Timestamp"]
        ).total_seconds() / 60

        crowd_difference = (
            recent[i]["Crowd_Count"]
            - recent[i - 1]["Crowd_Count"]
        )

        if time_difference > 0:

            rate = crowd_difference / time_difference
            rates.append(rate)

    if not rates:
        return 0

    return sum(rates) / len(rates)


# ============================================================
# 7. TRAIN IMPACT
# ============================================================

def calculate_train_impact(record):

    arrival = record["Train_Arrival"]
    delay = record["Train_delay"]

    # Prototype rule-based impact
    arrival_impact = 10 if arrival > 0 else 0
    delay_impact = delay * 2

    return arrival_impact + delay_impact


# ============================================================
# 8. PREDICT CROWD FOR ONE ZONE
# ============================================================

def predict_zone(data):

    if not data:
        return None

    current = data[-1]

    current_crowd = current["Crowd_Count"]

    trend = calculate_trend(data)

    train_impact = calculate_train_impact(current)

    predictions = {}

    for minutes in [10, 20, 45]:

        predicted = (
            current_crowd
            + trend * minutes
            + train_impact
        )

        predicted = max(0, round(predicted))

        predictions[minutes] = predicted

    return {
        "current_crowd": current_crowd,
        "trend": round(trend, 2),
        "train_impact": train_impact,
        "prediction_10": predictions[10],
        "prediction_20": predictions[20],
        "prediction_45": predictions[45]
    }


# ============================================================
# 9. PROCESS EVERY PLATFORM + ZONE
# ============================================================

results = []

groups = df.groupby(["Platform", "Zone"])

print("\nProcessing Platform + Zone combinations...")

for (platform, zone), group in groups:

    # Get sorted records belonging to this zone
    zone_data = [
        record for record in sorted_data
        if record["Platform"] == platform
        and record["Zone"] == zone
    ]

    # Need at least 2 records for trend calculation
    if len(zone_data) < 2:
        continue

    result = predict_zone(zone_data)

    if result is None:
        continue

    results.append({

        "Platform": platform,

        "Zone": zone,

        "Records": len(zone_data),

        "Current_Crowd":
            result["current_crowd"],

        "Trend_Per_Minute":
            result["trend"],

        "Train_Impact":
            result["train_impact"],

        "Prediction_10_Min":
            result["prediction_10"],

        "Status_10_Min":
            crowd_status(result["prediction_10"]),

        "Prediction_20_Min":
            result["prediction_20"],

        "Status_20_Min":
            crowd_status(result["prediction_20"]),

        "Prediction_45_Min":
            result["prediction_45"],

        "Status_45_Min":
            crowd_status(result["prediction_45"])
    })


# ============================================================
# 10. CREATE FINAL OUTPUT
# ============================================================

output = pd.DataFrame(results)

# Sort output by Platform and Zone
output = output.sort_values(
    ["Platform", "Zone"]
)


# ============================================================
# 11. SAVE OUTPUT
# ============================================================

output.to_csv(
    "crowd_prediction_output.csv",
    index=False
)


# ============================================================
# 12. DISPLAY SUMMARY
# ============================================================

print("\n" + "=" * 65)
print("PREDICTION COMPLETED")
print("=" * 65)

print("Total Platform + Zone combinations:", len(output))

print("\nSample predictions:\n")

print(
    output.head(10).to_string(index=False)
)

print("\nPrediction saved as:")
print("crowd_prediction_output.csv")

# 13. BINARY SEARCH DEMONSTRATION
if len(sorted_data) > 0:

    target_time = sorted_data[-1]["Timestamp"]

    search_result = binary_search(
        sorted_data,
        target_time
    )

    print("\n" + "=" * 65)
    print("BINARY SEARCH DEMONSTRATION")
    print("=" * 65)

    print(
        "Searching timestamp:",
        target_time.strftime("%H:%M:%S")
    )

    if search_result:
        print("Record found!")

        print(
            "Platform:",
            search_result["Platform"]
        )

        print(
            "Zone:",
            search_result["Zone"]
        )

        print(
            "Crowd:",
            search_result["Crowd_Count"]
        )

    else:
        print("Record not found.")

print("\n" + "=" * 65)
print("PROGRAM COMPLETED SUCCESSFULLY")
print("=" * 65)