
## Long Description

Effortlessly monetize your APIs without writing a single line of code. Create advanced metering rules based on any attribute or metric of your API usage. Simply connect Moesif to your billing provider, and let Moesif do the heavy lifting. Moesif integrates seamlessly with payment gateways like Stripe, or your custom solutions via webhooks.

Design flexible pricing plans—prepaid, postpaid, pay-as-you-go (PAYG), and more. Enforce quotas and subscription terms through [governance rules](https://www.moesif.com/features/api-governance-rules). Built for scale, Moesif ensures precise invoicing, while its open-source developer portal enables a quick and comprehensive customer experience for managing subscriptions and usage.

### Accurate API Usage Metering:

* Track any usage metric—API transactions, compute resources, payload size, unique users, and beyond.
* Easily configure [prepaid, postpaid, tiered, PAYG, and other pricing models](https://www.moesif.com/features/product-catalog) with just a few clicks.
* Leverage built-in formulas, functions, and aggregations for ultimate flexibility in defining billable metrics.

### Automatic Invoicing with Your Existing Tools:

* Seamlessly connect to [billing providers](https://www.moesif.com/extensions/api-monetization) like Stripe and Zuora for automated invoicing and payments.
* Integrate with custom in-house solutions or platforms like AWS Marketplace via webhook triggers.
* With bi-directional sync, track subscriptions and instantly see how usage translates into revenue.

### Deliver a Superior Customer Experience:

* Use Moesif's [open-source developer portal](https://www.moesif.com/solutions/developer-portal) to launch a subscription management experience in record time.
* Provide [real-time insights](https://www.moesif.com/features/embedded-api-logs) to customers on their quotas and current usage with a few lines of code.
* [Automate email notifications](https://www.moesif.com/features/user-behavioral-emails) to customers on quota limits or integration issues with ease.

### Customizable Logic for Unique Billing Needs:

* Define billable metrics from fields in your API payloads, custom events, and more.
* Utilize Moesif’s powerful [scripting language](https://www.moesif.com/docs/metered-billing/scripted-fields/) to create new metrics from multiple fields—even retroactively.
* Take advantage of features like date math, numeric calculations, aggregations, and windowing functions.

Install the Moesif Plugin for SBT-AWS today and integrate the most powerful API analytics and monetization solution into your application.


## Installation Instructions


### Prerequisites

1. If you don't already have a SBT project deployed, follow [AWS SBT's tutorial](https://github.com/awslabs/sbt-aws/tree/main/docs/public) to deploy the sample `hello-cdk` project with a `ControlPlane` and `CoreApplicationPlane`.
2. You already have a Moesif account. You can sign up for a trial on [moesif.com](https://www.moesif.com/)

### 1. Install the NPM package

Within your SBT project directory, install `sbt-aws-moesif` via the following command:

```shell
npm install --save sbt-aws-moesif
```

### 2. Add MoesifBilling to your ControlPlane

Instantiate the [MoesifBilling](https://github.com/Moesif/sbt-aws-moesif/blob/master/lib/moesif-billing.ts) construct like below. You will need to set some properties to authenticate with Moesif.


```typescript
export class ControlPlaneStack extends Stack {
  public readonly regApiGatewayUrl: string;
  public readonly eventBusArn: string;

  constructor(scope: Construct, id: string, props: any) {
    super(scope, id, props);
    const cognitoAuth = new CognitoAuth(this, 'CognitoAuth', {
      idpName: 'COGNITO',
      systemAdminRoleName: 'SystemAdmin',
      systemAdminEmail: '<<Your Admin Email>>',
    });

    const moesifBilling = new MoesifBilling(stack, 'MoesifBilling', {
      moesifApplicationId: '<<Your Moesif Application Id>>',
      moesifManagementAPIKey: '<<Your Moesif Management API Key>>',
      billingProviderSlug: BillingProviderSlug.STRIPE,
      billingProviderSecretKey: '<<Your Billing Provider\'s Secret Such as for Stripe>>'
    }
   );

    const controlPlane = new ControlPlane(this, 'ControlPlane', {
      auth: cognitoAuth,
      billing: moesifBilling,
    });
    this.eventBusArn = controlPlane.eventBusArn;
    this.regApiGatewayUrl = controlPlane.controlPlaneAPIGatewayUrl;
  }
}
```

### Moesif Billing Properties

|Property Name|Type|Required|Description|Default|
|-------------|----|--------|-----------|-------|
|moesifApplicationId|string|Required|Collector Application Id from your Moesif account for event ingestion||
|moesifManagementAPIKey|string|Required|Management API Key from your Moesif account. The key must have the following scopes: create:companies create:subscriptions create:users delete:companies  delete:subscriptions delete:users||
|moesifManagementAPIBaseUrl|string||Override the base URL for the Moesif Mangaement API. For most setups, you don't need to set this.|https://api.moesif.com|
|moesifCollectorAPIBaseUrl|string||Override the base URL for the Moesif Collector API. For most setups, you don't need to set this.|https://api.moesif.net|
|billingProviderSlug|BillingProviderSlug|Required| Slug for Billing Provider / Payment Gateway||
|billingProviderSecretKey|string|Required|Secret Key for Billing Provider / Payment Gateway selected by billingProviderSlug||
|billingProviderClientId|string|Only if Zuora|Client Id for Billing Provider / Payment Gateway. Only used when billingProviderSlug is Zuora||
|billingProviderBaseUrl|string|Only if Chargebee or Zuora|Base URL for Billing Provider / Payment Gateway. Only used when billingProviderSlug is Zuora or Chargebee||
|tenantPlanField|string||Tenant object's field name that contains the plan id used when creating new subscriptions. Only used when billingProviderSlug is Zuora|planId|
|tenantPriceField|string||Tenant object's field name that contains the price id used when creating new subscriptions.|priceId|
|firehoseName|string||The name of the Kinesis Firehose delivery stream. By default, a unique name will be generated.||
|bucketName|string||The name of the S3 bucket for backup. By default, a unique name will be generated.||
|schema|string||Moesif Event Schema for data ingestion. By default, Moesif actions||

### 3. Provision a Tenant

Once you deploy your updated stack, create a tenant in your AWS SBT setup using the SBT APIs.

When you create a tenant, you must also set the price id to be used for creating subscriptions, By default, the field name is `priceId`, but this can be overridden via the above options. If you are using Zuora, you must also set the plan id. The field `email` must also be set.

_If your provider is set to Zuora, [you must also set these fields](#Zuora)_

If you're running the `hello-cdk` project, this can be done by running [this script](https://github.com/awslabs/sbt-aws/tree/main/docs/public#test-the-deployment) to onboard a new tenant. Modify, the script to also include the price (and plan if required).

> To find your plan id and price id, you can log into Moesif UI and go to Product Catalog or log into your billing provider.

```bash
DATA=$(jq --null-input \
    --arg tenantEmail "$TENANT_EMAIL" \
    --arg tenantId "$TENANT_ID" \
    '{
  "email": $tenantEmail,
  "tenantId": $tenantId,
  "priceId": "price_1MoBy5LkdIwHu7ixZhnattbh"
}')

echo "creating tenant..."
curl --request POST \
    --url "${CONTROL_PLANE_API_ENDPOINT}tenants" \
    --header "Authorization: Bearer ${ID_TOKEN}" \
    --header 'content-type: application/json' \
    --data "$DATA"
```

Once done, you should see the company show up in the Moesif UI. There should also be a subscription for the company in the "active" status.

The tenant will be subscribed to the price defined by `defaultPriceId`.
This can be expanded to allow more customization.

### 4. Ingest Events

Now that you created a tenant, you should ingest some actions in you're newly created firehose. Actions have an action name (like "Signed Up", "API Request", or "Finished Job") which represents the usage event. You can also include arbitrary metadata with an action, which enables you to create billable metrics, usage reporting, and more. For more info, [see docs on actions](https://www.moesif.com/docs/getting-started/user-actions/)

You'll want to set a few fields like below:

* `action_name` is a string and should include name of the event such as "Processed Payment Transaction"
* `company_id` is your tenant identifier. [See companies](https://www.moesif.com/docs/getting-started/companies/)
* `transaction_id` should be a random UUID for this event which Moesif uses for deduplication. [Docs on Moesif idempotency](https://www.moesif.com/docs/api#idempotency).
* `request.time` represents the transaction time as an ISO formatted string.
* `metadata` is an object which includes any custom properties for this event. By setting metadata, you can bill on arbitrary metrics, create metrics on them, etc. For example, if the action name is "Processed Payment Transaction", you can include an amount and the currency to bill on the total amount.

For full schema and available fields, see [Actions API Reference](https://www.moesif.com/docs/api#track-user-actions-in-batch)

An example action is below:

```json
{
  "action_name": "Processed Payment Transaction",
  "request": {
    "time": "2024-03-01T04:45:42.914"
  },
  "company_id": "12345", // This is your tenant id
  "transaction_id": "a3765025-46ec-45dd-bc83-b136c8d1d257",
  "metadata": {
    "amount": 24.6,
    "currency": "USD",
    "time_seconds": 66.3
  }
}
```
In the above example, the action is created whenever a payment is processed. There are also two metrics we are tracking as part of the action (the amount of the payment and how long the job took). You can create billable metrics and usage reports from these attributes.

> If your events are API calls, we recommend changing the MoesifEventSchema to `API_CALL` which provides a different schema than the above actions. See [API Calls](https://www.moesif.com/docs/api?int_source=docs#api-calls)


### 5. Create a Billing Meter

Now that the tenant is created, follow [these steps](https://www.moesif.com/docs/metered-billing/creating-billing-meters/) to create a billing meter in Moesif. The billing meter can filter or aggregate on any of the metadata fields you included with your action.

You should also select the provider and price defined by `billingProviderSlug` and `defaultPriceId`.
