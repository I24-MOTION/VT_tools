import numpy as np
import pandas as pd
from tqdm import tqdm


"""
To know more details about the ASM method, refer to:

[1] Treiber, M., & Helbing, D. (2003). An adaptive smoothing method for traffic state 
identification from incomplete information. In Interface and transport dynamics: 
Computational Modelling (pp. 343-360). Berlin, Heidelberg: Springer Berlin Heidelberg.

"""

def beta_free_flow(x, t, x_s, t_s, x_win, t_win, c_free=-43):
    """
    Given a space and time with the center space and time, 
    calculate the free-flow weight for an observation point within the smoothing kernel.
    space unit: mile
    time unit: second 

    :param x: The target smoothing point in space.
    :param t: The target smoothing point in time.
    :param x_s: The observation point (space) within the smoothing kernel.
    :param t_s: The observation point (time) within the smoothing kernel.
    :param x_win: The window size in space for the smoothing kernel.
    :param t_win: The window size in time for the smoothing kernel.
    :param c_free: The characteristic free flow speed, usually set up at about 80% of the desired velocity V_0 on empty roads. Defaults to -43.
    :type x: float
    :type t: float
    :type x_s: float
    :type t_s: float
    :type x_win: float
    :type t_win: float
    :type c_free: float
    :return: Weight for the point (x_s, t_s).
    :rtype: float

    The function calculates the weight by considering the difference in space and time between the target point and the observation point,
     adjusted by the characteristic free flow speed.
    """

    dt = t-t_s- 3600*(x-x_s)/c_free
    dx = x-x_s
    return np.exp(-(2*np.abs(dx)/x_win + 2*np.abs(dt)/t_win))


def beta_cong_flow(x, t, x_s, t_s, x_win, t_win, c_cong=13):
    """
    Given a space and time with the center space and time, 
    calculate the congested-flow weight for an observation point within the smoothing kernel.
    space unit: mile
    time unit: second 

    :param x: The target smoothing point in space.
    :param t: The target smoothing point in time.
    :param x_s: The observation point (space) within the smoothing kernel.
    :param t_s: The observation point (time) within the smoothing kernel.
    :param x_win: The window size in space for the smoothing kernel.
    :param t_win: The window size in time for the smoothing kernel.
    :param c_free: The characteristic congested speed, i.e. the wave propagation speed. Defaults to 13.
    :type x: float
    :type t: float
    :type x_s: float
    :type t_s: float
    :type x_win: float
    :type t_win: float
    :type c_free: float
    :return: Weight for the point (x_s, t_s).
    :rtype: float

    The function calculates the weight by considering the difference in space and time between the target point and the observation point,
     adjusted by the characteristic free flow speed.
    """
    dt = t-t_s- 3600*(x-x_s)/c_cong
    dx = x-x_s
    return np.exp(-(2*np.abs(dx)/x_win + 2*np.abs(dt)/t_win))


def EGTF(x, t, smooth_x_window, smooth_t_window, speed_raw_df):
    """
    Calculate the Enhanced Generalised Treiber–Helbing Filter (EGTF) speed at a given point in space and time,
    using a smoothing window for both space and time dimensions and raw speed data.

    :param x: The target point in space where the smoothed speed is to be calculated.
    :param t: The target point in time where the smoothed speed is to be calculated.
    :param smooth_x_window: The window size in space for the smoothing kernel.
    :param smooth_t_window: The window size in time for the smoothing kernel.
    :param speed_raw_df: A DataFrame containing raw speed data with columns 't' for time, 'x' for space, and 'speed' for the observed speed.
    :type x: float
    :type t: float
    :type smooth_x_window: float
    :type smooth_t_window: float
    :type speed_raw_df: pandas.DataFrame with columns ['t','x','speed']
    :return: The calculated EGTF speed at the given point in space and time.
    :rtype: float

    The function filters the raw speed data within the given spatial and temporal windows centered around the target point (x, t).
    It then calculates weights for free-flow and congested conditions using the `beta_free_flow` and `beta_cong_flow` functions
    for each data point within the window. The EGTF speed is a weighted average of the observed speeds, where the weights
    are derived from the likelihood of free-flow and congested traffic conditions. The final speed is adjusted by a weighting
    function based on the tanh of the difference between a threshold speed and the minimum of the calculated free-flow and congested speeds.
    """

    speed = speed_raw_df[(np.abs(speed_raw_df.t - t)<=(smooth_t_window/2)) & (np.abs(speed_raw_df.x - x)<=(smooth_x_window/2))]
    speed = speed.copy()
    EGTF_v_free = 80
    EGTF_v_cong = 80
    # Now apply your functions
    speed['beta_free'] = speed.apply(lambda v: beta_free_flow(x, t, v.x, v.t, smooth_x_window, smooth_t_window), axis=1)
    speed['beta_cong'] = speed.apply(lambda v: beta_cong_flow(x, t, v.x, v.t, smooth_x_window, smooth_t_window), axis=1)
    if((sum(speed.beta_free)!=0) & (sum(speed.beta_cong)!=0)):
        EGTF_v_free = sum(speed.beta_free * speed.speed) / sum(speed.beta_free)
        EGTF_v_cong = sum(speed.beta_cong * speed.speed) / sum(speed.beta_cong)
    v = min(EGTF_v_free,EGTF_v_cong)
    tanh_term = np.tanh((36-v) / 12.43)
    w = 0.5*(1+tanh_term)
    return w*EGTF_v_cong + (1-w)*EGTF_v_free


def smooth_raw_data(speed_raw, dx, dt, smooth_x_window=0.15, smooth_t_window=36):
    """
    Preprocesses raw speed data and calculates the Enhanced Generalised Treiber–Helbing Filter (EGTF) speed
    for each data point using specified spatial and temporal smoothing windows.

    :param speed_raw: The raw speed data as a DataFrame from the macroscopic speed calculation with three columns time, space and speed.
    :param dx: The spatial resolution of the data, i.e., the distance between consecutive points in space. 
               It should be set consitent as Edie's box.
    :param dt: The temporal resolution of the data, i.e., the time difference between consecutive points in time.
               It should be set consitent as Edie's box.
    :param smooth_x_window: The window size in space for the smoothing operation, default is 0.15 mile.
    :param smooth_t_window: The window size in time for the smoothing operation, default is 36 seconds.
    :type speed_raw: pandas.DataFrame
    :type dx: float
    :type dt: float
    :type smooth_x_window: float
    :type smooth_t_window: float
    :return: A DataFrame containing the original time and space indices, raw speed, and calculated EGTF speed.
    :rtype: pandas.DataFrame

    The function first converts the raw time and space indices into actual time and space values using `dt` and `dx`, respectively.
    It then calculates the EGTF speed for each data point within the specified spatial and temporal smoothing windows.
    The progress of this calculation is tracked using a progress bar from `tqdm`. Finally, it returns a DataFrame with the
    original indices, calculated time and space values, raw speed, and the EGTF speed for each data point.
    """

    EGTF_speed = pd.DataFrame(speed_raw)
    EGTF_speed.columns=['t_index','x_index','speed']
    EGTF_speed['t'] = dt*EGTF_speed['t_index']
    EGTF_speed['x'] = dx*EGTF_speed['x_index'] + 58.7
    speed_raw_df  = EGTF_speed.dropna().copy()
    tqdm.pandas(desc="Processing EGTF")
    EGTF_speed['EGTF'] = EGTF_speed.progress_apply(lambda v: EGTF(v.x, v.t, smooth_x_window,smooth_t_window,speed_raw_df), axis=1)
    EGTF_speed.columns = ['t','x','raw_speed','time','milemarker','speed']
    return EGTF_speed


