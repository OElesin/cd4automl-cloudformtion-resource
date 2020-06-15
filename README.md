# CD4AutoML::Workflow::Deploy

[DEVELOPER PREVIEW]
---

This is the Amazon Cloudformation resource for CD4AutoML.

What is CD4AutoML?

Cd4AutoML is a managed end-to-end workflow that automates the entire machine learning workflow from automated
machine learning to real time inference over a REST API on managed infrastructure.

## Usage

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "Type" : "CD4AutoML::Workflow::Deploy",
    "Properties" : {
        "<a href="#s3trainingdatapath" title="S3TrainingDataPath">S3TrainingDataPath</a>" : <i>String</i>,
        "<a href="#targetcolumnname" title="TargetColumnName">TargetColumnName</a>" : <i>String</i>,
        "<a href="#notificationemail" title="NotificationEmail">NotificationEmail</a>" : <i>String</i>,
        "<a href="#workflowname" title="WorkflowName">WorkflowName</a>" : <i>String</i>,
        "<a href="#schedule" title="Schedule">Schedule</a>" : <i>String</i>,
    }
}
</pre>

### YAML

<pre>
Type: CD4AutoML::Workflow::Deploy
Properties:
    <a href="#s3trainingdatapath" title="S3TrainingDataPath">S3TrainingDataPath</a>: <i>String</i>
    <a href="#targetcolumnname" title="TargetColumnName">TargetColumnName</a>: <i>String</i>
    <a href="#notificationemail" title="NotificationEmail">NotificationEmail</a>: <i>String</i>
    <a href="#workflowname" title="WorkflowName">WorkflowName</a>: <i>String</i>
    <a href="#schedule" title="Schedule">Schedule</a>: <i>String</i>
</pre>

## Properties

#### S3TrainingDataPath

S3 Path containing training data. Data format must CSV with headers.

_Required_: Yes

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### TargetColumnName

The name of the target column to be predicted. This MUST be last column in the CSV data in S3

_Required_: Yes

_Type_: String

_Minimum_: <code>5</code>

_Maximum_: <code>10</code>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### NotificationEmail

Valid email address to receive email notifications.

_Required_: Yes

_Type_: String

_Pattern_: <code>^[\x20-\x45]?[\w-\+]+(\.[\w]+)*@[\w-]+(\.[\w]+)*(\.[a-z]{2,})$</code>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### WorkflowName

Unique Name or Identifier for CD4AutoML workflow

_Required_: Yes

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Schedule

Number of days before retraining AutoML model.

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

## Return Values

### Ref

When you pass the logical ID of this resource to the intrinsic `Ref` function, Ref returns the WorkflowName.

### Fn::GetAtt

The `Fn::GetAtt` intrinsic function returns a value for a specified attribute of this type. The following are the available attributes and sample return values.

For more information about using the `Fn::GetAtt` intrinsic function, see [Fn::GetAtt](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html).

#### InferenceApi

REST API URI for real time model inference available once workflow is completed

