import requests
import time
import os   # for environment variables
from requests.models import PreparedRequest
import json

# Authorization Code Grant Flow
# https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow
def auth_code_flow(tenant_id, client_id, redirect_uri, scope, state, response_mode='query', code_challenge=None, code_challenge_method=None):
    # Construct the authorization URL
    auth_endpoint = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize'

    params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'response_mode': response_mode, # query is the default for response_type code, so it's optional but recommended to include
        'scope': scope, #'https://graph.microsoft.com/.default' #Example
        'state': state 
    }
    
    # For PKCE scenarios, include the code_challenge and code_challenge_method
    if code_challenge is not None:
        params['code_challenge'] = code_challenge
        if code_challenge_method is not None:
            params['code_challenge_method'] = code_challenge_method

    # Prepare the URL for Authentication (AuthN) request
    req = PreparedRequest()
    req.prepare_url(auth_endpoint, params)

    #!NOTE: This flow requires user interaction, thus we don't make a request
    return req.url # Copy url and paste to sign-in with browser

    # Here you would typically redirect the user to the authorization URL in 
    #  the App, & capture the auth_code  from the redirect URL fragment.


# Hybrid Flow (ID Token + Access Token) - Requires user interaction
# https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow#request-an-id-token-as-well-or-hybrid-flow
def hybrid_flow(tenant_id, client_id, redirect_uri, response_type , response_mode, scope, state, nonce, code_challenge=None, code_challenge_method=None):
    # Construct the authorization URL
    auth_endpoint = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize'
    params = {
        'client_id': client_id,
        'response_type': response_type, # 'code id_token token',
        'redirect_uri': redirect_uri,
        'response_mode': response_mode, # 'fragment',
        'scope': scope, #'openid profile offline_access https://graph.microsoft.com/.default' #Example
        'state': state, #'A1B2C3D4E5F6'
        'nonce': nonce #'123456'
    }

    # For PKCE scenarios, include the code_challenge and code_challenge_method
    if code_challenge is not None:
        params['code_challenge'] = code_challenge
        if code_challenge_method is not None:
            params['code_challenge_method'] = code_challenge_method

    # Prepare the URL for Authentication (AuthN) request
    req = PreparedRequest()
    req.prepare_url(auth_endpoint, params)

    #!NOTE: This flow requires user interaction, thus we don't make a request
    return req.url # Copy url and paste to sign-in with browser

    # Here you would typically redirect the user to the authorization URL in 
    #  the App, & capture the ID token and access token from the redirect URL fragment.


# Client Credentials Grant Flow
# https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-client-creds-grant-flow
def client_credentials_flow(client_id, tenant_id, scope, client_secret):
    token_endpoint = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': scope#'https://graph.microsoft.com/.default'
    }
    response = requests.post(token_endpoint, data=data)
    access_token = response.json().get('access_token')
    return access_token


# Device Code Flow
# https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-device-code
def device_code_flow(tenant_id, client_id, scope):
    device_auth_endpoint = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/devicecode'
    data = {
        'client_id': client_id,
        'scope': scope #'openid profile email user.read' #Example
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(device_auth_endpoint, data=data, headers=headers)
    device_code = response.json().get('device_code')
    verification_uri = response.json().get('verification_uri')
    user_code = response.json().get('user_code') 
    expires_in = response.json().get('expires_in') # The number of seconds the device code is valid for
    interval = response.json().get('interval') # The number of seconds to wait before polling the token endpoint
    message = response.json().get('message') # A message to display to the user
    print('Interval:', interval)
    print('Device Code:', device_code)
    print('Verification URI:', verification_uri)
    print('User Code:', user_code)
    print('Expires In:', expires_in)
    print('Message:', message)

    # Token endpoint
    token_endpoint = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
    data = {
        'client_id': client_id,
        'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
        'device_code': device_code
    }

    access_token = ''
    refresh_token = ''
    id_token = ''
    # Poll the token endpoint until the user completes the flow
    while True:
        response = requests.post(token_endpoint, data=data)
        if response.status_code == 200:
            access_token = response.json().get('access_token')
            refresh_token = response.json().get('refresh_token')
            id_token = response.json().get('id_token')

            print(f'\n\nSuccessful Auth response:')
            print_raw_http_response(response)
            print(f'\n\n')
            break
        elif response.status_code == 400:
            error = response.json().get('error')
            if error == 'authorization_pending': # The user has not completed flow
                # Poll the token endpoint after the interval
                print(f'Error "{error}":  Waiting for user to complete the flow...')
                time.sleep(interval) 
            elif error == 'slow_down': # We are polling too frequently
                print(f'Error "{error}":  We are polling too frequently...')
                interval = response.json().get('interval') + 5
                time.sleep(interval)
                print(f'\t- Interval Set to {interval} seconds')
            elif error == 'authorization_declined':
                # Stop polling and revert to an unauthenticated state.
                print(f'Error "{error}": User denied AuthZ - ', response.json().get('authorization_declined'))
                break
            elif error == 'bad_verification_code':
                # Stop polling and revert to an unauthenticated state.
                print(f'Error "{error}":\n' + '\t- The device_code sent to the /token endpoint was incorrect:', response.json().get('bad_verification_code'))
                break
                #expired_token
            elif error == 'expired_token':
                # Stop polling and revert to an unauthenticated state.
                print(f'Error "{error}":\n' + 'Token Expired -', response.json().get('expired_token'))
                break
            else:
                # An error occurred
                print('Error:', response.json().get('error_description'))
                break
        else:
            # An error occurred
            print('Error:', response.json())
            break
    
    return access_token, refresh_token, id_token


# On-Behalf-Of Flow
# https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-on-behalf-of-flow
def on_behalf_of_flow(tenant_id, client_id, assertion, scope, client_secret=None, client_assertion=None, code_verifier=None, requested_token_type=None):
    # Token endpoint
    token_endpoint = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
    data = {
        'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        'client_id': client_id,
        'assertion': assertion, #'your_access_token',
        'scope': scope, #'openid profile email',
        'requested_token_use': 'on_behalf_of'
    }

    # If using client_secret
    if client_secret is not None:
        data['client_secret'] = client_secret

    # For confidential clients, include the client_assertion and client_assertion_type
    if client_assertion is not None:
        data['client_assertion'] = client_assertion
        client_assertion_type = 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer'
        data['client_assertion_type'] = client_assertion_type

    if code_verifier is not None:
        data['code_verifier'] = code_verifier

    # For APIs requiring a SAML tokens
    if requested_token_type is not None: 
        data['requested_token_type'] = requested_token_type
        # The value can be urn:ietf:params:oauth:token-type:saml2 or urn:ietf:params:oauth:token-type:saml1 depending on the requirements of the accessed resource.

    access_token = ''
    refresh_token = ''
    id_token = ''

    response = requests.post(token_endpoint, data=data)
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        refresh_token = response.json().get('refresh_token')
        id_token = response.json().get('id_token')
        return access_token, refresh_token, id_token
    elif response.status_code == 400:
        error = response.json().get('error')
        error_description = response.json().get('error_description')
        error_uri = response.json().get('error_uri')
        print('Error:', error)
        print('Error Description:', error_description)
        print(f'Error URI: {error_uri}\n')
    else:
        print('HTTP Status Code:', response.status_code)
        print('HTTP Response: {response.text}\n')

    # Return the access token, refresh token, and ID token
    return access_token, refresh_token, id_token # Note: The ID token and refresh token are only returned if supported


# Implicit Grant Flow
# https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-implicit-grant-flow
def implicit_flow(tenant_id, client_id, redirect_uri, response_type, scope, response_mode='fragment', nonce='123456'):
    # Construct the authorization URL
    auth_endpoint = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize'
    params = {
        'client_id': client_id,
        'response_type': response_type, #'id_token token', 
        'redirect_uri': redirect_uri,
        'response_mode': response_mode, #'fragment', # Defaults to query for just an access token, but fragment if the request includes an id_token.
        'scope': scope, #'openid',
        'nonce': nonce
    }

    # Prepare the URL for Authentication (AuthN) request
    req = PreparedRequest()
    req.prepare_url(auth_endpoint, params)

    #!NOTE: This flow requires user interaction, thus we don't make a request
    return req.url # Copy url and paste to sign-in with browser

    # Here you would typically redirect the user to the authorization URL, 
    # then capture the ID token and access token from the redirect URL fragment.


# Resource Owner Password Credentials Grant Flow
# https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth-ropc
def ropc(tenant_id, client_id, username, password, scope, client_secret=None, client_assertion=None):
    # Token endpoint
    token_endpoint = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
    data = {
        'client_id': client_id,
        'scope': scope,
        'username': username,
        'password': password,
        'grant_type': 'password'
    }

    if client_secret is not None:
        data['client_secret'] = client_secret

    # For confidential clients, include the client_assertion and client_assertion_type
    if client_assertion is not None:
        data['client_assertion'] = client_assertion
        data['client_assertion_type'] = 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer'
    
    print(data)

    data_query_string = '&'.join([f'{key}={value}' for key, value in data.items()])
    print(data_query_string)

    access_token = ''
    refresh_token = ''
    id_token = ''

    response = requests.post(token_endpoint, data=data_query_string)
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        refresh_token = response.json().get('refresh_token')
        id_token = response.json().get('id_token')
        return access_token, refresh_token, id_token
    elif response.status_code == 400:
        error = response.json().get('error')
        error_description = response.json().get('error_description')
        error_uri = response.json().get('error_uri')
        print('Error:', error)
        print('Error Description:', error_description)
        print('Error URI:', error_uri)
    else:
        print('HTTP Status Code:', response.status_code)
        print('HTTP Response: {response.text}\n')

    # Return the access token, refresh token, and ID token
    return access_token, refresh_token, id_token


def request_access_token(tenant_id, client_id, redirect_uri, auth_code, client_secret=None, client_assertion=None, code_verifier=None):
    # Exchange the authorization code for an access token
    token_endpoint = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
    }

    # If using client_secret
    if client_secret is not None:
        data['client_secret'] = client_secret

    # For confidential clients, include the client_assertion and client_assertion_type
    if client_assertion is not None:
        data['client_assertion'] = client_assertion
        client_assertion_type = 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer'
        data['client_assertion_type'] = client_assertion_type

    if code_verifier is not None:
        data['code_verifier'] = code_verifier

    access_token = ''
    refresh_token = ''
    id_token = ''

    response = requests.post(token_endpoint, data=data)
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        refresh_token = response.json().get('refresh_token')
        id_token = response.json().get('id_token')
        return access_token, refresh_token, id_token
    elif response.status_code == 400:
        error = response.json().get('error')
        error_description = response.json().get('error_description')
        error_uri = response.json().get('error_uri')
        print('Error:', error)
        print('Error Description:', error_description)
        print('Error URI:', error_uri)
    else:
        print('HTTP Status Code:', response.status_code)
        print('HTTP Response: {response.text}\n')

    # Return the access token, refresh token, and ID token
    return access_token, refresh_token, id_token


# Refresh Token
# https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow
def refresh_token(tenant_id, client_id, refresh_token, client_secret, scope=None):
    token_endpoint = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
    data = {
        'grant_type': 'refresh_token',
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token
    }
    if scope is not None:
        data['scope'] = scope

    access_token = ''
    refresh_token = ''
    id_token = ''

    response = requests.post(token_endpoint, data=data)
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        refresh_token = response.json().get('refresh_token')
        id_token = response.json().get('id_token')
        return access_token, refresh_token, id_token
    elif response.status_code == 400:
        error = response.json().get('error')
        error_description = response.json().get('error_description')
        error_uri = response.json().get('error_uri')
        print('Error:', error)
        print('Error Description:', error_description)
        print(f'Error URI: {error_uri}\n')
    else:
        print('HTTP Status Code:', response.status_code)
        print(f'HTTP Response: {response.text}\n')

    # Return the access token, refresh token, and ID token
    return access_token, refresh_token, id_token


def print_raw_http_response(response):
    # Print the status line
    print(f'HTTP/{response.raw.version} {response.status_code} {response.reason}')
    #print(f'HTTP/{response.raw.version} {response.status_code} {response.reason}')

    # Print the headers
    for key, value in response.headers.items():
        print(f'{key}: {value}')
    
    # Print a blank line to separate headers from the body
    print()
    
    # Check if the response is JSON and pretty print it
    if 'application/json' in response.headers.get('Content-Type', ''):
        try:
            json_data = response.json()
            print(json.dumps(json_data, indent=4))
        except ValueError:
            # In case the response body could not be parsed as JSON
            print(response.text)
    else:
        # Print the response body as is for non-JSON responses
        print(response.text)
