import random
import ContextCreator
import ldclient
from BaseGenerator import BaseGenerator
from ldclient.config import Config


class UserProfileGenerator(BaseGenerator):
    # Metrics
    ai_csat_positive_metric = "AI Chatbot Positive Feedback"
    ai_csat_negative_metric = "AI Chatbot Negative Feedback"

    def __init__(self, project_key, env_key, exp_key, api_key, iterations=1000):
        super().__init__(project_key, env_key, exp_key, api_key, iterations)
        self.context = ContextCreator.ContextCreator()
        ldclient.set_config(Config(self.sdk_key))

    def __del__(self):
        ldclient.get().close()

    def get_metric_params(self):
        # Control, Treatment 1, Treatment 2, Treatment 3
        params = [
            {
                "ai_csat_positive_percent_converted": 28,
                "ai_csat_negative_percent_converted": 5,
            },
            {
                "ai_csat_positive_percent_converted": 23,
                "ai_csat_negative_percent_converted": 11,
            },
            {
                "ai_csat_positive_percent_converted": 41,
                "ai_csat_negative_percent_converted": 3,
            },
            {
                "ai_csat_positive_percent_converted": 58,
                "ai_csat_negative_percent_converted": 7,
            },
        ]

        return params

    def calc_csat(self, positive_csat, negative_csat, context):
        value = random.randint(1, 100)
        if value <= negative_csat:
            print("CSAT: Negative")
            ldclient.get().track(self.ai_csat_negative_metric, context)
        elif value <= positive_csat:
            print("CSAT: Positive")
            ldclient.get().track(self.ai_csat_positive_metric, context)
        else:
            print("CSAT: None")

    def run(self):
        params = self.get_metric_params()
        treatments = self.get_experiment_treatments()
        for i in range(self.iterations):
            context = self.context.create_audience_context()
            context_name = context.get("name")
            print(f"USER: {context_name}")

            flag_detail = ldclient.get().variation_detail(
                self.flag_key, context, "unavailable"
            )
            index = flag_detail.variation_index

            for treatment in treatments:
                if index == treatment["index"]:
                    print("Serving " + treatment["treatment_name"])
                    # Track CSAT
                    self.calc_csat(
                        params[treatment["index"]][
                            "ai_csat_positive_percent_converted"
                        ],
                        params[treatment["index"]][
                            "ai_csat_negative_percent_converted"
                        ],
                        context,
                    )
