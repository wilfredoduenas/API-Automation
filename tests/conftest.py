import pytest
import pandas as pd
import os
import json
from datetime import datetime


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    report_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    config.option.htmlpath = os.path.join(report_dir, f'reports_{now}.html')


@pytest.fixture(scope="session", autouse=True)
def setup_teardown():
    print("Startling")
    yield
    print("End")


@pytest.fixture(scope="session")
def load_data():
    json_file_path = os.path.join(os.path.dirname(__file__), "data", 'test_data.json')
    with open(json_file_path) as json_file:
        data = json.load(json_file)
    return data


def load_data_excel():
    excel_file_path = os.path.join(os.path.dirname(__file__), "data", 'test_data.xlsx')
    df = pd.read_excel(excel_file_path)
    data = []
    for _, row in df.iterrows():
        record = {
            "Test": row["Test"],
            "Method": row["Method"],
            "Headers": json.loads(row["Headers"]),
            "Request JSON": json.loads(row["Request JSON"]),
            "Response Status Code": row["Response Status Code"],
            "Response JSON": row["Response JSON"],
            "Response Headers": json.loads(row["Response Headers"])

        }
        data.append((row["Test"], record))
    return data