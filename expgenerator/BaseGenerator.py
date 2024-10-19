import requests
import json
import os


class BaseGenerator:
    def __init__(self, project_key, env_key, exp_key, api_key, iterations=1000):
        self.project_key = project_key
        self.env_key = env_key
        self.exp_key = exp_key
        self.api_key = api_key
        self.iterations = iterations
        self.sdk_key = self.get_sdk_key()
        self.flag_key = self.get_flag_key()

    def get_flag_key(self):
        url = (
            "https://app.launchdarkly.com/api/v2/projects/"
            + self.project_key
            + "/environments/"
            + self.env_key
            + "/experiments/"
            + self.exp_key
            + "?expand=currentIteration,treatments"
        )
        headers = {
            "Authorization": os.getenv("LD_API_KEY"),
            "Content-Type": "application/json",
        }
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        flag_key = list(data["currentIteration"]["flags"].keys())[0]
        return flag_key

    def get_sdk_key(self):
        url = (
            "https://app.launchdarkly.com/api/v2/projects/"
            + self.project_key
            + "/environments/"
            + self.env_key
        )

        headers = {"Content-Type": "application/json", "Authorization": self.api_key}

        response = requests.get(
            url,
            headers=headers,
        )
        data = json.loads(response.text)

        return data["apiKey"]

    def get_flag_variations(self, flag_key):
        var_ids = []
        url = (
            "https://app.launchdarkly.com/api/v2/flags/"
            + self.project_key
            + "/"
            + flag_key
        )
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json",
        }
        res = requests.get(url, headers=headers)
        data = json.loads(res.text)
        idx = 0
        for var in data["variations"]:
            var_ids.append({"index": idx, "flag_id": var["_id"], "value": var["value"]})
            idx += 1

        return var_ids

    def get_experiment_treatments(self):
        treatments = []
        url = (
            "https://app.launchdarkly.com/api/v2/projects/"
            + self.project_key
            + "/environments/"
            + self.env_key
            + "/experiments/"
            + self.exp_key
            + "?expand=currentIteration,treatments"
        )
        headers = {
            "Authorization": os.getenv("LD_API_KEY"),
            "Content-Type": "application/json",
        }
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        flag_vars = self.get_flag_variations(self.flag_key)

        for treatment in data["currentIteration"]["treatments"]:
            index = 0
            flag_id = ""
            flag_value = ""

            for var in flag_vars:
                if treatment["parameters"][0]["variationId"] == var["flag_id"]:
                    index = var["index"]
                    flag_id = var["flag_id"]
                    flag_value = var["value"]
            treatments.append(
                {
                    "index": index,
                    "flag_id": flag_id,
                    "value": flag_value,
                    "treatment_name": treatment["name"],
                    "allocation": treatment["allocationPercent"],
                    "control": treatment["baseline"],
                }
            )
            print(f"Experiment Treatment: {treatment['name']}")

        return treatments
