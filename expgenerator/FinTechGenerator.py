#################################################
# This code is largely based on Tom Totenberg's
# app, located here:
# https://github.com/ttotenberg-ld/ld_funnel_experiment_runner_platform
#################################################

import random
import ContextCreator
import ldclient
from BaseGenerator import BaseGenerator
from ldclient.config import Config


class FinTechGenerator(BaseGenerator):
    # Metrics
    funnel_metric_1 = "ai-analyze-clicked"
    funnel_metric_2 = "financial-advisor-contacted"
    ai_csat_positive_metric = "ai-csat-positive"
    ai_csat_negative_metric = "ai-csat-negative"
    ai_response_latency = "ai-response-latency"
    ai_cost = "ai-analysis-cost"

    funnel_metric_1_percent_converted = 40

    def __init__(self, project_key, env_key, exp_key, api_key, iterations=1000):
        super().__init__(project_key, env_key, exp_key, api_key, iterations)
        self.context = ContextCreator.ContextCreator()
        ldclient.set_config(Config(self.sdk_key))

    def __del__(self):
        ldclient.get().close()

    def get_metric_params(self):
        # Control, Treatment 1, Treatment 2
        params = [
            {
                "funnel_metric_2_percent_converted": 64,
                "ai_csat_positive_percent_converted": 28,
                "ai_csat_negative_percent_converted": 5,
                "ai_response_latency_range": [500, 1750],
                "ai_cost_range": [0.04, 0.06],
            },
            {
                "funnel_metric_2_percent_converted": 60,
                "ai_csat_positive_percent_converted": 23,
                "ai_csat_negative_percent_converted": 11,
                "ai_response_latency_range": [650, 2200],
                "ai_cost_range": [0.04, 0.05],
            },
            {
                "funnel_metric_2_percent_converted": 77,
                "ai_csat_positive_percent_converted": 41,
                "ai_csat_negative_percent_converted": 3,
                "ai_response_latency_range": [400, 1280],
                "ai_cost_range": [0.03, 0.04],
            },
        ]

        return params

    def conversion_chance(self, chance_number):
        chance_calc = random.randint(1, 100)
        if chance_calc <= chance_number:
            return True
        else:
            return False

    def execute_call_if_converted(self, metric, percent_chance, context):
        user_context = context.get_individual_context("user")
        context_name = user_context.get("name")
        if self.conversion_chance(int(percent_chance)):
            ldclient.get().track(metric, context)
            print(f"User {context_name} converted for {metric}")
            return True
        else:
            print(f"User {context_name} did NOT convert for {metric}")
            return False

    def calc_csat(self, positive_csat, negative_csat, context):
        value = random.randint(1, 100)
        if value <= positive_csat:
            print("CSAT: Positive")
            ldclient.get().track(self.ai_csat_positive_metric, context)
        elif value <= negative_csat:
            print("CSAT: Negative")
            ldclient.get().track(self.ai_csat_negative_metric, context)
        else:
            print("CSAT: None")

    def run(self):
        params = self.get_metric_params()
        treatments = self.get_experiment_treatments()
        for i in range(self.iterations):
            context = self.context.create_multi_context()
            context_user = context.get_individual_context("user")
            context_name = context_user.get("name")
            print(f"USER: {context_name}")

            flag_detail = ldclient.get().variation_detail(
                self.flag_key, context, "unavailable"
            )
            index = flag_detail.variation_index

            if self.execute_call_if_converted(
                self.funnel_metric_1, self.funnel_metric_1_percent_converted, context
            ):
                for treatment in treatments:
                    if index == treatment["index"]:
                        print("Serving " + treatment["treatment_name"])
                        # Track latency
                        latency = random.randint(
                            params[treatment["index"]]["ai_response_latency_range"][0],
                            params[treatment["index"]]["ai_response_latency_range"][1],
                        )
                        ldclient.get().track(
                            "ai-response-latency", context, metric_value=latency
                        )
                        print(f"LATENCY: {latency}ms")
                        # Track cost
                        cost = random.uniform(
                            params[treatment["index"]]["ai_cost_range"][0],
                            params[treatment["index"]]["ai_cost_range"][1],
                        )
                        ldclient.get().track(
                            "ai-analysis-cost", context, metric_value=cost
                        )
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
                        # Track funnel metric 2 if they convert
                        self.execute_call_if_converted(
                            self.funnel_metric_2,
                            params[treatment["index"]][
                                "funnel_metric_2_percent_converted"
                            ],
                            context,
                        )
