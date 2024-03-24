from http_client.client import *
from datetime import datetime, timedelta

billing_provider_slug = os.environ['BILLING_PROVIDER_SLUG']
default_plan_id = os.environ['DEFAULT_PLAN_ID'] # Default plan to be used when creating new subscriptions
default_price_id = os.environ['DEFAULT_PRICE_ID'] # Default price to be used when creating new subscriptions

def create_subscription(detail):
    print("Request received to create new subscription")
    return create_provider_resources(detail)

def cancel_subscription(subscription_id):
    print(f'Request received to cancel subscription {subscription_id}')

    if (billing_provider_slug == 'stripe'):
        return request_stripe_resource('DELETE', f'subscriptions/{subscription_id}', None)
    if (billing_provider_slug == 'chargebee'):
        return request_chargebee_resource('POST', f'subscriptions/{subscription_id}/cancel_for_items', None)
    if (billing_provider_slug == 'zuora'):
        return request_zuora_resource('POST', f'subscriptions/{subscription_id}/cancel', {
            'cancel_date': datetime.utcnow().strftime('%Y-%m-%d')
        })
    if (billing_provider_slug == 'custom'):
        return request_moesif_resource('POST', f'subscriptions/{subscription_id}', None)

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
    elif (billing_provider_slug == 'chargebee'):
        new_customer = {
            'id': detail['tenantId'],
            'email': f'{detail['tenantId']}@example.com', # FIXME Need Email for Billing
            'meta_data[company_id]':  detail['tenantId']
        }
        customer = request_chargebee_resource('POST', 'customers', new_customer)
        print(json.dumps(customer))
        new_subscription = {
            'customer': detail['tenantId'],
            'subscription_items[item_price_id][0]': default_price_id
        }
        subscription_url = f'customers/{detail['tenantId']}/subscription_for_items'
        return request_chargebee_resource('POST', subscription_url, new_subscription)
    elif (billing_provider_slug == 'zuora'):
        new_customer = {
            'account_number': detail['tenantId'],
            "name": detail['tenantId'],
            'currency': 'USD', # FIXME should be set by tenant
            'bill_to': {
                'first_name': detail['tenantId'],
                'last_name': detail['tenantId'],
                'work_email': f'{detail['tenantId']}@example.com', # FIXME Need Email for Billing
                'address': {
                    'country': "USA", # FIXME should be set by tenant
                    'state': "CA"
                }
            }
        }
        customer = request_zuora_resource('POST', 'accounts', new_customer)
        print(json.dumps(customer))
        new_subscription = {
            'account_number': detail['tenantId'],
            'subscription_plans': [{
                'plan_id': default_plan_id,
                'prices': [{
                    'price_id': default_price_id
                }]
            }]
        }
        return request_zuora_resource('POST', 'subscriptions', new_subscription)
    elif (billing_provider_slug == 'custom'):
        current_time= datetime.utcnow()
        new_subscription = {
            'company_id': detail.get('tenantId'),
            'subscription_id': detail.get('tenantId'),
            'status': 'active',
            'items': [{
                'plan_id': default_plan_id
            }],
            'current_period_start': current_time.isoformat(),
            'current_period_end': (current_time + timedelta(days=365)).isoformat(), # For now, assume one year subscription
        }
        return request_moesif_resource('POST', 'subscriptions', new_subscription)
