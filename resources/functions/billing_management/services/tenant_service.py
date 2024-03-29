
from http_client.client import *
from services.subscription_service import cancel_subscription

resource_name = 'companies'

def create_tenant(detail):
    print("Request received to create new tenant in Moesif (i.e. Moesif company)")
    moesif_company = {}
    moesif_company['company_id'] = company_id = detail.get('tenantId')
    if 'email' in detail:
        moesif_company['company_domain'] = detail.get('email').split('@')[-1]
    moesif_company['metadata'] = detail.data
    print(f'Creating company company_id={moesif_company['company_id']}')
    return request_moesif_resource('POST', f'{resource_name}', moesif_company)

def get_tenant(tenant_id):
    print("Request received to create new tenant in Moesif (i.e. Moesif company)")
    return request_moesif_resource('GET', f'{resource_name}/{tenant_id}', None)

def deprovision_tenant(detail):
    print("Request received to delete company from Moesif")
    company_id = detail.get('tenantId')
    print(f'Deprovision company company_id={company_id}')

    company = request_moesif_resource('GET', f'{resource_name}/{company_id}', None)
    # Cancel all subscriptions for this company
    if (company and company.get('subscriptions')):
        for sub in company.get('subscriptions'):
            res = cancel_subscription(sub.get('subscription_id'))
            print(res)
    # Uncomment below line if you want to delete company object in Moesif.
    # Without below, the subscription will remain in a cancelled state in both Moesif and billing provider.
    # request_moesif_resource('DELETE', f'{resource_name}/{company_id}', None)
    return company