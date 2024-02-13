import numpy as np
import pandas as pd
import tqdm
from scipy.interpolate import griddata
import matplotlib.pyplot as plt


def get_bi_cubic(target_time, target_space, data):
    """
    Performs bicubic interpolation to estimate the speed at a specified target time and space,
    using a subset of data points close to these target values.

    :param target_time: The target time for which the speed is to be interpolated.
    :param target_space: The target space for which the speed is to be interpolated.
    :param data: The dataset containing time, space, and speed columns.
    :type target_time: float
    :type target_space: float
    :type data: pandas.DataFrame
    :return: The interpolated speed value at the specified target time and space.
    :rtype: float

    The function filters the input dataset to select points within a specified range of the target time
    (±8 units = ± 2 time standard units) and target space (±0.04 units = ± 2 space standard units). It
    then uses these filtered points to perform cubic interpolation,
    estimating the speed at the specified target time and space. The `griddata` function from SciPy is used for this
    interpolation, with 'cubic' method specified to achieve bicubic interpolation.
    """

    data_small = data[(np.abs(data.t - target_time) <=8) & (np.abs(data.x - target_space) <=0.04)]
    time = data_small['t']
    space = data_small['x']
    speed = data_small['speed']
    interpolated_value = griddata((time, space), speed, (target_time, target_space), method='cubic')
    return interpolated_value

def gen_VT(t0, v_id, large_speed_field, update_rate=1, x0=0.32):
    """
    Generates a vehicle trajectory based on interpolated speeds from a large speed field dataset,
    starting from an initial time and position, and moving forward at a specified update rate.

    :param t0: The initial time from which to start the trajectory, in seconds.
    :param v_id: The vehicle ID for which the trajectory is being generated.
    :param large_speed_field: A DataFrame containing the smooth speed field data with columns 't' for time and 'x' for space.
    :param update_rate: The rate, in seconds, at which the vehicle's position is updated. Defaults to 1 second (1Hz).
    :param x0: The initial position of the vehicle in space. Defaults to 0.32 mile to avoid missing data in the beginning.
    :type t0: float
    :type v_id: int
    :type large_speed_field: pandas.DataFrame
    :type update_rate: float
    :type x0: float
    :return: A list of tuples, each representing a point in the vehicle's trajectory. Each tuple contains
             the time 't', position 'x', speed 'v', and vehicle ID 'v_id'.
    :rtype: list

    The function begins by defining a time range based on the initial time `t0`, then uses bicubic interpolation
    to estimate the initial speed `v0` at the start position `x0`. It iterates through time, updating the vehicle's
    position based on the interpolated speed at each new time and position, until the vehicle reaches a specified
    boundary. The function also refreshes the speed field data every 300 seconds to ensure accurate speed estimations
    throughout the trajectory. The resulting trajectory is a series of (t, x, v, v_id) tuples representing the vehicle's
    path over time.
    """

    start_time = t0 - 30
    end_time = t0 + 900 - 30 # 900 is 900 secnods here, set a ranged_speed_field is to accelerate calculation
    ranged_speed_field = large_speed_field[(large_speed_field.t <= end_time) & (large_speed_field.t > start_time)]
    v0 = float(get_bi_cubic(t0, x0, ranged_speed_field))
    traj = [(t0, x0, v0, v_id)]
    t = t0
    x = x0
    while (x < 4.3):
        speed = float(get_bi_cubic(t, x, ranged_speed_field))
        x = x + update_rate * speed / 3600
        t = round(t + update_rate, 0)
        if ((t - 30) % 300 == 0):
            ranged_speed_field = large_speed_field[
                (large_speed_field.t <= t + 900 - 30) & (large_speed_field.t > t - 30)] # to fix the bug for 22-11-21
        traj.append((t, x, speed, v_id))
    return traj

def gen_all_VT(smooth_speed, frequency, hour, traj_hz=1):
    """
    Generates trajectories for multiple vehicles over a specified period based on smoothed speed data,
    with each vehicle starting its trajectory at regular intervals (frequency) within the period.

    :param smooth_speed: A DataFrame of the smoothed speed data, with columns for time and space indices,
                         raw speed, and interpolated speed.
    :param frequency: The time interval, in seconds, at which new virtual vehicle trajectories are initiated.
    :param hour: The total duration, in hours, for which to generate vehicle trajectories.
    :param traj_hz: The update rate, in seconds, for recalculating each vehicle's position. Defaults to 1Hz.
    :type smooth_speed: pandas.DataFrame
    :type frequency: int
    :type hour: int
    :type traj_hz: int
    :return: A DataFrame containing all generated vehicle trajectories, with columns for time, space, speed, and vehicle ID.
    :rtype: pandas.DataFrame

    The function first prepares the smoothed speed data by adjusting the space values and setting appropriate column names.
    It then iterates over time, starting new vehicle trajectories at intervals defined by `frequency`. Each trajectory is generated
    using the `gen_VT` function, which calculates the vehicle's path based on interpolated speeds from the `smooth_speed` DataFrame.
    The space values are adjusted to match the orientation of the input speed data. All individual vehicle trajectories are then
    concatenated into a single DataFrame, which is returned as the function's output.
    """

    vt_list = []
    smooth_vt = smooth_speed.copy() #hard copy to avoid pollution
    smooth_vt.columns = ['t_index', 'x_index', 'raw_speed', 't', 'x', 'speed']
    smooth_vt['x'] = 63 - smooth_vt['x'] # the raw x is decreasing, transform to have a increasing x-axis
    for time in np.arange(30, 30 + 3600 * hour + 1 - 120, int(frequency)):
        k = int(time / int(frequency))
        vt = pd.DataFrame(gen_VT(time, k, smooth_vt, update_rate = round(1/traj_hz,2)))
        vt.columns = ['time', 'space', 'speed', 'v_id']
        vt['space'] = 63 - vt['space'] # transform it back
        vt_list.append(vt)
    vt_all = pd.concat(vt_list)
    return vt_all
