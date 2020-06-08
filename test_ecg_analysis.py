import pytest


def test_split_data():
    from ecg_analysis import split_data
    expected = '1', '2'
    answer = split_data('1, 2')
    assert answer == expected
