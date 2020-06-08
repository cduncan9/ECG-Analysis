import pytest


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
