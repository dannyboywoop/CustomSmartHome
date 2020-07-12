import uuid
import time


def get_utc_timestamp(seconds=None):
    return time.strftime("%Y-%m-%dT%H:%M:%S.00Z", time.gmtime(seconds))


class AlexaResponse:

    def __init__(self, **kwargs):

        self.context_properties = []
        self.payload_endpoints = []

        # Set up the response structure
        self.context = {}
        self.event = {
            "header": {
                "namespace": kwargs.get("namespace", "Alexa"),
                "name": kwargs.get("name", "Response"),
                "messageId": str(uuid.uuid4()),
                "payloadVersion": kwargs.get("payload_version", "3")
            },
            "endpoint": {
                "scope": {
                    "type": "BearerToken",
                    "token": kwargs.get("token", "INVALID")
                },
                "endpointId": kwargs.get("endpoint_id", "INVALID")
            },
            "payload": kwargs.get("payload", {})
        }

        if "correlation_token" in kwargs:
            self.event["header"]["correlation_token"] =\
                kwargs.get("correlation_token", "INVALID")

        if "cookie" in kwargs:
            self.event["endpoint"]["cookie"] = kwargs.get("cookie", "{}")

        # No endpoint in an AcceptGrant or Discover request
        if (self.event["header"]["name"] == "AcceptGrant.Response"
           or self.event["header"]["name"] == "Discover.Response"):
            self.event.pop("endpoint")

    def add_context_property(self, **kwargs):
        self.context_properties.append(self.create_context_property(**kwargs))

    def add_cookie(self, key, value):

        if "cookies" in self is None:
            self.cookies = {}

        self.cookies[key] = value

    def add_payload_endpoint(self, **kwargs):
        self.payload_endpoints.append(self.create_payload_endpoint(**kwargs))

    def create_context_property(self, **kwargs):
        return {
            "namespace": kwargs.get("namespace", "Alexa.EndpointHealth"),
            "name": kwargs.get("name", "connectivity"),
            "value": kwargs.get("value", {"value": "OK"}),
            "timeOfSample": get_utc_timestamp(),
            "uncertaintyInMilliseconds": kwargs.get(
                "uncertainty_in_milliseconds", 0)
        }

    def create_payload_endpoint(self, **kwargs):
        # Return the proper structure expected for the endpoint
        endpoint = {
            "capabilities": kwargs.get("capabilities", []),
            "description": kwargs.get("description", "Custom Smart Device"),
            "displayCategories": kwargs.get("display_categories", ["OTHER"]),
            "endpointId": kwargs.get("endpoint_id", "endpoint_0"),
            "friendlyName": kwargs.get("friendly_name", "NULL"),
            "manufacturerName": kwargs.get("manufacturer_name",
                                           "Tanno Holmes Ideas")
        }

        if "cookie" in kwargs:
            endpoint["cookie"] = kwargs.get("cookie", {})

        return endpoint

    def create_payload_endpoint_capability(self, **kwargs):
        capability = {
            "type": kwargs.get("type", "AlexaInterface"),
            "interface": kwargs.get("interface", "Alexa"),
            "version": kwargs.get("version", "3")
        }
        supported = kwargs.get("supported", None)
        if supported:
            capability["properties"] = {}
            capability["properties"]["supported"] = supported
            capability["properties"]["proactivelyReported"] =\
                kwargs.get("proactively_reported", True)
            capability["properties"]["retrievable"] =\
                kwargs.get("retrievable", True)
        return capability

    def get(self, remove_empty=True):

        response = {
            "context": self.context,
            "event": self.event
        }

        if len(self.context_properties) > 0:
            response["context"]["properties"] = self.context_properties

        if len(self.payload_endpoints) > 0:
            response["event"]["payload"]["endpoints"] = self.payload_endpoints

        if remove_empty:
            if len(response["context"]) < 1:
                response.pop("context")

        return response

    def set_payload(self, payload):
        self.event["payload"] = payload

    def set_payload_endpoint(self, payload_endpoints):
        self.payload_endpoints = payload_endpoints

    def set_payload_endpoints(self, payload_endpoints):
        if "endpoints" not in self.event["payload"]:
            self.event["payload"]["endpoints"] = []

        self.event["payload"]["endpoints"] = payload_endpoints
