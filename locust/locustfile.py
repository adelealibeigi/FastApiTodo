import os
from locust import HttpUser, task, between
from requests.exceptions import RequestException


class LoginUser(HttpUser):
    wait_time = between(1, 3)
    shared_token = None

    def on_start(self):
        if LoginUser.shared_token is None:
            try:
                login_response = self.client.post(
                    "/auth/login",
                    json={"username": 'locustusertest', "password": 'locustpasswordtest'},
                    name="User Login"  # Name for the UI
                )

                login_response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

                token_data = login_response.json()
                LoginUser.shared_token = token_data.get("access_token")  # Adjust key based on your API response

                if not LoginUser.shared_token:
                    return

                self.client.headers.update({
                    "Authorization": f"Bearer {LoginUser.shared_token}"
                })
            except RequestException as e:
                self.environment.runner.quit()  # This will stop all users if login fails critically
            except Exception as e:
                self.environment.runner.quit()
        else:
            self.client.headers.update({
                "Authorization": f"Bearer {LoginUser.shared_token}"
            })

    @task
    def get_tasks(self):

        params = {
            "offset": 1,
            "limit": 50
        }
        response = self.client.get("/task/list", params=params, name='Get Task List')
        if response.status_code!=200:
            print(f"Error fetching tasks: {response.status_code} - {response.text}")
