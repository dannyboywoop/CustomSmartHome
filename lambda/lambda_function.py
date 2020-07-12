import json
from AlexaResponse import AlexaResponse


def lambda_handler(request, context):

    # Dump the request for logging - check the CloudWatch logs
    print('lambda_handler request  -----')
    print(json.dumps(request))

    if context is not None:
        print('lambda_handler context  -----')
        print(context)

    # Validate we have an Alexa directive
    if 'directive' not in request:
        aer = AlexaResponse(
            name='ErrorResponse',
            payload={'type': 'INVALID_DIRECTIVE',
                     'message': 'Missing key: directive, Is the request a valid Alexa Directive?'})
        return send_response(aer.get())

    # Check the payload version
    payload_version = request['directive']['header']['payloadVersion']
    if payload_version != '3':
        aer = AlexaResponse(
            name='ErrorResponse',
            payload={'type': 'INTERNAL_ERROR',
                     'message': 'This skill only supports Smart Home API version 3'})
        return send_response(aer.get())

    # Crack open the request and see what is being requested
    name = request['directive']['header']['name']
    namespace = request['directive']['header']['namespace']

    # Handle the incoming request from Alexa based on the namespace

    if namespace == 'Alexa.Authorization':
        if name == 'AcceptGrant':
            # Note: This sample accepts any grant request
            # In your implementation you would use the code and token to get and store access tokens
            grant_code = request['directive']['payload']['grant']['code']
            grantee_token = request['directive']['payload']['grantee']['token']
            aar = AlexaResponse(namespace='Alexa.Authorization', name='AcceptGrant.Response')
            return send_response(aar.get())

    if namespace == 'Alexa.Discovery':
        if name == 'Discover':
            adr = AlexaResponse(namespace='Alexa.Discovery', name='Discover.Response')
            capability_alexa = adr.create_payload_endpoint_capability()
            capability_alexa_percentagecontroller = adr.create_payload_endpoint_capability(
                interface='Alexa.PercentageController',
                supported=[{'name': 'percentage'}])
            adr.add_payload_endpoint(
                friendly_name='Blinds',
                endpoint_id='smart_blind_01',
                description='Custom Smart Blind',
                display_categories=['INTERIOR_BLIND'],
                capabilities=[capability_alexa, capability_alexa_percentagecontroller])
            return send_response(adr.get())

    if namespace == 'Alexa.PercentageController':
        # Note: This sample always returns a success response for either a request to TurnOff or TurnOn
        endpoint_id = request['directive']['endpoint']['endpointId']
        correlation_token = request['directive']['header']['correlationToken']
        token = request['directive']['endpoint']['scope']['token']
        
        if name == 'SetPercentage':
            percentage = request['directive']['payload']['percentage']
            state_set = set_device_state(endpoint_id=endpoint_id, state='percentage', value=percentage)
            final_percentage = percentage
        
        if name == 'AdjustPercentage':
            percentageDelta = request['directive']['payload']['percentageDelta']
            state_set = set_device_state(endpoint_id=endpoint_id, state='percentageDelta', value=percentageDelta)
            final_percentage = 50

        # Check for an error when setting the state
        if not state_set:
            return AlexaResponse(
                name='ErrorResponse',
                payload={'type': 'ENDPOINT_UNREACHABLE', 'message': 'Unable to reach endpoint database.'}).get()

        apcr = AlexaResponse(correlation_token=correlation_token, endpoint_id=endpoint_id, token=token)
        apcr.add_context_property(namespace='Alexa.PercentageController', name="percentage", value=final_percentage)
        return send_response(apcr.get())
    
    if namespace == 'Alexa' and name == 'ReportState':
        endpoint_id = request['directive']['endpoint']['endpointId']
        correlation_token = request['directive']['header']['correlationToken']
        token = request['directive']['endpoint']['scope']['token']
        
        
        state = get_device_state(endpoint_id)
        if state is None:
            return AlexaResponse(
                name='ErrorResponse',
                payload={'type': 'ENDPOINT_UNREACHABLE', 'message': 'Unable to reach endpoint database.'}).get()
        
        apcr = AlexaResponse(correlation_token=correlation_token, endpoint_id=endpoint_id, token=token, name='StateReport')
        apcr.add_context_property(namespace='Alexa.PercentageController', name="percentage", value=state)
        return send_response(apcr.get())


def send_response(response):
    # TODO Validate the response
    print('lambda_handler response -----')
    print(json.dumps(response))
    return response


def set_device_state(endpoint_id, state, value):
    print(value)
    return True


def get_device_state(endpoint_id):
    return 70