from modules import TAB_SPACES


class OutputFormatter:
    @staticmethod
    def print_hyphenated(level, tab_list, to_print):
        print(f'{"".join(level*tab_list)}- {to_print}'.expandtabs(TAB_SPACES))

    def print_everything(self, points: list[dict]):
        tab_list = ["\t"]
        for point in points:
            level = 0
            if point["properties"].get("stepDefinition-displayName"):
                self.print_hyphenated(
                    level, tab_list, point["properties"]["stepDefinition-displayName"]
                )
            elif point["properties"].get("type"):
                self.print_hyphenated(level, tab_list, point["properties"]["type"])

            if point["id"] == "flow_info":
                self.print_hyphenated(level, tab_list, "Flow info:")

            level += 1
            self.print_hyphenated(level, tab_list, f"Timestamp: {point['timestamp']}")
            self.print_hyphenated(level, tab_list, "Properties:")

            level += 1
            for k, v in point["properties"].items():
                self.print_hyphenated(level, tab_list, f"{k}: {v}")

            level -= 1
            if point.get("response"):
                self.print_hyphenated(level, tab_list, "Response:")
                level += 1
                for k, v in point["response"]["headers"].items():
                    self.print_hyphenated(level, tab_list, f"{k}: {v}")
                level -= 1
                self.print_hyphenated(
                    level, tab_list, f"Status Code: {point['response']['status_code']}"
                )
                self.print_hyphenated(
                    level, tab_list, f"Reason: {point['response']['reason']}"
                )
            elif point.get("request"):
                self.print_hyphenated(level, tab_list, "Request:")
                level += 1
                for k, v in point["request"]["headers"].items():
                    self.print_hyphenated(level, tab_list, f"{k}: {v}")
                level -= 1
                self.print_hyphenated(
                    level, tab_list, f"Verb: {point['response']['verb']}"
                )
                self.print_hyphenated(
                    level, tab_list, f"URI: {point['response']['uri']}"
                )

    def print_policies(self, policies: list[dict]):
        tab_list = ["\t"]
        for policy in policies:
            level = 0
            if policy["properties"].get("stepDefinition-displayName"):
                self.print_hyphenated(
                    level, tab_list, policy["properties"]["stepDefinition-displayName"]
                )
            else:
                self.print_hyphenated(level, tab_list, policy["properties"]["type"])

            level += 1
            self.print_hyphenated(level, tab_list, f"Timestamp: {policy['timestamp']}")
            self.print_hyphenated(level, tab_list, "Properties:")

            level += 1
            for k, v in policy["properties"].items():
                self.print_hyphenated(level, tab_list, f"{k}: {v}")

    def print_flow_infos(self, flow_infos: list[dict]):
        tab_list = ["\t"]
        level = 0
        self.print_hyphenated(level, tab_list, "Properties:")

        level += 1
        for flow_info in flow_infos:
            self.print_hyphenated(
                level, tab_list, f"Timestamp: {flow_info['timestamp']}"
            )

            level += 1
            for k, v in flow_info["properties"].items():
                self.print_hyphenated(level, tab_list, f"{k}: {v}")
            level -= 1

    def print_flow_hooks():
        pass

    def print_shared_flows():
        pass
