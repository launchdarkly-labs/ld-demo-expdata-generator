import json
import requests
import time
import os
from FinTechGenerator import FinTechGenerator
from UserProfileGenerator import UserProfileGenerator


def get_resource_names(resource):
    resource_items = resource.split(":")
    for item in resource_items:
        res = item.split("/")
        match res[0]:
            case "proj":
                tp_key = res[1].split(";")
                project_key = tp_key[0]
            case "env":
                te_key = res[1].split(";")
                env_key = te_key[0]
            case "experiment":
                tf_key = res[1].split(";")
                exp_key = tf_key[0]
    return project_key, env_key, exp_key


def lambda_handler(event, context):
    project_key = ""
    env_key = ""
    exp_key = ""
    current_action = ""
    current_resource = ""
    api_key = os.getenv("LD_API_KEY")

    data = json.loads(event["body"])
    # data = event["body"]

    for action in data["accesses"]:
        print("Action: " + action["action"])
        print("Resource: " + action["resource"])
        print(action)
        current_action = action["action"]
        current_resource = action["resource"]

    project_key, env_key, exp_key = get_resource_names(current_resource)

    exit_message = "Nothing actionable."

    if current_action == "updateExperiment":
        print("Starting...")
        time.sleep(10)
        print("Gathering data...")
        current_time = int(time.time() * 1000)
        url = "https://app.launchdarkly.com/api/v2/auditlog?before=" + str(current_time)
        headers = {
            "Content-Type": "application/json",
            "Authorization": os.getenv("LD_API_KEY"),
        }
        payload = [
            {
                "actions": ["*"],
                "effect": "allow",
                "resources": [
                    "proj/" + project_key + ":env/" + env_key + ":experiment/" + exp_key
                ],
            }
        ]
        response = requests.request("POST", url, headers=headers, json=payload)

        data = json.loads(response.text)
        item = data["items"][0]
        print("Status: " + item["titleVerb"])
        if item["titleVerb"].lower() == "started experiment":
            match (exp_key):
                case "ai-analysis-to-advisor":
                    print("Generating data for Advisor Conversion.")
                    exp = FinTechGenerator(
                        project_key, env_key, exp_key, api_key, iterations=1047
                    )
                    exp.run()
                    del exp
                    exit_message = "Advisor Conversion data generation complete!"
                case "ai-chatbot-experiment":
                    exp = UserProfileGenerator(
                        project_key, env_key, exp_key, api_key, iterations=2681
                    )
                    exp.run()
                    del exp
                    exit_message = "Advisor Conversion data generation complete!"
                    print("Generating data for AI Chatbot Experiment.")
                case _:
                    exit_message = "Unknown experiment (" + exp_key + "). Exiting."

    return {"statusCode": 200, "body": json.dumps(exit_message)}
