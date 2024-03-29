import base64
import json
import http.client
import os
from urllib.parse import urlencode

moesif_management_api_key = os.environ['MOESIF_MANAGEMENT_API_KEY'].replace('Bearer ', '')
moesif_management_base_url = os.environ['MOESIF_MANAGEMENT_BASE_URL']
billing_provider_slug = os.environ['BILLING_PROVIDER_SLUG']
billing_provider_secret_key = os.environ['BILLING_PROVIDER_SECRET_KEY']
billing_provider_client_id = os.environ['BILLING_PROVIDER_CLIENT_ID']
billing_provider_base_url = os.environ['BILLING_PROVIDER_BASE_URL']

def request_moesif_resource(method, resource, payload):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {moesif_management_api_key}'
    }
    path = f'/v1/search/~/{resource}'
    return request(moesif_management_base_url, method, path, headers, payload, json.dumps)

def request_stripe_resource(method, resource, payload):
    basic_auth = base64.b64encode(f'{billing_provider_secret_key}:'.encode('utf-8')).decode('utf-8')
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {basic_auth}'
    }
    path = f'/v1/{resource}'
    return request('https://api.stripe.com', method, path, headers, payload, urlencode)

def request_chargebee_resource(method, resource, payload):
    basic_auth = base64.b64encode(f'{billing_provider_secret_key}:'.encode('utf-8')).decode('utf-8')
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {basic_auth}'
    }
    path = f'/api/v2/{resource}'
    return request(billing_provider_base_url, method, path, headers, payload, urlencode)

def request_zuora_resource(method, resource, payload):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'grant_type': "client_credentials",
        'client_id': billing_provider_client_id,
        'client_secret': billing_provider_secret_key
    }
    auth_response = request(billing_provider_base_url, 'POST', '/oauth/token', headers, data, urlencode, False)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {auth_response['access_token']}'
    }
    path = f'/v2/{resource}'
    return request(billing_provider_base_url, method, path, headers, payload, json.dumps)

def request(base_url, method, path, headers, payload, serialize, log_payload = True):
    conn = http.client.HTTPSConnection(base_url.replace('https://', ''), 443)

    print(f'Making request to {method} {base_url}{path}')
    payload_str = serialize(payload) if payload else None

    if (log_payload):
        print(payload_str)

    # Retry HTTP requests up to 3 times
    retry = 3
    while retry:
        try:
            conn.request(method, path, payload_str, headers)
            response = conn.getresponse()
            print(f'response.status={response.status}')
            response_body = response.read().decode('utf-8')
            if (log_payload):
                print(response_body.replace('\n', '').replace('\r',''))
            if response.status >= 400:
                raise Exception(f'HTTP error {response.status}')
            return json.loads(response_body)
        except Exception as e: 
            print(e)
            if not retry:
                raise e
            print(f'Retrying... Attempt {3 - retry}')
            retry -= 1
