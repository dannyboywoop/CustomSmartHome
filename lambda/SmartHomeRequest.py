from http.client import HTTPConnection
from json import loads, dumps


class SmartHomeRequest():
    @staticmethod
    def send_discover_request():
        return SmartHomeRequest._send_request("discover")

    @staticmethod
    def send_status_request(endpoint_id):
        return SmartHomeRequest._send_request("status", endpoint_id.encode())

    @staticmethod
    def send_directive_request(directive_json):
        return SmartHomeRequest._send_request("directive",
                                              dumps(directive_json))

    @staticmethod
    def _send_request(name, body=None):
        connection = HTTPConnection("tannoholmes.ddns.net", 80)
        connection.request("POST",
                           "/smarthome/"+name,
                           headers={"Content-Type": "text/json"},
                           body=body)
        response = connection.getresponse()
        if response.status == 200:
            return loads(response.read())
        else:
            return None
