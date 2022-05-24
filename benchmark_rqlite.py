import requests
import names
import random
from tqdm import tqdm

rqlite_url = "http://34.223.40.95:4001"

print("Creating test table")
# First, create a simple table for use in testing
requests.post(rqlite_url + "/db/execute", json=[
    "CREATE TABLE testtable (id INTEGER NOT NULL PRIMARY KEY, name TEXT, age INTEGER)"
])

# Send 1000 requests with varying write-read ratios
num_requests = 1000
write_ratio = 0.5
num_write_requests = int(write_ratio * num_requests)
num_read_requests = 1000 - num_write_requests

# Generate entries to write
print(f"Generating {num_write_requests} write requests")

write_entries = []
generated_names = []
for i in range(num_write_requests):
    name = names.get_first_name()
    generated_names.append(name)
    write_entries.append({"name": name, "age": random.randint(1, 100)})

all_requests = []
for write_entry in write_entries:
    all_requests.append(("write", rqlite_url + "/db/execute", [
        f"INSERT INTO testtable(name, age) VALUES(\"{write_entry['name']}\", {write_entry['age']})"
    ]))
for _ in range(num_read_requests):
    random_name = random.choice(generated_names)
    all_requests.append(("read", rqlite_url + "/db/query", {"q": f"SELECT * FROM testtable WHERE name = {random_name}"}))

# Interleave the requests
random.shuffle(all_requests)

print("Issuing requests. Sample:")
print(all_requests[:5])

for request in tqdm(all_requests):
    if request[0] == "write":
        requests.post(request[1], json=request[2])
    elif request[0] == "read":
        requests.get(request[1], data=request[2])
print("Done!")
