import json
import time
from venv import create
import requests
from typing import Optional
from s3ping.solvers.base import CaptchaSolver
from s3ping.core.utils.logger import Logger  # Adjust the import based on your structure

class CapSolver(CaptchaSolver):
    def __init__(self, api_key: str, logger: Optional[Logger] = None):
        self.api_key = api_key
        self.logger = logger or Logger(class_name=self.__class__.__name__)

    def solve(self, site_key: str, url: str) -> Optional[str]:
        api_url = "https://api.capsolver.com"
        headers = {"Content-Type": "application/json"}
        self.logger.info("Creating CAPTCHA task...")

        try:
            payload = {
                "clientKey": self.api_key,
                "task": {
                    "type": "ReCaptchaV2TaskProxyLess",
                    "websiteURL": url,
                    "websiteKey": site_key,
                }
            }

            create_resp = requests.post(
                f"{api_url}/createTask",
                headers=headers,
                data=json.dumps(payload)
            )
        
            print(create_resp.json())

            if not create_resp.ok:
                self.logger.error(f"Failed to create CAPTCHA task {api_url}. HTTP {create_resp.status_code}")
                return None

            create_data = create_resp.json()
            self.logger.debug(f"CAPTCHA task create response: {create_data}")

            task_id = create_data.get("taskId")
            if not task_id:
                self.logger.error("No taskId received from capsolver.")
                return None

        except Exception as e:
            self.logger.error(f"Exception while creating CAPTCHA task: {e}")
            return None

        # Polling for result
        self.logger.info(f"Polling for CAPTCHA solution (taskId: {task_id})...")
        for i in range(20):
            time.sleep(5)
            try:
                result_payload = {
                    "clientKey": self.api_key,
                    "taskId": task_id
                }
                poll_resp = requests.post(
                    f"{api_url}/getTaskResult",
                    headers=headers,
                    data=json.dumps(result_payload)
                )

                if not poll_resp.ok:
                    self.logger.warning(f"Polling failed at attempt {i+1}: HTTP {poll_resp.status_code}")
                    continue

                result = poll_resp.json()
                self.logger.debug(f"CAPTCHA result poll {i+1}: {result}")

                if result.get("status") == "ready":
                    solution = result.get("solution", {})
                    token = solution.get("gRecaptchaResponse")
                    if token:
                        self.logger.info("CAPTCHA solved successfully.")
                        return token
                    else:
                        self.logger.warning("Solution received but token is missing.")
                        return None

            except Exception as e:
                self.logger.error(f"Exception while polling result: {e}")
                return None

        self.logger.warning("CAPTCHA solving timed out.")
        return None