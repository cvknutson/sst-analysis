import netCDF4 as nc
import numpy as np
import datetime

# reading in a netCDF file
def read_latest_sst(filename):
    with nc.Dataset(filename) as ds:
        sst = ds.variables["sst"]
        latest_sst = sst[-1, :, :]
        return np.array(latest_sst)

def read_sst(filename):
    with nc.Dataset(filename) as ds:
        sst = ds.variables["sst"][:]      # shape (time, lat, lon)
        lats = ds.variables["lat"][:]     # shape (lat)
        lons = ds.variables["lon"][:]     # shape (lon)
        times = ds.variables["time"][:]   # shape (time)
    
    return sst, lats, lons, times

def extract_timeseries(sst, lats, lons, lat, lon):
    # Find the nearest latitude and longitude indices
    lat_idx = np.argmin(np.abs(lats - lat))
    lon_idx = np.argmin(np.abs(lons - lon))
    timeseries = sst[:, lat_idx, lon_idx]
    return timeseries

def load_time(filename):
    with nc.Dataset(filename) as ds:
        time_var = ds.variables["time"][:]  # days since 1891-01-01
        base_date = datetime.datetime(1891, 1, 1)
        datetime_vec = [base_date + datetime.timedelta(days=float(t)) for t in time_var]
    return np.array(datetime_vec)