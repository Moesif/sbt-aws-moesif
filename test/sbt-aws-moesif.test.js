"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const cdk = require("aws-cdk-lib");
const assertions_1 = require("aws-cdk-lib/assertions");
const lib_1 = require("../lib");
test('Moesif Billing Management Lambdas Created', () => {
    const app = new cdk.App();
    const stack = new cdk.Stack(app, "moesif-test-stack");
    new lib_1.MoesifBilling(stack, 'MoesifBilling', {
        moesifApplicationId: '<<Your Moesif Application Id>>',
        moesifManagementAPIKey: '<<Your Moesif Management API Key>>',
        billingProviderSlug: lib_1.BillingProviderSlug.STRIPE,
        billingProviderSecretKey: '<<Your Billing Provider\'s Secret Such as for Stripe>>'
    });
    const template = assertions_1.Template.fromStack(stack);
});
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoic2J0LWF3cy1tb2VzaWYudGVzdC5qcyIsInNvdXJjZVJvb3QiOiIiLCJzb3VyY2VzIjpbInNidC1hd3MtbW9lc2lmLnRlc3QudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7QUFBQSxtQ0FBbUM7QUFDbkMsdURBQWtEO0FBQ2xELGdDQUE0RDtBQUU1RCxJQUFJLENBQUMsMkNBQTJDLEVBQUUsR0FBRyxFQUFFO0lBQ3BELE1BQU0sR0FBRyxHQUFHLElBQUksR0FBRyxDQUFDLEdBQUcsRUFBRSxDQUFDO0lBQzFCLE1BQU0sS0FBSyxHQUFHLElBQUksR0FBRyxDQUFDLEtBQUssQ0FBQyxHQUFHLEVBQUUsbUJBQW1CLENBQUMsQ0FBQztJQUN0RCxJQUFJLG1CQUFhLENBQUMsS0FBSyxFQUFFLGVBQWUsRUFBRTtRQUN2QyxtQkFBbUIsRUFBRSxnQ0FBZ0M7UUFDckQsc0JBQXNCLEVBQUUsb0NBQW9DO1FBQzVELG1CQUFtQixFQUFFLHlCQUFtQixDQUFDLE1BQU07UUFDL0Msd0JBQXdCLEVBQUUsd0RBQXdEO0tBQ25GLENBQ0QsQ0FBQztJQUNGLE1BQU0sUUFBUSxHQUFHLHFCQUFRLENBQUMsU0FBUyxDQUFDLEtBQUssQ0FBQyxDQUFDO0FBQzlDLENBQUMsQ0FBQyxDQUFDIiwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0ICogYXMgY2RrIGZyb20gJ2F3cy1jZGstbGliJztcbmltcG9ydCB7IFRlbXBsYXRlIH0gZnJvbSAnYXdzLWNkay1saWIvYXNzZXJ0aW9ucyc7XG5pbXBvcnQgeyBNb2VzaWZCaWxsaW5nLCBCaWxsaW5nUHJvdmlkZXJTbHVnIH0gZnJvbSAnLi4vbGliJztcblxudGVzdCgnTW9lc2lmIEJpbGxpbmcgTWFuYWdlbWVudCBMYW1iZGFzIENyZWF0ZWQnLCAoKSA9PiB7XG4gICBjb25zdCBhcHAgPSBuZXcgY2RrLkFwcCgpO1xuICAgY29uc3Qgc3RhY2sgPSBuZXcgY2RrLlN0YWNrKGFwcCwgXCJtb2VzaWYtdGVzdC1zdGFja1wiKTtcbiAgIG5ldyBNb2VzaWZCaWxsaW5nKHN0YWNrLCAnTW9lc2lmQmlsbGluZycsIHtcbiAgICAgIG1vZXNpZkFwcGxpY2F0aW9uSWQ6ICc8PFlvdXIgTW9lc2lmIEFwcGxpY2F0aW9uIElkPj4nLFxuICAgICAgbW9lc2lmTWFuYWdlbWVudEFQSUtleTogJzw8WW91ciBNb2VzaWYgTWFuYWdlbWVudCBBUEkgS2V5Pj4nLFxuICAgICAgYmlsbGluZ1Byb3ZpZGVyU2x1ZzogQmlsbGluZ1Byb3ZpZGVyU2x1Zy5TVFJJUEUsXG4gICAgICBiaWxsaW5nUHJvdmlkZXJTZWNyZXRLZXk6ICc8PFlvdXIgQmlsbGluZyBQcm92aWRlclxcJ3MgU2VjcmV0IFN1Y2ggYXMgZm9yIFN0cmlwZT4+J1xuICAgIH1cbiAgICk7XG4gICBjb25zdCB0ZW1wbGF0ZSA9IFRlbXBsYXRlLmZyb21TdGFjayhzdGFjayk7XG59KTtcbiJdfQ==