def output_file(metrics):
    pass


def metrics(raw_data):
    pass


def read_input(filename):
    pass


def interface():
    filename = input("Please enter the filename: ")
    ecg_raw_data = read_input(filename)
    ecg_metrics = metrics(ecg_raw_data)
    output_file(ecg_metrics)


if __name__ == '__main__':
    interface()