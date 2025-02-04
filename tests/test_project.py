import pytest
from deepdiff import DeepDiff
from utils.apis import APIS
import json
import os
from tests.conftest import load_data_excel


@pytest.fixture(scope='module')
def api_client():
    return APIS()


@pytest.mark.parametrize("test_id, record", load_data_excel())
def test_post_projects(api_client, test_id, record):
    response = api_client.post('projects', record["Request JSON"], headers=record["Headers"])
    assert response.status_code == record["Response Status Code"], \
        f"Status code does not match: expected {record['Response Status Code']}, got {response.status_code}"

    header_value = response.headers.get("Access-Control-Max-Age")
    print(f"Header 'Access-Control-Max-Age': {header_value}")
    assert header_value == "3600", \
        f"Header 'Access-Control-Max-Age' does not match: expected '3600', got {header_value}"

    print(f"Response headers: {response.headers}")
    print(f"Response JSON: {response.json()}")

    response_json = response.json()
    expected_json = json.loads(record["Response JSON"])

    # Define paths to exclude from comparison
    exclude_paths = ["root['errors']['timestamp']", "root['Date']"]

    # Validate that the expected fields are present in the response
    for key in expected_json.keys():
        assert key in response_json, f"Missing expected field in response JSON: {key}"

    for key in record["Response Headers"].keys():
        assert key in response.headers, f"Missing expected header in response: {key}"

    diff = DeepDiff(expected_json, response_json, significant_digits=6)
    header_diff = DeepDiff(record["Response Headers"], dict(response.headers))

    # Exclude variable fields from assertion checks
    filtered_diff = DeepDiff(expected_json, response_json, significant_digits=6, exclude_paths=exclude_paths)
    filtered_header_diff = DeepDiff(record["Response Headers"], dict(response.headers), exclude_paths=exclude_paths)

    if diff or header_diff:
        save_test_artifacts(test_id, record, response, response_json, expected_json, diff, header_diff)

    assert not filtered_diff, f"Difference in response JSON for test {test_id}: {filtered_diff}"
    assert not filtered_header_diff, f"Difference in response headers for test {test_id}: {filtered_header_diff}"


def save_test_artifacts(test_id, record, response, response_json, expected_json, diff, header_diff):
    base_dir = os.path.join(os.path.dirname(__file__), '..', 'test_artifacts')
    directories = ['expected_responses', 'received_responses', 'request_headers', 'response_headers', 'request_body',
                   'diffs', 'expected_headers']
    for directory in directories:
        os.makedirs(os.path.join(base_dir, directory), exist_ok=True)

    save_json_to_file(os.path.join(base_dir, f'expected_responses/expected_response_{test_id}.json'), expected_json)
    save_json_to_file(os.path.join(base_dir, f'received_responses/received_response_{test_id}.json'), response_json)
    save_json_to_file(os.path.join(base_dir, f'request_headers/request_headers_{test_id}.json'), record["Headers"])
    save_json_to_file(os.path.join(base_dir, f'response_headers/response_headers_{test_id}.json'),
                      dict(response.headers))
    save_json_to_file(os.path.join(base_dir, f'request_body/request_body_{test_id}.json'), record["Request JSON"])
    save_json_to_file(os.path.join(base_dir, f'diffs/diff_{test_id}.json'),
                      {"body_diff": diff, "header_diff": header_diff})
    save_json_to_file(os.path.join(base_dir, f'expected_headers/expected_headers_{test_id}.json'),
                      record["Response Headers"])

    print_differences(diff, "field")
    print_differences(header_diff, "header")


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
