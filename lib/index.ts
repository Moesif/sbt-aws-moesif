// import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
// import * as sqs from 'aws-cdk-lib/aws-sqs';

export interface SbtAwsMoesifProps {
  // Define construct properties here
}

export class SbtAwsMoesif extends Construct {

  constructor(scope: Construct, id: string, props: SbtAwsMoesifProps = {}) {
    super(scope, id);

    // Define construct contents here

    // example resource
    // const queue = new sqs.Queue(this, 'SbtAwsMoesifQueue', {
    //   visibilityTimeout: cdk.Duration.seconds(300)
    // });
  }
}
