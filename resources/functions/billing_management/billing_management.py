import json
import http.client
import os
import sys
import traceback
from util.event_detail import *
from services.subscription_service import *
from services.tenant_service import *
from services.user_service import *

moesif_management_api_key = os.environ['MOESIF_MANAGEMENT_API_KEY'].replace('Bearer ', '')
moesif_management_base_url = os.environ['MOESIF_MANAGEMENT_BASE_URL']
billing_provider_slug = os.environ['BILLING_PROVIDER_SLUG']
billing_provider_secret_key = os.environ['BILLING_PROVIDER_SECRET_KEY']

header = '''name:       Moesif Billing Management
repository: https://github.com/Moesif/sbt-aws-moesif
license:    Apache-2.0
'''
print(header)
for k, v in os.environ.items():
    k = k.lower()
    if ('billing' in k or 'tenant' in k) and 'key' not in k:
        print(f"       {k}: {v}")

def handler(event, context):
    print("Received event:", json.dumps(event))

    detail_type = event['detail-type']
    detail = EventDetail(event['detail'])

    try:
        # DetailType defined in https://github.com/awslabs/sbt-aws/blob/main/src/utils/event-manager.ts
        if detail_type == 'onboardingRequest':
            create_tenant(detail)
            create_subscription(detail)
        elif detail_type == 'offboardingRequest':
            deprovision_tenant(detail)
        elif detail_type == 'tenantUserCreated':
            create_user(detail)
        elif detail_type == 'tenantUserDeleted':
            delete_user(detail)
    except Exception as e:
        print(e)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(f'Error handling {detail_type}')
        traceback.print_tb(exc_traceback)
        raise e

