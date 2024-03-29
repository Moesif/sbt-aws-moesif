import * as cdk from 'aws-cdk-lib';
import { Template } from 'aws-cdk-lib/assertions';
import { MoesifBilling, BillingProviderSlug } from '../lib';

test('Moesif Billing Management Lambdas Created', () => {
   const app = new cdk.App();
   const stack = new cdk.Stack(app, "moesif-test-stack");
   new MoesifBilling(stack, 'MoesifBilling', {
      moesifApplicationId: '<<Your Moesif Application Id>>',
      moesifManagementAPIKey: '<<Your Moesif Management API Key>>',
      billingProviderSlug: BillingProviderSlug.STRIPE,
      billingProviderSecretKey: '<<Your Billing Provider\'s Secret Such as for Stripe>>'
    }
   );
   const template = Template.fromStack(stack);
});
