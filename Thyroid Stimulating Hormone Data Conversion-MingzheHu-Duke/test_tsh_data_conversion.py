import pytest
from tsh_data_conversion import strip_returns
from tsh_data_conversion import split_name
from tsh_data_conversion import to_sorted_subfloats
from tsh_data_conversion import tsh_diagnosis
from tsh_data_conversion import dict_generator


@pytest.mark.parametrize("string_list1, string_list2", [
                (["Hello\n", "World\n"], ["Hello", "World"]),
                (["An\n", "Apple\n", "Orange\n"], ["An", "Apple", "Orange"]),
                (["There\n", "is\n", "a\n", "cat\n"],
                 ["There", "is", "a", "cat"])
])
def test_strip_returns(string_list1, string_list2):
    assert strip_returns(string_list1) == string_list2


@pytest.mark.parametrize("full_name, splitted_name", [
                ("James Smith", ["James", "Smith"]),
                ("Michael Smith", ["Michael", "Smith"]),
                ("Maria Garcia", ["Maria", "Garcia"]),
                ("Joshua Boss", ["Joshua", "Boss"])
])
def test_split_name(full_name, splitted_name):
    assert split_name(full_name) == splitted_name


@pytest.mark.parametrize("string_in, sorted_subfloats", [
                ("TSH,2.7,5.2,4.5,3.3,5.8,2.4,5.3,4.2,2.5,5.2,4",
                 [2.4, 2.5, 2.7, 3.3, 4, 4.2, 4.5, 5.2, 5.2, 5.3, 5.8]),
                ("TSH,6.3,6.7,6.3,7.6,2.1,6.9,7.1,4.1,7.2,3.5,2.9",
                 [2.1, 2.9, 3.5, 4.1, 6.3, 6.3, 6.7, 6.9, 7.1, 7.2, 7.6]),
                ("TSH,2,2.6,2.4,2.2,1,1.4,0.2,0.5,2,2.3,0.2",
                 [0.2, 0.2, 0.5, 1, 1.4, 2, 2, 2.2, 2.3, 2.4, 2.6]),
                ("TSH,3.1,4.5,3.5,3.6,5.6,4.8,4.3,5.7,4.2,2.4,5.5",
                 [2.4, 3.1, 3.5, 3.6, 4.2, 4.3, 4.5, 4.8, 5.5, 5.6, 5.7])
])
def test_to_sorted_subfloats(string_in, sorted_subfloats):
    assert to_sorted_subfloats(string_in) == sorted_subfloats


@pytest.mark.parametrize("float_list, result", [
                ([2, 2.6, 2.4, 2.2, 1, 1.4, 0.2, 0.5, 2, 2.3, 0.2],
                 "hyperthyroidism"),
                ([3.1, 4.5, 3.5, 3.6, 5.6, 4.8, 4.3, 5.7, 4.2, 2.4, 5.5],
                 "hypothyroidism"),
                ([0.6, 3.5, 0.2, 3.7, 1.1, 0.2, 3.5, 2.2, 1, 0.6, 3.5],
                 "hyperthyroidism"),
                ([2.4, 2.4, 3.5, 1.1, 3, 3.9, 2, 3.7, 2.1, 3.9],
                 "normal thyroid function")
])
def test_tsh_diagnosis(float_list, result):
    assert tsh_diagnosis(float_list) == result


@pytest.mark.parametrize("field1, field2, field3, field4, field5, dict_result",
                         [(["Jeffrey", "Bond"], 77, "Male",
                          [0.2, 0.2, 0.5, 1.0, 1.4,
                           2.0, 2.0, 2.2, 2.3, 2.4, 2.6], "hyperthyroidism",
                          {"First Name": "Jeffrey",
                           "Last Name": "Bond", "Age": 77,
                           "Gender": "Male", "Diagnosis": "hyperthyroidism",
                           "TSH": [0.2, 0.2, 0.5, 1.0,
                                   1.4, 2.0, 2.0, 2.2, 2.3, 2.4, 2.6]}),
                          (["Monte", "Swarup"], 51, "Male",
                           [2.4, 3.1, 3.5, 3.6, 4.2,
                            4.3, 4.5, 4.8, 5.5, 5.6, 5.7], "hypothyroidism",
                           {"First Name": "Monte",
                            "Last Name": "Swarup", "Age": 51,
                            "Gender": "Male", "Diagnosis": "hypothyroidism",
                            "TSH": [2.4, 3.1, 3.5, 3.6, 4.2,
                                    4.3, 4.5, 4.8, 5.5, 5.6, 5.7]})
                          ]
                         )
def test_dict_generator(field1, field2, field3, field4, field5, dict_result):
    assert dict_generator(field1, field2,
                          field3, field4, field5) == dict_result


def content_formatting(string_list):
    """Format the raw data into different fields and save them.

    This function will first format the raw information into
    different fields and save them into dictionaries, it will then
    call the dict_to_json to save them into .json files.

    Args:
        string_list (list): The list of string that you want to format

    Returns:
        None
    """
    for i in range(int((len(string_list)-1)/4)):
        field1 = split_name(string_list[4*i + 0])
        field2 = int(string_list[4*i + 1])
        field3 = string_list[4*i + 2]
        field4 = to_sorted_subfloats(string_list[4*i + 3])
        diagnosis_result = tsh_diagnosis(field4)
        patient_dict = dict_generator(field1, field2, field3, field4,
                                      diagnosis_result)
        dict_to_json(patient_dict)
