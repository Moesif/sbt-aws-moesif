// Copyright Moesif, Inc. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0

import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import { aws_logs, Duration } from 'aws-cdk-lib';
import { IDataIngestorAggregator } from '@cdklabs/sbt-aws/lib/control-plane/ingestor-aggregator/ingestor-aggregator-interface';
import { IBilling } from '@cdklabs/sbt-aws/lib/control-plane/billing/billing-interface';
import * as path from 'path';

export interface MoesifBillingProps {

    // Collector Application Id from your Moesif account for event ingestion
    readonly applicationId: string 

    // Management API Key from your Moesif account. The key must have the following scopes:
    // create:users create:companies delete:users delete:companies   
    readonly managementAPIKey: string   

    // URL for the Moesif Mangaement API
    readonly managementAPIBaseUrl?: string

    // Credentials for the Billing Provider / Payment Gateway
    readonly billingProviderSlug: string

    readonly billingProviderSecretKey: string

    // Default price to be used when creating new subscriptions
    // TODO this should be determined by plan/price selected by customer
    readonly defaultPriceId: string
  }

export class MoesifBilling extends Construct implements IBilling {
    readonly createUserFunction: lambda.IFunction;
    readonly deleteUserFunction: lambda.IFunction;
    readonly ingestor: IDataIngestorAggregator;
    readonly putUsageFunction: lambda.IFunction;
    readonly webhookFunction?: lambda.IFunction;
    readonly webhookPath?: string;
    readonly managementAPIBaseUrl: string;
    readonly logGroupName: string

    constructor(scope: Construct, id: string, props: MoesifBillingProps) {
        super(scope, id);

        this.managementAPIBaseUrl = props.managementAPIBaseUrl || 'https://api.moesif.com'
        this.logGroupName = 'MoesifBilling'

        /**
         * The function to trigger when creating a new billing user.
         */
        const billingUserService: lambda.IFunction = new lambda.Function(this, 'MoesifManagement', {
            runtime: lambda.Runtime.PYTHON_3_12,
            handler: 'billing_management.handler',
            tracing: lambda.Tracing.ACTIVE,
            timeout: Duration.seconds(60),
            logGroup: new aws_logs.LogGroup(this, this.logGroupName, {
                retention: aws_logs.RetentionDays.FIVE_DAYS,
            }),
            code: lambda.Code.fromAsset(path.resolve(__dirname, '../resources/functions/billing_management')), // Path to the directory containing your Lambda function code
            environment: {
                MOESIF_MANAGEMENT_API_KEY: props.managementAPIKey,
                MOESIF_MANAGEMENT_BASE_URL: this.managementAPIBaseUrl,
                BILLING_PROVIDER_SLUG: props.billingProviderSlug,
                BILLING_PROVIDER_SECRET_KEY: props.billingProviderSecretKey,
                DEFAULT_PRICE_ID: props.defaultPriceId
            },
        });

        this.createUserFunction = billingUserService;
        this.deleteUserFunction = billingUserService;
        this.ingestor = null as any; // TODO. We don't need an ingestor/aggregator
        this.putUsageFunction = billingUserService;  // TODO. Prefer handling via firehose
        this.webhookFunction = null as any; // TODO What is this for?
        this.webhookPath = null as any; // TODO What is this for?
    }
}