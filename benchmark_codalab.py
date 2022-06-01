#!/usr/bin/env python3
from locust import User, task
import subprocess

class UserBehavior(User):
    # @task(1)
    # def run_date(self):
    #     subprocess.run(["cl", "run", "date"], check=True)

    @task(1)
    def run_search(self):
        subprocess.run(["cl", "search", ".mine"], check=True)
