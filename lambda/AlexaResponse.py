import uuid
import time


def get_utc_timestamp(seconds=None):
    return time.strftime("%Y-%m-%dT%H:%M:%S.00Z", time.gmtime(seconds))


class AlexaResponse:

    MANUFACTURER_NAME = "Tanno Holmes Ideas"
    INTERFACE_TYPE = "AlexaInterface"
    INTERFACE_VERSION = "3"

    def __init__(self,
                 namespace="Alexa",
                 name="Response",
                 token="INVALID",
                 endpoint_id="INVALID",
                 payload={},
                 correlation_token=None,
                 cookie=None):

        self.context_properties = []

        # Set up the response structure
        self.context = {}
        self.event = {
            "header": {
                "namespace": namespace,
                "name": name,
                "messageId": str(uuid.uuid4()),
                "payloadVersion": self.INTERFACE_VERSION
            },
            "endpoint": {
                "scope": {
                    "type": "BearerToken",
                    "token": token
                },
                "endpointId": endpoint_id
            },
            "payload": payload
        }

        if correlation_token:
            self.event["header"]["correlation_token"] = correlation_token

        if cookie:
            self.event["endpoint"]["cookie"] = cookie

        # No endpoint in an AcceptGrant or Discover request
        if (self.event["header"]["name"] == "AcceptGrant.Response"
           or self.event["header"]["name"] == "Discover.Response"):
            self.event.pop("endpoint")

    def add_cookie(self, key, value):

        if "cookies" in self is None:
            self.cookies = {}

        self.cookies[key] = value

    def add_context_properties(self, properties):
        if len(self.context_properties) == 0:
            self.context_properties = properties
        else:
            for prop in properties:
                self.context_properties.append(prop)

    def get(self, remove_empty=True):

        response = {
            "context": self.context,
            "event": self.event
        }

        if len(self.context_properties) > 0:
            response["context"]["properties"] = self.context_properties

        if remove_empty:
            if len(response["context"]) == 1:
                response.pop("context")

        return response
