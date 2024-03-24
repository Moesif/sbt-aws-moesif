// Copyright Moesif, Inc. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0

import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import { aws_logs, Duration } from 'aws-cdk-lib';
import { IDataIngestorAggregator } from '@cdklabs/sbt-aws/lib/control-plane/ingestor-aggregator/ingestor-aggregator-interface';
import { IBilling } from '@cdklabs/sbt-aws/lib/control-plane/billing/billing-interface';
import * as path from 'path';
import { MoesifFirehoseConstruct, MoesifEventSchema } from './moesif-firehose'

export enum BillingProviderSlug {
    STRIPE = 'stripe', // https://www.moesif.com/docs/metered-billing/integrate-with-stripe/
    CHARGEBEE = 'chargebee', // https://www.moesif.com/docs/metered-billing/integrate-with-chargebee/
    ZUORA = 'zuora', // https://www.moesif.com/docs/metered-billing/integrate-with-zuora/
    CUSTOM = 'custom' // https://www.moesif.com/docs/metered-billing/integrate-with-a-custom-webhook/
}

export interface MoesifBillingProps {

    /**
     * Collector Application Id from your Moesif account for event ingestion
     */
    readonly moesifApplicationId: string 

    /**
     * Management API Key from your Moesif account. The key must have the following scopes:
     * create:companies create:subscriptions create:users delete:companies  delete:subscriptions delete:users 
     */ 
    readonly moesifManagementAPIKey: string   

    /**
     * Override the base URL for the Moesif Mangaement API. For most setups, you don't need to set this.
     * @default https://api.moesif.com
     */ 
    readonly moesifManagementAPIBaseUrl?: string

    /**
     * Override the base URL for the Moesif Collector API. For most setups, you don't need to set this.
     * @default https://api.moesif.net
     */ 
    readonly moesifCollectorAPIBaseUrl?: string

    /**
     * Slug for Billing Provider / Payment Gateway
     */ 
    readonly billingProviderSlug: BillingProviderSlug

    /**
     * Secret Key for Billing Provider / Payment Gateway selected by billingProviderSlug
     */ 
    readonly billingProviderSecretKey: string

    /**
     * Client Id for Billing Provider / Payment Gateway. Only used when billingProviderSlug is ZUORA
     */ 
    readonly billingProviderClientId?: string

    /**
     * Base URL for Billing Provider / Payment Gateway. Only used when billingProviderSlug is ZUORA or CHARGEBEE
     */ 
    readonly billingProviderBaseUrl?: string

    /**
     * Default plan id to be used when creating new subscriptions 
     * Only used when billingProviderSlug is ZUORA
     */ 
    readonly defaultPlanId?: string

    /**
     * Default price id to be used when creating new subscriptions 
     */ 
    readonly defaultPriceId: string

    /**
     * The name of the Kinesis Firehose delivery stream.
     * @default - A unique name will be generated.
     */
    readonly firehoseName?: string

    /**
     * The name of the S3 bucket for backup.
     * @default - A unique name will be generated.
     */
    readonly bucketName?: string;

    /**
     * Moesif Event Schema for data ingestion
     * @default - Moesif Action
     */
    readonly schema?: MoesifEventSchema;
}

export class MoesifBilling extends Construct implements IBilling {
    readonly createUserFunction: lambda.IFunction;
    readonly deleteUserFunction: lambda.IFunction;
    readonly ingestor: IDataIngestorAggregator;
    readonly putUsageFunction: lambda.IFunction;
    readonly webhookFunction?: lambda.IFunction;
    readonly webhookPath?: string;
    readonly managementBaseUrl: string;
    readonly firehose: MoesifFirehoseConstruct;
    readonly logGroupName: string

    constructor(scope: Construct, id: string, props: MoesifBillingProps) {
        super(scope, id);

        this.managementBaseUrl = props.moesifManagementAPIBaseUrl || 'https://api.moesif.com'
        this.logGroupName = 'MoesifBilling'

        /**
         * The function to trigger when creating a new billing user.
         */
        const billingUserService: lambda.IFunction = new lambda.Function(this, '-Management', {
            runtime: lambda.Runtime.PYTHON_3_12,
            handler: 'billing_management.handler',
            tracing: lambda.Tracing.ACTIVE,
            timeout: Duration.seconds(60),
            logGroup: new aws_logs.LogGroup(this, this.logGroupName, {
                retention: aws_logs.RetentionDays.FIVE_DAYS,
            }),
            code: lambda.Code.fromAsset(path.resolve(__dirname, '../resources/functions/billing_management')), // Path to the directory containing your Lambda function code
            environment: {
                MOESIF_MANAGEMENT_API_KEY: props.moesifManagementAPIKey,
                MOESIF_MANAGEMENT_BASE_URL: this.managementBaseUrl,
                BILLING_PROVIDER_SLUG: props.billingProviderSlug,
                BILLING_PROVIDER_SECRET_KEY: props.billingProviderSecretKey,
                BILLING_PROVIDER_CLIENT_ID: props.billingProviderClientId || '',
                BILLING_PROVIDER_BASE_URL: props.billingProviderBaseUrl || '',
                DEFAULT_PLAN_ID: props.defaultPlanId || '',
                DEFAULT_PRICE_ID: props.defaultPriceId,
            },
        });

        // TODO should this be part of IBilling or not included here?
        this.firehose = new MoesifFirehoseConstruct(this, '-CollectorFirehose', {
            moesifApplicationId: props.moesifApplicationId,
            moesifCollectorAPIBaseUrl: props.moesifCollectorAPIBaseUrl,
            firehoseName: props.firehoseName,
            bucketName: props.bucketName,
            schema: props.schema
        })

        this.createUserFunction = billingUserService;
        this.deleteUserFunction = billingUserService;
        this.ingestor = null as any;
        this.putUsageFunction = billingUserService // FIXME
        this.webhookFunction = null as any;
        this.webhookPath = null as any;
    }
}