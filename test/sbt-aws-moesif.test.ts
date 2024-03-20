import * as cdk from 'aws-cdk-lib';
import { Template } from 'aws-cdk-lib/assertions';
import * as MoesifBilling from '../lib/index';

test('Moesif User Management Lambdas Created', () => {
   const app = new cdk.App();
   const stack = new cdk.Stack(app, "moesif-test-stack");
   new MoesifBilling.MoesifBilling(stack, 'MoesifBilling', {
        applicationId: '',
        managementAPIKey: '',
    }
   );
   const template = Template.fromStack(stack);
});
