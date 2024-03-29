from http_client.client import *

resource_name = 'users' 

def get_user_id(detail):
    return detail.get('userId') or detail.get('user_id') or detail.get('userName') or detail.get('user_name')

def create_user(detail):
    print("Request received to create new user in Moesif")
    moesif_user = {}
    moesif_user['user_id'] = get_user_id(detail)
    moesif_user['company_id'] = detail.get('tenantId')
    moesif_user['metadata'] = detail.data
    print(f'Creating user for user_id={moesif_user['user_id']}')
    return request_moesif_resource('POST', f'{resource_name}', moesif_user)

def delete_user(detail):
    print("Request received to delete user from Moesif")
    user_id = get_user_id(detail)
    return request_moesif_resource('DELETE', f'{resource_name}/{user_id}', None)