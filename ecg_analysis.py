import logging
import math
import matplotlib.pyplot as plt
import heartpy as hp
import numpy as np
import json


logging.basicConfig(filename='bad_data.log',
                    filemode='w',
                    level=logging.INFO)


def output_file(metrics, filename):
    """This function writes the output json file for the ECG data

    This function takes the dictionary of ECG metrics and the name
    of the csv file as inputs. The name of the csv file is split
    into a list at the period and the first item of the list is
    put into a string followed by .json to create the filename.
    Using a with statement and a .dump() command the json file is
    written.

    Args:
        metrics (dict): Dictionary containing ECG metrics including
        the time duration, extreme values, number of beats,
        time points of beats, and mean heart rate in bpm.
    """
    logging.info('Creating JSON output file')
    filename_split = filename.split(".")
    file = filename_split[0]
    filename = file + ".json"
    with open(filename, 'x') as out_file:
        json.dump(metrics, out_file)


def group_similar_values(beat_list):
    """This returns a list of time points that represents heart beats

    The input argument beat_list contains a list of time values
    that correspond to voltages that are above half the max voltage.
    The list beat_list has groups of voltages that represent heart beats.
    For each group of times the median time is selected to be the heart
    beat and is appended to the list median_list which is returned and
    used as the list of times when heart beats occur.

    Args:
        beat_list (list): This list contains all times that correspond
        to voltages over one half of the max voltage.

    Returns:
        list : a list of time points representing heart beats
    """
    big_list = [[]]
    x = 0
    for i in range(len(beat_list)):
        diff = beat_list[i] - beat_list[i - 1]
        if diff > 0.1:
            x += 1
            big_list.append([])
        big_list[x].append(beat_list[i])
    median_list = list()
    for i in range(len(big_list)):
        val = math.floor(len(big_list[i])/2)
        median_list.append(big_list[i][val])
    return median_list


def calc_beats(time, volts):
    """This function returns the time points of heart beats by looking
    at the voltage values

    This function takes the time and voltage lists as input. The max voltage
    is stored in the variable maximum by calling the function
    calc_voltage_extremes() and selecting the max value. A for
    loop loops through the voltage values and stores the time points
    where the voltage is greater than half of the max voltage. This list
    of times is sent to the function group_similar_values() which
    returns the list of times corresponding to heart beats.

    Args:
        time (list): list of time values for the ECG data
        volts (list): list of ECG voltage magnitudes

    Returns:
        list : list of time values corresponding to heart beats
    """
    logging.info('Finding the times that each '
                 'heart beat occurred')
    beat_list = list()
    extremes = calc_voltage_extremes(volts)
    maximum = extremes[1]
    for i in range(len(volts)):
        if volts[i] > (maximum / 2):
            beat_list.append(time[i])
    beat_list = group_similar_values(beat_list)
    return beat_list


def calc_mean_hr_bpm(time, volts):
    """This function returns the average heart rate over the ECG data

    The two lists time and volts are used as input parameters and are sent
    to the function calc_beats which returns the list of time points
    corresponding to heart beats. Using a for loop the time between beats
    are stored in the list hr_list. The inverse of the time between the
    beats is multiplied by 60 to convert beats per second to beats per
    minute. The average of this list of heart rates is calculated by
    finding the mean of the heart rates.

    Args:
        time (list): list of time values for the ECG data
        volts (list): list of ECG voltage magnitudes

    Returns:
        float : mean heart rate over the ECG data
    """
    logging.info('Calculating the mean heart rate '
                 'in beats-per-minute')
    beat_list = calc_beats(time, volts)
    hr_list = list()
    for i in range(len(beat_list)):
        if i > 0:
            diff = beat_list[i] - beat_list[i-1]
            hr_list.append(diff)
    ave_hr = [(1/x)*60 for x in hr_list]
    ave = np.mean(ave_hr)
    return ave


def calc_num_beats(time, volt):
    """This returns the number of heart beats over the ECG data.

    This function calls the function calc_beats to get the list
    of heart beats for the ECG data. The length of this list
    returned which is the number of beats in the list.

    Args:
        time (list): list of time values for the ECG data
        volts (list): list of ECG voltage magnitudes

    Returns:
        int : the number of beats in the ECG data
    """
    logging.info('Calculating the number of heart beats')
    beats = calc_beats(time, volt)
    return len(beats)


def calc_voltage_extremes(volt):
    """This function calculates the extreme values in the ECG data.

    This functon takes the volt list as input which is the magnitude
    of the ECG data, and finds the extreme values using the max() and
    min() values. The max and min values are returned as a tuple.

    Args:
        volts (list): list of ECG voltage magnitudes

    Returns:
        tuple: (min, max)
    """
    logging.info('Finding max and min ECG values')
    maximum = max(volt)
    minimum = min(volt)
    ans = (minimum, maximum)
    return ans


def calc_duration(time):
    """This calculates the time duration of the ECG data.

    The time duration is found by subtracting the first time
    value from the last time value.

    Args:
        time (list): list of time values for the ECG data

    Returns:
        float : duration of ECG data in seconds
    """
    logging.info('Calculating ECG duration')
    first = time[0]
    last = time[-1]
    return last - first


def filter_data(time, raw_volt):
    """This function filters out noise below 10 Hz and above 50Hz

    This filter takes the time and raw_volt data as input and
    filters out noises below 10 Hz and above 50 Hz using the heartpy
    function filter_signal. See documentation on the filter_signal function
    at: https://python-heart-rate-analysis-toolkit.readthedocs.io/en/
    latest/_modules/heartpy/filtering.html

    Args:
        time (list): list of time values for the ECG data
        volts (list): list of ECG voltage magnitudes

    Returns:
        list : the filtered ECG voltage values
    """
    logging.info('Filtering Data')
    sample_rate = 1 / (time[1] - time[0])
    volt = hp.filter_signal(raw_volt, [5, 20], sample_rate, 2, 'bandpass')
    return volt


def make_dictionary(duration, voltage_extremes, num_beats, mean_hr_bpm, beats):
    """This function returns a dictionary of ECG metric data

    This function makes a dictionary containing all of the ECG metric data,
    which is passed into the function as the function's input parameters.

    Args:
        duration (float): the time duration of the ECG data
        voltage_extremes (tuple): a tuple containing the min and max voltages
        num_beats (int): the number of heart beats in the ECG data
        mean_hr_bpm (float): the mean heart rate in beats per minutes
        beats (list): the list of times corresponding to heart beats

    Returns:
        dictionary : dictionary containing ecg metrics
    """
    metrics = {"duration": duration, "voltage_extremes": voltage_extremes,
               "num_beats": num_beats, "mean_hr_bpm": mean_hr_bpm,
               "beats": beats}
    return metrics


def plot_data(time, volt, filename):
    """This function plots the ECG data for a file

    This function takes three arguments as inputs: time, volt,
    and filename. It uses matplotlib.pyplot to plot the time and
    voltage pairs and uses the filename as the title.

    Args:
        time (list): list of time values for the ECG data
        volts (list): list of ECG voltage magnitudes
        filename (str): the string of the filename to be opened
    """
    plt.plot(time, volt)
    plt.title(filename)
    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (mV)")
    plt.show()


def calc_metrics(time, volt, filename):
    """This function calls the functions necessary to calculate the
    ECG metrics

    This function takes the time and volt lists as inputs and calls several
    functions to return a dictionary of ECG metrics. First filter_data() is
    called to get the voltage data without the high and low noise. Then the
    duration is calculated using the function calc_duration(), the voltage
    extremes are calculated by calling the function calc_voltage_extremes(),
    the number of beats is calculated by calling the function
    calc_num_beats(), the average heart rate is calculated by calling the
    function calc_mean_hr_bpm(), the list of times corresponding to heart
    beats is calculated by calling the function calc_beats(). All of the
    metric data is put into a dictionare by calling the function
    make_dictionary.

    Args:
        time (list): list of time values for the ECG data
        volts (list): list of ECG voltage magnitudes

    Returns:
        dictionary : dictionary containing ecg metrics
    """
    logging.info('Beginning analysis of ECG data.')
    volt = filter_data(time, volt)
    duration = calc_duration(time)
    voltage_extremes = calc_voltage_extremes(volt)
    num_beats = calc_num_beats(time, volt)
    mean_hr_bpm = calc_mean_hr_bpm(time, volt)
    beats = calc_beats(time, volt)
    plot_data(time, volt, filename)
    metrics = make_dictionary(duration, voltage_extremes, num_beats,
                              mean_hr_bpm, beats)
    return metrics


def split_data(temp_line):
    """This function recieves a line of input from the
    data file and returns the data after it is isolated

    ECG test data is read into the software using the function
    read_input() which sends the data line by line to this function
    to clean it up. The lines of data are stripped and split at the comma
    into time and voltage values. If a value is missing, then a blank string
    is returned.

    Args:
        temp_line (str): a string that contains a line of ECG data

    Returns:
        time (list): list of time values for the ECG data
        volts (list): list of ECG voltage magnitudes
    """
    temp_line = temp_line.strip("\n")
    temp_list = temp_line.split(",")
    time = temp_list[0]
    time = time.strip(" ")
    if len(temp_list) == 2:
        volt = temp_list[1]
        volt = volt.strip(" ")
    else:
        volt = ''
    return time, volt


def is_a_number(number):
    """This function returns whether a string contains a number

    This function uses a try-except statement to check whether a
    string is numeric. It does so by trying to take the float of
    a string and returning True if it is successful and False if
    unsuccessful.

    Args:
        number (str): a string containing data from the .csv file

    Returns:
        bool: True or False depending on if the string is numeric
    """
    try:
        float(number)
    except ValueError:
        return False
    return True


def check_data(temp_time, temp_volt):
    """This function checks whether the .csv data can be used for analysis

    This function takes two string arguments, one of the string in the time
    location in the csv file and one string that was in the voltage location
    in the csv file. This function returns False if either of the strings are
    empty, non-numeric, or NaN.

    Args:
        temp_time (str): a string of what should be the time data
        temp_volt (str): a string of what should be the voltage data
    """
    if temp_volt == '':
        return False
    elif temp_time == '':
        return False
    elif is_a_number(temp_time) is False:
        return False
    elif is_a_number(temp_volt) is False:
        return False
    elif math.isnan(float(temp_time)) is True:
        return False
    elif math.isnan(float(temp_volt)) is True:
        return False
    else:
        return True


def log_if_bad_data(temp_check):
    """This function logs an error if there is a bad data point.

    This function uses the result of temp_check to see if a data point
    is usable in the ECG analysis. If the data point prompts check_data()
    to return False, then it will log it as a bad data point.

    Args:
        temp_check (bool): True or False depending on whether the data
        can be used
    """
    if temp_check is False:
        logging.error('Bad data point, '
                      'skipping to next line')
    return


def log_if_data_too_high(volt):
    """This function logs a warning if there are voltages outside of the
    normal operating range.

    This function takes the volt list as input and finds the max and min of
    the list. If the max is above 300 mV or the min is under -300 mV then a
    warning is logged.

    Args:
        volt (list): list of ECG voltage magnitudes
    """
    maximum = max(volt)
    minimum = min(volt)
    if maximum > 300 or minimum < -300:
        logging.warning("This file contains a value outside the "
                        "normal operating range of +/- 300 mV.")
    return


def read_input(filename):
    """This function reads the data from an input file
    This function uses a with statement to open a file and a while loop to
    go through the entire function. Each line is read, and the contents of
    the line are cleaned and turned into time and voltage values where they
    are then stored in the time and volt lists.

    Args:
        filename (str): the string of the filename to be opened

    Returns:
        list : a list of time values
        list : a list of voltages
    """
    time = list()
    volt = list()
    with open(filename, 'r') as f:
        temp_line = f.readline()
        while temp_line != "":
            temp_time, temp_volt = split_data(temp_line)
            temp_check = check_data(temp_time, temp_volt)
            log_if_bad_data(temp_check)
            if temp_check is True:
                time.append(float(temp_time))
                volt.append(float(temp_volt))
            temp_line = f.readline()
    log_if_data_too_high(volt)
    return time, volt


def interface():
    """This function calls the functions that read the data and write json
    files

    This funcion is called when the module is ran. It requests that the
    user type in the filename that stores the ECG data. This function
    then calls the function read_input() that reads the data inside the
    given filename and creates a dictionary of ECG metrics. This dictionary
    of metrics is then sent to the function output_file() which creates the
    json to store the data.
    """
    filename = input("Please enter the filename: ")
    ecg_time, ecg_volt = read_input(filename)
    metrics = calc_metrics(ecg_time, ecg_volt, filename)
    output_file(metrics, filename)


if __name__ == '__main__':
    interface()
