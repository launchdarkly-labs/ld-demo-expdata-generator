import json
import names
import random
import uuid
from ldclient import Context


class ContextCreator:
    def beta_chance(self):
        if random.randint(1, 10) <= 3:
            return True
        else:
            return False

    def create_user_context(self):
        user_key = "usr-" + str(uuid.uuid4())
        name = f"{names.get_first_name()} {names.get_last_name()}"
        plan = random.choice(["platinum", "silver", "gold", "diamond", "free"])
        tier = random.choice(["Platinum", "Gold", "Silver"])
        role = random.choice(["reader", "writer", "admin"])
        metro = random.choice(
            [
                "New York",
                "Chicago",
                "Minneapolis",
                "Atlanta",
                "Los Angeles",
                "San Francisco",
                "Denver",
                "Boston",
            ]
        )

        user_context = (
            Context.builder(user_key)
            .set("kind", "user")
            .set("name", name)
            .set("plan", plan)
            .set("role", role)
            .set("metro", metro)
            .set("tier", tier)
            .set("beta", self.beta_chance())
            .build()
        )

        return user_context

    def create_audience_context(self):
        audience_key = "aud-" + str(uuid.uuid4())
        name = f"{names.get_first_name()} {names.get_last_name()}"
        plan = random.choice(["platinum", "silver", "gold", "diamond", "free"])
        state = random.choice(["MN", "CA", "NY", "FL", "TX", "GA", "CO", "MA"])
        audience_context = (
            Context.builder(audience_key)
            .set("kind", "audience")
            .set("name", name)
            .set("plan", plan)
            .set("state", state)
            .build()
        )

        return audience_context

    def create_device_context(self):
        device_key = "dvc-" + str(uuid.uuid4())
        os = random.choice(["Android", "iOS", "Mac OS", "Windows"])
        version = random.choice(["1.0.2", "1.0.4", "1.0.7", "1.1.0", "1.1.5"])
        type = random.choice(
            ["Fire TV", "Roku", "Hisense", "Comcast", "Verizon", "Browser"]
        )

        device_context = (
            Context.builder(device_key)
            .set("kind", "device")
            .set("os", os)
            .set("type", type)
            .set("version", version)
            .build()
        )

        return device_context

    def create_organization_context(self):
        key_name = random.choice(
            [
                {
                    "key": "org-7f9f58eb-c8e8-4c40-9962-43b13eeec4ea",
                    "name": "Mayo Clinic",
                    "employees": 76000,
                },
                {
                    "key": "org-40fad050-3f91-49dc-8007-33d02f1869e0",
                    "name": "IBM",
                    "employees": 288000,
                },
                {
                    "key": "org-fca878d0-3cab-4301-91da-bbc6dbb08fff",
                    "name": "3M",
                    "employees": 92000,
                },
            ]
        )
        region = random.choice(["NA", "CN", "EU", "IN", "SA"])

        org_context = (
            Context.builder(key_name["key"])
            .set("kind", "organization")
            .set("name", key_name["name"])
            .set("region", region)
            .set("employees", key_name["employees"])
            .build()
        )

        return org_context

    def create_multi_context(self):

        multi_context = Context.create_multi(
            self.create_user_context(),
            self.create_device_context(),
            self.create_organization_context(),
        )

        return multi_context
