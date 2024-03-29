from http_client.client import *
from datetime import datetime, timedelta

billing_provider_slug = os.environ['BILLING_PROVIDER_SLUG']
tenant_plan_field = os.environ['TENANT_PLAN_FIELD']
tenant_price_field = os.environ['TENANT_PRICE_FIELD']

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
            'email': detail.get_email(),
            'metadata[company_id]':  detail.get('tenantId')
        }
        customer = request_stripe_resource('POST', 'customers', new_customer)
        new_subscription = {
            'customer': customer.get('id'),
            'items[0][price]': detail.get(tenant_price_field)
        }
        return request_stripe_resource('POST', 'subscriptions', new_subscription)
    elif (billing_provider_slug == 'chargebee'):
        new_customer = {
            'id': detail.get('tenantId'),
            'email': detail.get_email(),
            'meta_data[company_id]':  detail.get('tenantId')
        }
        customer = request_chargebee_resource('POST', 'customers', new_customer)
        new_subscription = {
            'customer': detail.get('tenantId'),
            'subscription_items[item_price_id][0]': detail.get(tenant_price_field)
        }
        subscription_url = f'customers/{detail.get('tenantId')}/subscription_for_items'
        return request_chargebee_resource('POST', subscription_url, new_subscription)
    elif (billing_provider_slug == 'zuora'):
        new_customer = {
            'account_number': detail.get('tenantId'),
            "name": detail.get('tenantId'),
            'currency': detail.safe_get('currency', 'USD'),
            'bill_to': {
                'first_name': detail.safe_get('firstName', detail.get('tenantId')),
                'last_name': detail.safe_get('lastName', detail.get('tenantId')),
                'work_email': detail.get_email(),
                'address': {
                    'country': detail.safe_get_nested('address.country', 'USA'),
                    'state': detail.safe_get_nested('address.state', 'CA')
                }
            }
        }
        customer = request_zuora_resource('POST', 'accounts', new_customer)
        new_subscription = {
            'account_number': detail.get('tenantId'),
            'subscription_plans': [{
                'plan_id': detail.get(tenant_plan_field),
                'prices': [{
                    'price_id': detail.get(tenant_price_field)
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
                'plan_id': detail.get(tenant_plan_field)
            }],
            'current_period_start': current_time.isoformat(),
            'current_period_end': (current_time + timedelta(days=365)).isoformat(), # For now, assume one year subscription
        }
        return request_moesif_resource('POST', 'subscriptions', new_subscription)
