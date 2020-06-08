import logging


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
    return


def check_data(temp_time, temp_volt):
    if temp_volt  == '':
        return False
    elif temp_time == '':
        return False
    elif temp_time.isnumeric() is False:
        return False
    elif temp_volt.isnumeric() is False:
        return False
    else:
        return True


def read_input(filename):
    with open(filename, 'r') as f:
        temp_line = f.readline()
        while temp_line != " \n":
            temp_time, temp_volt = split_data(temp_line)
            temp_check = check_data(temp_time, temp_volt)
    return


def interface():
    filename = input("Please enter the filename: ")
    ecg_raw_data = read_input(filename)
    ecg_metrics = metrics(ecg_raw_data)
    output_file(ecg_metrics)


if __name__ == '__main__':
    interface()
