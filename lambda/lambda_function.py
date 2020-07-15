import json
from AlexaResponse import AlexaResponse
from SmartHomeRequest import SmartHomeRequest


def lambda_handler(request, context):

    # Dump the request for logging - check the CloudWatch logs
    print("lambda_handler request  -----")
    print(json.dumps(request))

    if context is not None:
        print("lambda_handler context  -----")
        print(context)

    # Validate we have an Alexa directive
    if "directive" not in request:
        aer = AlexaResponse(
            name="ErrorResponse",
            payload={"type": "INVALID_DIRECTIVE",
                     "message": "Missing key: directive, " +
                     "Is the request a valid Alexa Directive?"})
        return send_response(aer.get())

    # Check the payload version
    payload_version = request["directive"]["header"]["payloadVersion"]
    if payload_version != "3":
        aer = AlexaResponse(
            name="ErrorResponse",
            payload={"type": "INTERNAL_ERROR",
                     "message": "This skill only supports Smart Home API v3."})
        return send_response(aer.get())

    # Crack open the request and see what is being requested
    name = request["directive"]["header"]["name"]
    namespace = request["directive"]["header"]["namespace"]

    # Handle the incoming request from Alexa based on the namespace

    if namespace == "Alexa.Authorization":
        if name == "AcceptGrant":
            # Note: This sample accepts any grant request
            grant_code = request["directive"]["payload"]["grant"]["code"]
            grantee_token = request["directive"]["payload"]["grantee"]["token"]
            print(grant_code)
            print(grantee_token)
            aar = AlexaResponse(namespace="Alexa.Authorization",
                                name="AcceptGrant.Response")
            return send_response(aar.get())

    if namespace == "Alexa.Discovery":
        if name == "Discover":
            smart_home_response = SmartHomeRequest.send_discover_request()
            if smart_home_response is None:
                return endpoint_unreachable()
            adr = AlexaResponse(namespace="Alexa.Discovery",
                                name="Discover.Response",
                                payload=smart_home_response)
            return send_response(adr.get())

    if namespace.endswith("Controller") or namespace.endswith("Sensor"):
        endpoint_id, correl_token, token = get_directive_properties(request)

        smart_home_response = SmartHomeRequest.send_directive_request(request)
        # Check for an error when setting the state
        if smart_home_response is None:
            return endpoint_unreachable()

        apcr = AlexaResponse(correlation_token=correl_token,
                             endpoint_id=endpoint_id,
                             token=token)
        apcr.add_context_properties(smart_home_response)
        return send_response(apcr.get())

    if namespace == "Alexa" and name == "ReportState":
        endpoint_id, correl_token, token = get_directive_properties(request)

        smart_home_response = SmartHomeRequest.send_status_request(endpoint_id)

        if smart_home_response is None:
            return endpoint_unreachable()

        apcr = AlexaResponse(correlation_token=correl_token,
                             endpoint_id=endpoint_id,
                             token=token,
                             name="StateReport")
        apcr.add_context_properties(smart_home_response)
        return send_response(apcr.get())


def get_directive_properties(request):
    endpoint_id = request["directive"]["endpoint"]["endpointId"]
    correlation_token = request["directive"]["header"]["correlationToken"]
    token = request["directive"]["endpoint"]["scope"]["token"]
    return endpoint_id, correlation_token, token


def endpoint_unreachable():
    return AlexaResponse(
        name="ErrorResponse",
        payload={"type": "ENDPOINT_UNREACHABLE",
                 "message": "Unable to reach endpoint database."}
    ).get()


def send_response(response):
    # TODO Validate the response
    print("lambda_handler response -----")
    print(json.dumps(response))
    return response
