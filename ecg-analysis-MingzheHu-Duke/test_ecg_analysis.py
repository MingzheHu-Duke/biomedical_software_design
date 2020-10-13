import pytest
import numpy as np


def test_exception():
    import numpy as np
    from ecg_analysis import data_check
    with pytest.raises(Exception):
        data_check(np.ndarray([[1, 2], [np.nan, 3]]))


# data_processing won't be tested since it is only used to catch exceptions
@pytest.mark.parametrize("data_in, data_out", [
    (np.array([[1, 2], [np.nan, 5], [4, 6]]),
     np.array([[1, 2], [2.5, 5], [4, 6]])),
    (np.array([[np.nan, 2], [2, 5], [4, 6]]),
     np.array([[2, 2], [2, 5], [4, 6]])),
    (np.array([[1, 2], [2, 5], [4, np.nan]]),
     np.array([[1, 2], [2, 5], [4, 5]]))
])
def test_nan_interpolate(data_in, data_out):
    from ecg_analysis import nan_interpolate
    assert np.array_equal(nan_interpolate(data_in), data_out)


def test_ecg_logging():
    from testfixtures import LogCapture
    from ecg_analysis import ecg_logging
    with LogCapture() as log_c:
        ecg_logging(0, "a log")
    log_c.check(("root", "INFO", "a log"))


def test_butter_band_pass():
    import numpy as np
    import math
    from ecg_analysis import butter_band_pass
    x_axis = np.arange(0, 10000)
    low_frequent = np.sin(0.001 * x_axis)
    high_frequent = np.sin(1000 * x_axis)
    mid_frequent = np.sin(0.1 * x_axis)
    low_out = butter_band_pass(low_frequent, 370, 1, 15, order=5)
    high_out = butter_band_pass(high_frequent, 370, 1, 15, order=5)
    mid_out = butter_band_pass(mid_frequent, 370, 1, 15, order=5)
    assert math.isclose(np.sum(np.square(low_out))/10000, 0, abs_tol=1e-04)
    assert math.isclose(np.sum(np.square(high_out)) / 10000, 0, abs_tol=1e-04)
    assert not math.isclose(np.sum(np.square(mid_out)) / 10000, 0,
                            abs_tol=1e-04)


def test_ecg_peaks():
    from scipy.misc import electrocardiogram
    from ecg_analysis import ecg_peaks
    x = electrocardiogram()[2000:4000]
    x2 = electrocardiogram()[1000:2000]
    x3 = electrocardiogram()[6000:8000]
    peaks1 = ecg_peaks(x)
    peaks2 = ecg_peaks(x2)
    peaks3 = ecg_peaks(x3)
    assert peaks1.tolist() == [251, 431, 608, 779, 956, 1125, 1292, 1456]
    assert peaks2.tolist() == [130, 317, 501, 691, 880]
    assert peaks3.tolist() == [48, 250, 454, 865, 1155, 1423, 1608, 1797, 1975]


# just for testing, result dicts are not performance of my entire program
# Did not preprocess electrocardiogram from scipy.misc
def test_ecg_calculator():
    from scipy.misc import electrocardiogram
    from ecg_analysis import ecg_peaks
    import numpy as np
    from ecg_analysis import ecg_peaks
    from ecg_analysis import ecg_logging
    from ecg_analysis import ecg_calculator
    x1 = electrocardiogram()[2000:4000]
    x2 = electrocardiogram()[1000:2000]
    x3 = electrocardiogram()[6000:8000]
    peaks1 = ecg_peaks(x1)
    peaks2 = ecg_peaks(x2)
    peaks3 = ecg_peaks(x3)
    x_axis = np.arange(2000, 4000)
    data1 = np.transpose(np.vstack((x_axis, x1)))
    x_axis = np.arange(1000, 2000)
    data2 = np.transpose(np.vstack((x_axis, x2)))
    x_axis = np.arange(6000, 8000)
    data3 = np.transpose(np.vstack((x_axis, x3)))
    dict1 = ecg_calculator("aaa", data1, peaks1)
    dict1_ans = {'beats': [2251.0, 2431.0, 2608.0, 2779.0, 2956.0, 3125.0,
                           3292.0, 3456.0],
                 'duration': 1998.0,
                 'mean_hr_bpm': 0.24024024024024024,
                 'num_beats': 8,
                 'voltage_extremes': (-1.14, 2.09)}
    dict2 = ecg_calculator("aaa", data2, peaks2)
    dict2_ans = {'beats': [1130.0, 1317.0, 1501.0, 1691.0, 1880.0],
                 'duration': 998.0,
                 'mean_hr_bpm': 0.3006012024048096,
                 'num_beats': 5,
                 'voltage_extremes': (-1.05, 1.5)}
    dict3 = ecg_calculator("aaa", data3, peaks3)
    dict3_ans = {'beats': [6048.0,
                           6250.0,
                           6454.0,
                           6865.0,
                           7155.0,
                           7423.0,
                           7608.0,
                           7797.0,
                           7975.0],
                 'duration': 1998.0,
                 'mean_hr_bpm': 0.2702702702702703,
                 'num_beats': 9,
                 'voltage_extremes': (-1.35, 2.125)}
    assert dict1 == dict1_ans
    assert dict2 == dict2_ans
    assert dict3 == dict3_ans
