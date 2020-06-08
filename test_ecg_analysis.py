import pytest


def test_split_data():
    from ecg_analysis import split_data
    expected = '1', '2'
    answer = split_data('1, 2')
    assert answer == expected


@pytest.mark.parametrize("time, volt, expected", [
                        ('1', '1', True),
                        ('1', '', False),
                        ('1', 'Hello', False),
                        ('0.5', '-1.7', True)])
def test_check_data(time, volt, expected):
    from ecg_analysis import check_data
    answer = check_data(time, volt)
    assert answer == expected