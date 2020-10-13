def load_data(file_name):
    """Read and load the raw data from the .txt file

    This function will read all the lines from the given
    file and store them as a list of Strings.

    Args:
        file_name (str): The file you want to read from

    Returns:
        list: a list of strings
    """
    with open(file_name, "r+") as read_object:
        content = read_object.readlines()
    return content


def strip_returns(string_list):
    """Strip all the trailing returns

    This function will remove all the trailing returns
    from all the elements of a list of strings.

    Args:
        string_list (list): A list of strings

    Returns:
        list: A list of strings without trialing returns
    """
    string_list = [i.strip("\n") for i in string_list]
    return string_list


def split_name(full_name):
    """Split the name

    This function will split the full names into first names and last
    names.

    Args:
        full_name (str): The full name you want to split.

    Returns:
        list: list of strings [First Name, Last Name]
    """
    splitted_name = full_name.split(" ")
    return splitted_name


def to_sorted_subfloats(float_string):
    """Convert string of floats into sorted list of floats.

    This function will first remove the "TSH" and turn the string of
    floats into the list of floats and sort them from smaller to larger.

    Args:
        float_string (str): A string begin with "TSH" and followed by
            a sequence of floats.

    Returns:
        list: a list of pure sorted floats.
    """
    float_list = float_string.split(",")
    float_list.remove("TSH")
    float_list = [float(i) for i in float_list]
    float_list.sort()
    return float_list


def tsh_diagnosis(float_list):
    """Diagnosis from data

        From the TSH results from each patient, assign one of the following
        diagnoses to the patient "hyperthyroidism", hypothyroidism",
        "normal thyroid function".

        Args:
            float_list (list): list of floats of the tsh data.

        Returns:
            str: "hyperthyroidism" or hypothyroidism" or
                "normal thyroid function"
    """
    for i in float_list:
        if i < 1:
            return "hyperthyroidism"
            break
        elif i > 4:
            return "hypothyroidism"
            break
    return "normal thyroid function"


def dict_generator(field1, field2, field3, field4, field5):
    """Generate dictionary

        Generate the dictionaries from the given field information.

        Args:
            field1 (list): [first name, last name]
            field2 (int): age of the patient_dict
            field3 (str): Gender of the patient
            field4 (list): TSH data of the patient
            field5 (str): Diagnosis result of the patient

        Returns:
            dictionary: The dict include all the information of the patient
    """
    patient_dict = {}
    patient_dict["First Name"] = field1[0]
    patient_dict["Last Name"] = field1[1]
    patient_dict["Age"] = field2
    patient_dict["Gender"] = field3
    patient_dict["Diagnosis"] = field5
    patient_dict["TSH"] = field4
    return patient_dict


def dict_to_json(dict_in):
    """Save the dictionary into JSON

        Save the dictionary information into the JSON file names as
        fistname-lastname.json

        Args:
            dict_in (dictionary): Include all the information of the
                patient.

        Returns:
            None
    """
    import json
    with open("{}-{}.json".format(dict_in["First Name"],
                                  dict_in["Last Name"]), "w") as write_object:
        json.dump(dict_in, write_object)


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


def main():
    # Here is the main function
    in_file = input("Please enter the file name you want us to analysis:")
    content = load_data(in_file)
    trimmed_content = strip_returns(content)
    content_formatting(trimmed_content)


if __name__ == "__main__":
    main()
