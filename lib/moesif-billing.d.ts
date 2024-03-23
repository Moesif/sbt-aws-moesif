import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import { IDataIngestorAggregator } from '@cdklabs/sbt-aws/lib/control-plane/ingestor-aggregator/ingestor-aggregator-interface';
import { IBilling } from '@cdklabs/sbt-aws/lib/control-plane/billing/billing-interface';
export interface MoesifBillingProps {
    readonly applicationId: string;
    readonly managementAPIKey: string;
    readonly managementAPIBaseUrl?: string;
    readonly billingProviderSlug: string;
    readonly billingProviderSecretKey: string;
    readonly defaultPriceId: string;
}
export declare class MoesifBilling extends Construct implements IBilling {
    readonly createUserFunction: lambda.IFunction;
    readonly deleteUserFunction: lambda.IFunction;
    readonly ingestor: IDataIngestorAggregator;
    readonly putUsageFunction: lambda.IFunction;
    readonly webhookFunction?: lambda.IFunction;
    readonly webhookPath?: string;
    readonly managementAPIBaseUrl: string;
    readonly logGroupName: string;
    constructor(scope: Construct, id: string, props: MoesifBillingProps);
}
