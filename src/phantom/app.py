APP_ERROR = False
APP_SUCCESS = True
ACTION_ID_TEST_ASSET_CONNECTIVITY = "test_connectivity"


def is_fail(x):
    if x:
        return False
    return True


def is_success(x):
    return not is_fail(x)


def get_req_value(in_dict, in_key, strip_it=True):
    print(strip_it)

    if in_key not in in_dict:
        raise TypeError("Required Parameter not found")

    value = in_dict[in_key].strip()

    if len(value) == 0:
        raise TypeError("Required Parameter not found")

    return value
