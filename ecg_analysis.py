def output_file(data):
    pass


def metrics(raw_data):
    return


def split_data(temp_line):
    return

def read_input(filename):
    with open(filename, 'r') as f:
        temp_line = f.readline()
        while temp_line != " \n":
            temp_time, temp_volt = split_data(temp_line)
    return


def interface():
    filename = input("Please enter the filename: ")
    ecg_raw_data = read_input(filename)
    ecg_metrics = metrics(ecg_raw_data)
    output_file(ecg_metrics)


if __name__ == '__main__':
    interface()
