from http_client.client import *

billing_provider_slug = os.environ['BILLING_PROVIDER_SLUG']
default_price_id = os.environ['DEFAULT_PRICE_ID'] # Default price to be used when creating new subscriptions

def create_subscription(detail):
    print("Request received to create new subscription")
    return create_provider_resources(detail)

def cancel_subscription(subscription_id):
    print(f'Request received to cancel subscription {subscription_id}')

    if (billing_provider_slug == 'stripe'):
        request_stripe_resource('DELETE', f'subscriptions/{subscription_id}', None)

def create_provider_resources(detail):
    # Not required to create a subscription in Moesif as provider will push this directly to Moesif
    if (billing_provider_slug == 'stripe'):
        new_customer = {
            'email': f'{detail['tenantId']}@example.com', # FIXME Need Email for Billing
            'metadata[company_id]':  detail['tenantId']
        }
        customer = request_stripe_resource('POST', 'customers', new_customer)
        print(json.dumps(customer))
        new_subscription = {
            'customer': customer.get('id'),
            'items[0][price]': default_price_id
        }
        return request_stripe_resource('POST', 'subscriptions', new_subscription)
    
