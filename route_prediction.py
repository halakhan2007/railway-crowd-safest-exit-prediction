import pandas as pd
from collections import deque
import heapq

df = pd.read_csv("crowd_prediction_output.csv")

platform_crowd = (
    df.groupby("Platform")["Prediction_10_Min"]
    .sum()
)

print("\nPredicted crowd by platform:")
print(platform_crowd.sort_values().to_string())

# Train schedule data
trains = [
    {"train_no": "12001", "arrival": "17:20", "departure": "17:25"},
    {"train_no": "12015", "arrival": "17:25", "departure": "17:30"},
    {"train_no": "12110", "arrival": "17:30", "departure": "17:35"},
    {"train_no": "12205", "arrival": "17:35", "departure": "17:40"},
    {"train_no": "12320", "arrival": "17:40", "departure": "17:45"}
]

# Available platforms
platforms = [
    "Platform 1",
    "Platform 1A",
    "Platform 2",
    "Platform 3",
    "Platform 4",
    "Platform 5",
    "Platform 6",
    "Platform 7",
    "Platform 8"
]


# Store train-platform assignments
platform_allocation = {}

train_queue = deque(trains)

available_platforms = platforms.copy()

platform_free_time = {
    platform: 0
    for platform in platforms
}

def time_to_minutes(time):
    hours, minutes = map(int, time.split(":"))
    return hours * 60 + minutes


for _ in range(len(trains)):
    current_train = train_queue.popleft()

    arrival_time = time_to_minutes(current_train["arrival"])
    departure_time = time_to_minutes(current_train["departure"])

   # Allow a 5-minute clearance buffer between trains
    CLEARANCE_MINUTES = 5

    available_platforms_now = [
        platform
        for platform in available_platforms
        if platform_free_time[platform] + CLEARANCE_MINUTES
        <= arrival_time
    ]

    # Keep only platforms with crowd data
    available_crowd = platform_crowd[
        platform_crowd.index.isin(available_platforms_now)
    ]

    # Handle missing crowd data or unavailable platforms
    if available_crowd.empty:
        print(
            f"Warning: No suitable platform available for train "
            f"{current_train['train_no']}"
        )
        continue

    # Select the available platform with the lowest predicted crowd
    selected_platform = available_crowd.idxmin()

    # Mark the platform as occupied until departure
    platform_free_time[selected_platform] = departure_time

    # Save the allocation
    platform_allocation[current_train["train_no"]] = {
        "platform": selected_platform,
        "arrival": current_train["arrival"],
        "departure": current_train["departure"],
        "predicted_crowd": platform_crowd[selected_platform]
    }

    print(
        current_train["train_no"],
        "| Arrival:", current_train["arrival"],
        "| Departure:", current_train["departure"],
        "| Platform:", selected_platform,
        "| Predicted crowd:", platform_crowd[selected_platform]
    )


# Station graph
graph = {
    "Platform 1": [("Junction", 15)],
    "Platform 1A": [("Junction", 18)],
    "Platform 2": [("Junction", 20)],
    "Platform 3": [("Junction", 22)],
    "Platform 4": [("Junction", 25)],
    "Platform 5": [("Junction", 28)],
    "Platform 6": [("Junction", 30)],
    "Platform 7": [("Junction", 32)],
    "Platform 8": [("Junction", 35)],

    "Junction": [
        ("Platform 1", 15),
        ("Platform 1A", 18),
        ("Platform 2", 20),
        ("Platform 3", 22),
        ("Platform 4", 25),
        ("Platform 5", 28),
        ("Platform 6", 30),
        ("Platform 7", 32),
        ("Platform 8", 35),
        ("Exit A", 20),
        ("Exit B", 25),
        ("Exit C", 30)
    ],

    "Exit A": [("Junction", 20)],
    "Exit B": [("Junction", 25)],
    "Exit C": [("Junction", 30)]
}

# Dijkstra's shortest path algorithm
def dijkstra(graph, start, crowd=0):

    distances = {node: float("inf") for node in graph}
    previous = {node: None for node in graph}

    distances[start] = 0

    priority_queue = [(0, start)]

    while priority_queue:

        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node]:

            # Add crowd penalty when leaving the platform
            if current_node.startswith("Platform") and neighbor == "Junction":
                new_distance = (
                current_distance
                + weight
                + crowd_penalty(crowd)
                )

            # Add exit congestion penalty
            elif current_node == "Junction" and neighbor in exit_congestion:
                new_distance = (
                current_distance
                + weight
                + (crowd * exit_congestion[neighbor])
                )

            else:
                new_distance = current_distance + weight

            if new_distance < distances[neighbor]:

                distances[neighbor] = new_distance
                previous[neighbor] = current_node

                heapq.heappush(
                    priority_queue,
                    (new_distance, neighbor)
                )

    return distances, previous

# Reconstruct the shortest route
def get_route(previous, start, destination):

    route = []
    current = destination

    while current is not None:
        route.append(current)
        current = previous[current]

    route.reverse()

    if route[0] != start:
        return []

    return route

def crowd_penalty(crowd):
    if crowd >= 200:
        return 30
    elif crowd >= 100:
        return 15
    else:
        return 5

exits = ["Exit A", "Exit B", "Exit C"]

exit_congestion = {
    "Exit A": 0.10,
    "Exit B": 0.05,
    "Exit C": 0.02
}

# Recommend the best route for each allocated train

print("\nFinal Route Recommendations:")
print("-----------------------------")

for train_no, allocation in platform_allocation.items():

    assigned_platform = allocation["platform"]
    arrival = allocation["arrival"]
    departure = allocation["departure"]
    predicted_crowd = allocation["predicted_crowd"]

    distances, previous = dijkstra(
    graph,
    assigned_platform,
    predicted_crowd
    )

    best_exit = min(exits, key=lambda exit: distances[exit])

    best_distance = distances[best_exit]

    best_route = get_route(
        previous,
        assigned_platform,
        best_exit
    )

    print("\nTrain:", train_no)
    print("Arrival:", arrival)
    print("Departure:", departure)
    print("Assigned Platform:", assigned_platform)
    print("Predicted Crowd:", predicted_crowd)
    print("Recommended Exit:", best_exit)
    print("Recommended Route:", " → ".join(best_route))
    print("Route Cost:", round(best_distance, 2))

# Save final results to CSV

results = []

for train_no, allocation in platform_allocation.items():

    assigned_platform = allocation["platform"]
    arrival = allocation["arrival"]
    departure = allocation["departure"]
    predicted_crowd = allocation["predicted_crowd"]

    distances, previous = dijkstra(
        graph,
        assigned_platform,
        predicted_crowd
    )

    best_exit = min(
        exits,
        key=lambda exit: distances[exit]
    )

    best_distance = distances[best_exit]

    best_route = get_route(
        previous,
        assigned_platform,
        best_exit
    )

    results.append({
        "Train_No": train_no,
        "Arrival": arrival,
        "Departure": departure,
        "Assigned_Platform": assigned_platform,
        "Predicted_Crowd": predicted_crowd,
        "Recommended_Exit": best_exit,
        "Recommended_Route": " → ".join(best_route),
        "Route_Cost": round(best_distance, 2)
    })

results_df = pd.DataFrame(results)

results_df.to_csv(
    "route_prediction_output.csv",
    index=False
)

print("\nFinal results saved to route_prediction_output.csv")