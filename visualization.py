import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.style as mplstyle
import datetime
import warnings
import os


def visualize_heatmap(speed_data, starttime, endtime,
                      fig_width=8, fig_height=8, minor_xtick=1800,
                      min_milemarker=58.7, testbed_mile=4, 
                      save_filepath=None):
    """
    Visualizes a heatmap of speed data over time and mile markers.
    Note: this function requires smoothed speed fields from `macro_data_processing.py`.

    Parameters:
    -----------
    speed_data : DataFrame
        A DataFrame containing speed data with columns 'time', 'milemarker', and 'speed'.
    starttime : int
        The starting time in seconds in Unix time.
    endtime : int
        The ending time in seconds in Unix time.
    fig_width : int, optional
        The width of the generated figure in inches. Default is 8.
    fig_height : int, optional
        The height of the generated figure in inches. Default is 8.
    minor_xtick : int, optional
        The interval between minor x-axis ticks in seconds. Default is 150.
    save_filepath : file path name, optional
        Absolute path name (type .png or .pdf) for saving the figure (optional); if None, does not save.

    Returns:
    --------
    None
        This function generates and displays a heatmap plot but does not return any value.

    Notes:
    ------
    This function uses matplotlib to create a heatmap visualization of speed data along 
    mile markers and time intervals. It displays speed data as a colormap with color-coded 
    speed values, and mile markers and time intervals are marked on the axes. 

    Example:
    --------
    visualize_heatmap(speed_data, starttime=0, endtime=3600, dx=0.01, dt=60)

    This example will create a heatmap plot of `speed_data` with specified parameters.
    """
    # Use a portion of the Jet colormap for a custom green-to-red colormap
    jet = plt.cm.jet
    colors = [jet(x) for x in np.linspace(1, 0.5, 256)]
    green_to_red = LinearSegmentedColormap.from_list('GreenToRed', colors, N=256)
    # Create a new figure with a custom font.
    plt.figure(figsize=(fig_width, fig_height))
    plt.rc('font', family='serif', size=30)
    # Create a scatter plot of all of the spatiotemporal data points.
    sc = plt.scatter(speed_data.time, speed_data.milemarker, c=speed_data.speed, 
                     cmap=green_to_red, vmin=0, vmax=80, marker='s', s=5)
    # Customize the axes ticks and labels for milemarkers on y-axis and timestamp on x-axis.
    start_time = datetime.datetime.strptime(datetime.datetime.fromtimestamp(starttime).strftime("%H:%M"), "%H:%M")
    ticks = list(range(0, endtime-starttime + 1, minor_xtick))
    plt.ylabel('Mile Marker')
    plt.xlabel(datetime.datetime.fromtimestamp(starttime).strftime("%Y-%m-%d"))
    xlabels = [(start_time + datetime.timedelta(seconds=tick)).strftime("%H:%M") for tick in ticks]
    plt.xticks(ticks, labels=xlabels, rotation=45, fontsize=16)
    plt.xlim(0, (endtime-starttime))
    plt.ylim(min_milemarker, min_milemarker+testbed_mile)
    plt.gca().invert_yaxis()
    # Add a grid and colorbar.
    plt.grid(which='both', linewidth=2, linestyle='--')
    plt.colorbar(sc, pad=0.01).set_label('Speed (mph)', rotation=90, labelpad=20)
    # If a file path was defined for this plot, save the figure.
    if save_filepath is not None:
        if os.path.splitext(save_filepath)[1] not in ('.png', '.pdf'):
            warnings.warn("Invalid file type for saving; must be .png or .pdf.")
        plt.savefig(save_filepath, dpi=300, bbox_inches='tight')
    plt.show()


def visualize_heatmap_vt(speed_data, vt, starttime, endtime, 
                         fig_width=8, fig_height=8, minor_xtick=1800,
                         colors=None, cmap='green_to_red',
                         min_milemarker=58.7, testbed_mile=4, 
                         save_filepath=None):
    """
    Visualizes a heatmap of speed data over time and mile markers, along with virtual trajectories overlaid.
    Note: this function requires smoothed speed fields from `macro_data_processing.py`.

    Parameters:
    -----------
    speed_data : DataFrame
        A DataFrame containing speed data with columns 'time', 'milemarker', and 'speed'.
    vt: DataFrame
        A DataFrame containing virtual trajectory data with columns 'time', 'space'.
    starttime : int
        The starting time in seconds in Unix time.
    endtime : int
        The ending time in seconds in Unix time.
    fig_width : int, optional
        The width of the generated figure in inches. Default is 8.
    fig_height : int, optional
        The height of the generated figure in inches. Default is 8.
    minor_xtick : int, optional
        The interval between minor x-axis ticks in seconds. Default is 150.
    save_filepath : file path name, optional
        Absolute path name (type .png or .pdf) for saving the figure (optional); if None, does not save.

    Returns:
    --------
    None
        This function generates and displays a heatmap plot but does not return any value.

    Notes:
    ------
    This function uses matplotlib to create a heatmap visualization of speed data along 
    mile markers and time intervals. It displays speed data as a colormap with color-coded 
    speed values, and mile markers and time intervals are marked on the axes. 

    Example:
    --------
    visualize_heatmap(speed_data, starttime=0, endtime=3600)

    This example will create a heatmap plot of `speed_data` with specified parameters.
    """
    # Use a portion of the Jet colormap for a custom green-to-red colormap
    jet = plt.cm.jet
    colors = [jet(x) for x in np.linspace(1, 0.5, 256)]
    green_to_red = LinearSegmentedColormap.from_list('GreenToRed', colors, N=256)
    # Create a new figure with a custom font.
    plt.figure(figsize=(fig_width, fig_height))
    plt.rc('font', family='serif', size=30)
    # Create a scatter plot of all of the spatiotemporal data points.
    sc = plt.scatter(speed_data.time, speed_data.milemarker, c=speed_data.speed, 
                     cmap=green_to_red, vmin=0, vmax=80, marker='s', s=5)
    # Overlay the virtual trajectories.
    plt.scatter(vt.time, vt.space, color='k',s=1)
    # Customize the axes ticks and labels for milemarkers on y-axis and timestamp on x-axis.
    start_time = datetime.datetime.strptime(datetime.datetime.fromtimestamp(starttime).strftime("%H:%M"), "%H:%M")
    ticks = list(range(0, endtime-starttime + 1, minor_xtick))
    plt.ylabel('Mile Marker')
    plt.xlabel(datetime.datetime.fromtimestamp(starttime).strftime("%Y-%m-%d"))
    xlabels = [(start_time + datetime.timedelta(seconds=tick)).strftime("%H:%M") for tick in ticks]
    plt.xticks(ticks, labels=xlabels, rotation=45, fontsize=16)
    plt.xlim(0, (endtime-starttime))
    plt.ylim(min_milemarker, min_milemarker+testbed_mile)
    plt.gca().invert_yaxis()
    # Add a grid and colorbar.
    plt.grid(which='both', linewidth=2, linestyle='--')
    plt.colorbar(sc, pad=0.01).set_label('Speed (mph)', rotation=90, labelpad=20)
    # If a file path was defined for this plot, save the figure.
    if save_filepath is not None:
        if os.path.splitext(save_filepath)[1] not in ('.png', '.pdf'):
            warnings.warn("Invalid file type for saving; must be .png or .pdf.")
        plt.savefig(save_filepath, dpi=300, bbox_inches='tight')
    plt.show()
