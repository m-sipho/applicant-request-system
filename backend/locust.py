from locust import HttpUser, between, task
import random
import string

class ApplicantIser(HttpUser):
    wait_time = between(1, 5)

    @task
    def register_applicant(self):
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        email = f"user_{random_suffix}@example.com"

        # Define the payload
        payload = {
            "name": f"Test User {random_suffix}",
            "email": email,
            "password": "StrongPassword123"
        }

        # Send the POST request
        self.client.post("/register", json=payload, name="/register")