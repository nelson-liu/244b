from locust import HttpUser, task
import requests
import names
import random
from tqdm import tqdm
import warnings

rqlite_url = "http://34.223.40.95:4001"

print("Creating test table")
# First, create a simple table for use in testing
requests.post(rqlite_url + "/db/execute", json=[
    "CREATE TABLE testtable (id INTEGER NOT NULL PRIMARY KEY, name TEXT, age INTEGER)"
])

# Send 1000 requests with varying write-read ratios
num_requests = 10000

write_entries = []
generated_names = []
for i in range(num_requests):
    name = names.get_first_name()
    generated_names.append(name)
    write_entries.append({"name": name, "age": random.randint(1, 100)})

write_requests = []
for write_entry in write_entries:
    write_requests.append([
        f"INSERT INTO testtable(name, age) VALUES(\"{write_entry['name']}\", {write_entry['age']})"
    ])

read_requests = []
for _ in range(num_requests):
    random_name = random.choice(generated_names)
    read_requests.append([f"SELECT * FROM testtable WHERE name = \"{random_name}\""])

class UserBehavior(HttpUser):
    @task(1)
    def write_request(self):
        message = random.choice(write_requests)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.client.post("/db/execute", json=message, verify=False)

    @task(1)
    def read_request(self):
        message = random.choice(read_requests)
        self.client.post("/db/query", json=message)
