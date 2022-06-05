import pandas as pd
import numpy as np

station_data = pd.read_csv("../data/santander_locations.csv")


class StationIdError(IndexError):
    """Called when we try and read a non-existing station id."""
    pass


def get_station_name(in_id):
    """Get station name from bike_data for a given id."""
    try:
        return station_data[
            station_data["Station.Id"] == in_id].StationName.iloc[0]
    except IndexError:
        StationIdError("No station matching input ID")


bike_data = pd.read_csv("../data/processed_df.csv", index_col=0)
x = bike_data.min()["start_time"]
t_min = (x // 86400) * 86400
bike_data["start_time"] = (bike_data["start_time"] - t_min) / 60
bike_data["end_time"] = (bike_data["end_time"] - t_min) / 60
bike_data["start_time"] = bike_data["start_time"] \
    + np.random.rand(*bike_data["start_time"].shape)
bike_data["end_time"] = bike_data["end_time"] \
    + np.random.rand(*bike_data["end_time"].shape)
bike_data["duration"] = bike_data.end_time - bike_data.start_time
bike_data = bike_data.sort_values(by=["start_time"])

train_time = 12*7*24*60
train_bike_data = bike_data[bike_data.start_time <= train_time]
train_sorted_stations = []
for st_id in train_bike_data.start_id.sort_values().unique():
    train_sorted_stations.append(
        train_bike_data[train_bike_data.start_id == st_id]
        )
rates_dict = {}
for station in train_sorted_stations:
    time_elapsed = station.start_time.to_numpy()[-1] \
        - station.start_time.to_numpy()[0]
    n_events = train_sorted_stations[0].size
    rate = n_events / time_elapsed

    rates_dict[station.start_id.unique()[0]] = rate
