def verify_dict_has_desired_keys(base_dict, desired_keys):
    base_dict_keys = set(base_dict.keys())
    intersection = desired_keys & base_dict_keys

    return intersection == desired_keys


def verify_dict_doesnt_have_unaccepted_keys(base_dict, accepted_keys):
    base_dict_keys = set(base_dict.keys())
    union = accepted_keys | base_dict_keys

    return union == accepted_keys
