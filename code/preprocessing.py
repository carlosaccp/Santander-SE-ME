import pandas as pd
import numpy as np

station_data = pd.read_csv("../data/santander_locations.csv")


class OptimizationError(RuntimeError):
    """Called when optimizer does not converge."""
    pass

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

nweeks = 12
bike_data = pd.read_csv("../data/processed_df.csv", index_col=0)
x = bike_data.min()["start_time"]
t_min = (x // 86400) * 86400
end_T = t_min + 16*7*24*3600
train_time = nweeks*7*24*60
bike_data["start_time"] = (bike_data["start_time"] - t_min) / 60
bike_data["end_time"] = (bike_data["end_time"] - t_min) / 60
bike_data["start_time"] = bike_data["start_time"] \
    + np.random.rand(*bike_data["start_time"].shape)
bike_data["end_time"] = bike_data["end_time"] \
    + np.random.rand(*bike_data["end_time"].shape)
bike_data["duration"] = bike_data.end_time - bike_data.start_time
bike_data = bike_data.sort_values(by=["start_time"])
train_bike_data = bike_data[bike_data.start_time <= train_time]
test_bike_data = bike_data[bike_data.start_time > train_time]
train_sorted_stations_start = []
for st_id in train_bike_data.start_id.sort_values().unique():
    train_sorted_stations_start.append(
        train_bike_data[train_bike_data.start_id == st_id]
        )
test_sorted_stations = []
for st_id in test_bike_data.start_id.sort_values().unique():
    test_sorted_stations.append(
        test_bike_data[test_bike_data.start_id == st_id]
        )
rates_dict = {}
for station in test_sorted_stations:
    time_elapsed = station.start_time.to_numpy()[-1] \
        - station.start_time.to_numpy()[0]
    n_events = test_sorted_stations[0].size
    rate = n_events / time_elapsed

    rates_dict[station.start_id.unique()[0]] = rate
rates_dict_train = {}
for station in train_sorted_stations_start:
    time_elapsed = station.start_time.to_numpy()[-1] \
        - station.start_time.to_numpy()[0]
    n_events = train_sorted_stations_start[0].size
    rate = n_events / time_elapsed
    rates_dict_train[station.start_id.unique()[0]] = rate
station_array = list(rates_dict.keys())


def ecdf(data):
    # https://cmdlinetips.com/2019/05/empirical-cumulative-distribution-function-ecdf-in-python/
    """ Compute ECDF """
    x = np.sort(data)
    n = x.size
    y = np.arange(1, n+1) / n
    return(x, y)


end_times_per_station_sorted = {}
for id in bike_data.end_id.unique():
    unsorted_station_end_time = train_bike_data[train_bike_data.end_id == id]
    sorted_station_end_time = unsorted_station_end_time.sort_values(
        by=["end_time"])
    end_times_per_station_sorted[id] = sorted_station_end_time.\
        end_time.to_numpy()

start_times_per_station_sorted = {}
for id in bike_data.start_id.unique():
    unsorted_station_start_time = train_bike_data[train_bike_data.start_id == id]
    sorted_station_start_time = unsorted_station_start_time.sort_values(
        by=["start_time"])
    start_times_per_station_sorted[id] = sorted_station_start_time.\
        start_time.to_numpy()

test_end_times_per_station_sorted = {}
for id in bike_data.end_id.unique():
    test_unsorted_station_end_time = test_bike_data[test_bike_data.end_id == id]
    test_sorted_station_end_time = test_unsorted_station_end_time.sort_values(
        by=["end_time"])
    test_end_times_per_station_sorted[id] = test_sorted_station_end_time.\
        end_time.to_numpy()

test_start_times_per_station_sorted = {}
for id in bike_data.start_id.unique():
    test_unsorted_station_start_time = test_bike_data[test_bike_data.start_id == id]
    test_sorted_station_start_time = test_unsorted_station_start_time.sort_values(
        by=["start_time"])
    test_start_times_per_station_sorted[id] = test_sorted_station_start_time.\
        start_time.to_numpy()

t_per_station = start_times_per_station_sorted
t_prime_per_station = end_times_per_station_sorted
test_t_per_station = test_start_times_per_station_sorted
test_t_prime_per_station = test_end_times_per_station_sorted
train_sorted_start_ids = np.sort(train_bike_data.start_id.unique())
test_sorted_start_ids = np.array(list(set(train_bike_data.start_id.unique()).intersection(set(test_bike_data.start_id.unique()))))