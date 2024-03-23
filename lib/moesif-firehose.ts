import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import * as s3 from "aws-cdk-lib/aws-s3";
import * as iam from "aws-cdk-lib/aws-iam";
import * as kinesisfirehose from "aws-cdk-lib/aws-kinesisfirehose";

/**
 * Properties for the MoesifFirehoseConstruct.
 */
export interface MoesifFirehoseConstructProps {
  /**
   * The Application Id from your Moesif account. This is a required property with a minimum length of 50 characters.
   */
  readonly moesifApplicationId: string;

  /**
   * The name of the Kinesis Firehose delivery stream.
   * @default - A unique name will be generated.
   */
  readonly firehoseName?: string;

  /**
   * The name of the S3 bucket for backup.
   * @default - A unique name will be generated.
   */
  readonly bucketName?: string;
}

/**
 * A construct that creates a Kinesis Firehose delivery stream for sending logs to Moesif.
 */
export class MoesifFirehoseConstruct extends Construct {
  /**
   * The Kinesis Firehose delivery stream that will deliver events to Moesif.
   */
  public readonly firehoseStream: kinesisfirehose.CfnDeliveryStream;

  /**
   * Creates a new instance of the MoesifFirehoseConstruct.
   *
   * @param {Construct} scope - The scope in which to define this construct.
   * @param {string} id - The unique ID of this construct.
   * @param {MoesifFirehoseConstructProps} props - The properties for the construct.
   */
  constructor(scope: Construct, id: string, props: MoesifFirehoseConstructProps) {
    super(scope, id);

    const moesifURL = "https://api.moesif.net/v1/partners/aws/kinesis/actions";
    const bucket = new s3.Bucket(this, "MoesifBackupBucket", {
      bucketName: props.bucketName,
      encryption: s3.BucketEncryption.S3_MANAGED,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      enforceSSL: true,
    });

    const deliveryRole = new iam.Role(this, "DeliveryRole", {
      assumedBy: new iam.ServicePrincipal("firehose.amazonaws.com"),
      externalIds: [cdk.Stack.of(this).account],
    });

    this.firehoseStream = new kinesisfirehose.CfnDeliveryStream(this, "KinesisFirehose", {
      deliveryStreamName: props.firehoseName,
      deliveryStreamType: "DirectPut",
      httpEndpointDestinationConfiguration: {
        bufferingHints: {
          intervalInSeconds: 60,
          sizeInMBs: 1,
        },
        endpointConfiguration: {
          accessKey: props.moesifApplicationId,
          name: "Moesif-collector",
          url: moesifURL,
        },
        requestConfiguration: {
          contentEncoding: "GZIP",
        },
        s3Configuration: {
          bucketArn: bucket.bucketArn,
          roleArn: deliveryRole.roleArn,
        },
      },
    });
  }
}
