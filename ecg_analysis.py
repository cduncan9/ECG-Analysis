import logging
import math
import matplotlib.pyplot as plt


logging.basicConfig(filename='bad_data.log',
                    level=logging.INFO)


def output_file(data):
    pass


def metrics(raw_data):
    return


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


def read_input(filename):
    time = list()
    volt = list()
    with open(filename, 'r') as f:
        temp_line = f.readline()
        while temp_line != "":
            temp_time, temp_volt = split_data(temp_line)
            temp_check = check_data(temp_time, temp_volt)
            if temp_check is True:
                temp_time = float(temp_time)
                time.append(temp_time)
                temp_volt = float(temp_volt)
                volt.append(temp_volt)
            else:
                logging.error('Bad data point,'
                              'skipping to next line')
            temp_line = f.readline()
    return time, volt


def interface():
    filename = input("Please enter the filename: ")
    ecg_time, ecg_volt = read_input(filename)
    ecg_metrics = metrics(ecg_time, ecg_volt)
    output_file(ecg_metrics)


if __name__ == '__main__':
    interface()
