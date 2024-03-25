import json
import pathlib

import xmltodict


class XMLParser:
    def __init__(self, xml_file_path: pathlib.Path) -> None:
        self.file = xml_file_path
        self.filters = None
        self.json_dict = None
        self.text = None
        self.transactions = []
        self.flow_infos: list[dict] = []
        self.policies: list[dict] = []
        self.skipped: list[dict] = []
        self.invoked: list[dict] = []
        self.everything: list[dict] = []

    def json(self):
        with open(str(self.file), "r") as xml_file:
            self.json_dict = xmltodict.parse(xml_file.read(), xml_attribs=True)
        self.transactions = self.json_dict["DebugSession"]["Messages"]["Message"]

    @staticmethod
    def set_attributes(d: dict, obj: dict):
        name = obj.get("@name")
        text = obj.get("#text")
        match name:
            case "type":
                d[name] = text.replace("Execution", "").replace("Step", "")
            case _:
                d[name] = text

    @staticmethod
    def set_properties(obj: dict, properties: dict):
        if isinstance(properties, list):
            for prop in properties:
                XMLParser.set_attributes(obj, prop)
        elif isinstance(properties, dict):
            XMLParser.set_attributes(obj, properties)

    def set_policy_message(self, message_type: str, policy: dict):
        original_message = policy[f"{message_type.capitalize()}Message"]
        message = {"headers": {}}
        message_headers: list = original_message["Headers"]["Header"]
        for obj in message_headers:
            self.set_attributes(message["headers"], obj)
        if message_type == "request":
            message["uri"] = original_message["URI"]
            message["verb"] = original_message["Verb"]
        elif message_type == "response":
            message["reason"] = original_message["ReasonPhrase"]
            message["status_code"] = original_message["StatusCode"]

        policy[message_type] = message

    def set_policies(self, policy: dict):
        self.policies.append(
            {
                "id": "policy",
                "properties": {},
                "timestamp": policy["DebugInfo"]["Timestamp"],
            }
        )
        current_policy = self.policies[-1]
        properties = policy["DebugInfo"]["Properties"]["Property"]
        self.set_properties(current_policy["properties"], properties)
        if (
            current_policy["properties"].get("result")
            and current_policy["properties"]["stepDefinition-enabled"] == "true"
        ):
            self.invoked.append(current_policy)
        else:
            self.skipped.append(current_policy)
        
        if policy.get("RequestMessage"):
            self.set_policy_message("request", policy)
        elif policy.get("ResponseMessage"):
            self.set_policy_message("response", policy)


    def set_flow_info(self, point: dict):
        self.flow_infos.append(
            {
                "id": "flow_info",
                "timestamp": point["DebugInfo"]["Timestamp"],
                "properties": {},
            }
        )
        properties = point["DebugInfo"]["Properties"]["Property"]
        self.set_properties(self.flow_infos[-1]["properties"], properties)

    def set_data(self, transaction) -> None:
        if isinstance(self.transactions, list):
            for point in self.transactions[transaction]["Data"]["Point"]:
                match point["@id"]:
                    case "Execution":
                        self.set_policies(point)
                        self.everything.append(self.policies[-1])
                    case "FlowInfo":
                        self.set_flow_info(point)
                        self.everything.append(self.flow_infos[-1])
        elif isinstance(self.transactions, dict):
            for point in self.transactions["Data"]["Point"]:
                match point["@id"]:
                    case "Execution":
                        self.set_policies(point)
                        self.everything.append(self.policies[-1])
                    case "FlowInfo":
                        self.set_flow_info(point)
                        self.everything.append(self.flow_infos[-1])

    def get_transaction_id(self, main_sel):
        if isinstance(self.transactions, list):
            return self.transactions[main_sel]["DebugId"]
        elif isinstance(self.transactions, dict):
            return self.transactions["DebugId"]
