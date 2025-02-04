import requests


class APIS:
    def __init__(self, base_url='http://localhost:8080/'):
        self.base_url = base_url

    def get(self, endpoint, headers):
        url = f"{self.base_url}/{endpoint}"
        return requests.get(url, headers=headers)

    def post(self, endpoint, data, headers):
        url = f"{self.base_url}/{endpoint}"
        return requests.post(url, headers=headers, json=data)

    def put(self, endpoint, data, headers):
        url = f"{self.base_url}/{endpoint}"
        return requests.put(url, headers=headers, json=data)

    def delete(self, endpoint, headers):
        url = f"{self.base_url}/{endpoint}"
        return requests.delete(url, headers=headers)
