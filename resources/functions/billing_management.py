import json
import http.client
import os

def handler(event, context):
    print("Received event:", json.dumps(event))

    id = event['id']
    source = event['source']
    detail_type = event['detail-type']
    detail = event['detail']
    time = event['time']

    # DetailType defined in  https://github.com/awslabs/sbt-aws/blob/2463b9a751223aca90b6e4d95df374ca11342e97/src/utils/event-manager.ts#L12
    if detail_type == 'provisionSuccess':
        create_user(detail)
    elif detail_type == 'onboardingRequest':
        create_user(detail)
    elif detail_type == 'deprovisionSuccess':
        delete_user(detail)

def create_user(detail):
    # FIXME Assuming user data is in the request body in Moesif format
    print("Request received to create new user in Moesif")
    moesif_user = {}
    moesif_user['user_id'] = detail.get('user_name') or detail.get('userName') or detail.get('tenant_id') or detail.get('tenantId')
    moesif_user['metadata'] = detail
    print("Creating user " + json.dumps(moesif_user))
    return update_resource(moesif_user, 'POST', 'users')

def delete_user(detail):
    print("Request received to delete user from Moesif")
    user_id = detail.get('user_name') or detail.get('userName') or detail.get('tenant_id') or detail.get('tenantId')
    # FIXME Assuming username in param
    return update_resource(None, 'DELETE', f'users/{user_id}')

def update_resource(payload, method, resource):
    management_api_key = os.environ['MOESIF_MANAGEMENT_API_KEY'].replace('Bearer ', '')
    base_url = os.environ['MOESIF_MANAGEMENT_BASE_URL']
    conn = http.client.HTTPSConnection(base_url.replace('https://', ''), 443)
    payload_str = json.dumps(payload) if payload else None

    # Retry HTTP requests up to 3 times
    retry = 3
    while retry:
        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {management_api_key}'
            }
            conn.request(method, f'/v1/search/~/{resource}', payload_str, headers)
            
            response = conn.getresponse()
            response_body = response.read().decode('utf-8')
            print(response.status)
            return {
                'statusCode': response.status,
                'body': response_body
            }
        except Exception as e:
            print(e)
            print(payload) 
            if not retry:
                raise e
            print(f'Retrying... Attempt {3 - retry}')
            retry -= 1