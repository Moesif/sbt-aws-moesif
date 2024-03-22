from http_client.client import *

resource_name = 'users' 

def create_user(detail):
    print("Request received to create new user in Moesif")
    moesif_user = {}
    moesif_user['user_id'] = user_id = detail.get('userName')
    moesif_user['company_id'] = detail.get('tenantId')
    moesif_user['metadata'] = detail
    print("Creating user " + json.dumps(moesif_user))
    return request_moesif_resource('POST', f'{resource_name}', moesif_user)

def deprovision_user(detail):
    print("Request received to delete user from Moesif")
    user_id = detail.get('userName')
    return request_moesif_resource('DELETE', f'{resource_name}/{user_id}', None)