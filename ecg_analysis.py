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
    is stored in the variable maximum by calling the function calc_voltage_extremes()
    and selecting the max value. A for loop loops through the voltage values and
    stores the time points where the voltage is greater than half of the max
    voltage. This list of times is sent to the function group_similar_values() which
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
    to the function calc_beats which returns the list of time points corresponding
    to heart beats. Using a for loop the time between beats are stored in the
    list hr_list. The inverse of the time between the beats is multiplied by
    60 to convert beats per second to beats per minute. The average of this
    list of heart rates is calculated by finding the mean of the heart rates.
    
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
    logging.info('Finding max and min ECG values')
    maximum = max(volt)
    minimum = min(volt)
    ans = (minimum, maximum)
    return ans


def calc_duration(time):
    logging.info('Calculating ECG duration')
    first = time[0]
    last = time[-1]
    return last - first


def filter_data(time, raw_volt):
    logging.info('Filtering Data')
    sample_rate = 1 / (time[1] - time[0])
    volt = hp.filter_signal(raw_volt, [5, 20], sample_rate, 2, 'bandpass')
    return volt


def make_dictionary(duration, voltage_extremes, num_beats, mean_hr_bpm, beats):
    metrics = {"duration": duration, "voltage_extremes": voltage_extremes,
               "num_beats": num_beats, "mean_hr_bpm": mean_hr_bpm,
               "beats": beats}
    return metrics


def calc_metrics(time, volt):
    logging.info('Beginning analysis of ECG data.')
    volt = filter_data(time, volt)
    duration = calc_duration(time)
    voltage_extremes = calc_voltage_extremes(volt)
    num_beats = calc_num_beats(time, volt)
    mean_hr_bpm = calc_mean_hr_bpm(time, volt)
    beats = calc_beats(time, volt)
    metrics = make_dictionary(duration, voltage_extremes, num_beats,
                              mean_hr_bpm, beats)
    return metrics


def split_data(temp_line):
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
    try:
        float(number)
    except ValueError:
        return False
    return True


def check_data(temp_time, temp_volt):
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
    if temp_check is False:
        logging.error('Bad data point, '
                      'skipping to next line')
    return


def log_if_data_too_high(volt):
    maximum = max(volt)
    minimum = min(volt)
    if maximum > 300 or minimum < -300:
        logging.warning("This file contains a value outside the "
                        "normal operating range of +/- 300 mV.")
    return


def read_input(filename):
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
    filename = input("Please enter the filename: ")
    ecg_time, ecg_volt = read_input(filename)
    metrics = calc_metrics(ecg_time, ecg_volt)
    output_file(metrics, filename)


if __name__ == '__main__':
    interface()
