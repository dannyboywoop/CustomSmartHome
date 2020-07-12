import socket


class HTTPPostRequest():

    POST_Request = """\
POST /{0} HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: {1}

{2}"""

    DOMAIN = "tannoholmes.ddns.net"
    PORT = "80"

    def __init__(self, clientId, directive, value):
        self.clientId = clientId
        self.directive = directive
        self.value = value

        self.body = "directive={0}&value={1}".format(directive, value)
        self.content_length = len(self.body)
        self.request = self.POST_Request.format(clientId,
                                                self.content_length,
                                                self.body)

    def send_request(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.DOMAIN, self.PORT))

        s.sendall(self.request.encode("utf-8"))
        s.close()
