import json


def save_json_to_file(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)


def print_differences(diff, diff_type):
    for key, value in diff.items():
        for item in value:
            if 'old_value' in value[item] and 'new_value' in value[item]:
                print(f"Difference in {diff_type} {item}: {value[item]['old_value']} -> {value[item]['new_value']}")
            else:
                print(f"Difference in {diff_type} {item}: {value[item]}")
