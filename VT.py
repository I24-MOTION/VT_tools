import numpy as np
import pandas as pd
import tqdm
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
def get_bi_cubic(target_time, target_space,data):
# Extract necessary columns
    data_small = data[(np.abs(data.t - target_time) <=8) & (np.abs(data.x - target_space) <=0.04)]
    time = data_small['t']
    space = data_small['x']
    speed = data_small['speed']
    interpolated_value = griddata((time, space), speed, (target_time, target_space), method='cubic')
#         error_message = None
    return interpolated_value

def gen_VT(t0,v_id,large_speed_field,update_rate = 1, x0=0.32):
    start_time = t0 - 30
    end_time = t0 + 900 - 30
    #     print(t0,x0)
    ranged_speed_field = large_speed_field[(large_speed_field.t <= end_time) & (large_speed_field.t > start_time)]
    v0 = float(get_bi_cubic(t0, x0, ranged_speed_field))
    #     print(t0,x0)
    traj = [(t0, x0, v0, v_id)]
    t = t0
    x = x0
    while (x < 4.3):
        speed = float(get_bi_cubic(t, x, ranged_speed_field))
        x = x + update_rate * speed / 3600
        t = round(t + update_rate, 0)
        if ((t - 30) % 300 == 0):
            ranged_speed_field = large_speed_field[
                (large_speed_field.t <= t + 900 - 30) & (large_speed_field.t > t - 30)]
        traj.append((t, x, speed, v_id))
    return traj

def gen_all_VT(smooth_speed, frequency, hour):
    vt_list = []
    smooth_vt = smooth_speed.copy()
    smooth_vt.columns = ['t_index', 'x_index', 'raw_speed', 't', 'x', 'speed']
    smooth_vt['x'] = 63 - smooth_vt['x']
    for time in np.arange(30, 30 + 3600 * hour + 1 - 120, int(frequency)):
        k = int(time / int(frequency))
        vt = pd.DataFrame(gen_VT(time, k, smooth_vt))
        vt.columns = ['time', 'space', 'speed', 'v_id']
        vt['space'] = 63 - vt['space']
        vt_list.append(vt)
    vt_all = pd.concat(vt_list)
    return vt_all