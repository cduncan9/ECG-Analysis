import pytest
import math
import numpy as np


@pytest.mark.parametrize("string, exp", [
    ('1, 2', ('1', '2')),
    ('1, ', ('1', '')),
    ('2', ('2', '')),
    ('  , 3', ('', '3'))])
def test_split_data(string, exp):
    from ecg_analysis import split_data
    answer = split_data(string)
    assert answer == exp


@pytest.mark.parametrize("time, volt, expected", [
    ('1', '1', True),
    ('1', '', False),
    ('1', 'Hello', False),
    ('', '1', False),
    ('0.5', '-1.7', True)])
def test_check_data(time, volt, expected):
    from ecg_analysis import check_data
    answer = check_data(time, volt)
    assert answer == expected


@pytest.mark.parametrize("test_num, exp", [
    ("1", True),
    ("0.5", True),
    ("-0.56677", True),
    ("Happy", False),
    ("#*$(", False)])
def test_is_a_number(test_num, exp):
    from ecg_analysis import is_a_number
    answer = is_a_number(test_num)
    assert answer == exp


# def test_filter_data():
#     from ecg_analysis import filter_data
#     time = np.linspace(0, 0.05, 20)
#     sample_data = np.ones(20)
#     noise = [math.sin(2*math.pi*100*time[i]) for i in range(len(time))]
#     volt_w_noise = [sample_data[i] * noise[i] for i in range(len(time))]
#     answer = filter_data(time, volt_w_noise)
#     assert answer[3] == sample_data[3]

def test_calc_duration():
    from ecg_analysis import calc_duration
    time = np.linspace(0, 1, 200)
    expected = 1
    answer = calc_duration(time)
    assert answer == expected


def test_calc_voltage_extremes():
    from ecg_analysis import calc_voltage_extremes
    data = [0, 1, 1, -4, 18, -7, 2, 0]
    expected = (-7, 18)
    answer = calc_voltage_extremes(data)
    assert answer == expected
