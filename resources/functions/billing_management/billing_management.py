import json
import http.client
import os
from services.subscription_service import *
from services.tenant_service import *
from services.user_service import *

moesif_management_api_key = os.environ['MOESIF_MANAGEMENT_API_KEY'].replace('Bearer ', '')
moesif_management_base_url = os.environ['MOESIF_MANAGEMENT_BASE_URL']
billing_provider_slug = os.environ['BILLING_PROVIDER_SLUG']
billing_provider_secret_key = os.environ['BILLING_PROVIDER_SECRET_KEY']


def handler(event, context):
    print("Received event:", json.dumps(event))

    detail_type = event['detail-type']
    detail = event['detail']

    # DetailType defined in  https://github.com/awslabs/sbt-aws/blob/2463b9a751223aca90b6e4d95df374ca11342e97/src/utils/event-manager.ts#L12
    if detail_type == 'provisionSuccess':
        create_tenant(detail)
        create_subscription(detail)
    elif detail_type == 'deprovisionSuccess':
        deprovision_tenant(detail)
