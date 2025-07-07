{
  "Comment": "EBS Volume Conversion Workflow without DynamoDB",
  "StartAt": "InvokeEBSConversionLambda",
  "States": {
    "InvokeEBSConversionLambda": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:<your-region>:<your-account-id>:function:ConvertEBSVolume",
      "ResultPath": "$.LambdaResult",
      "Next": "CheckVolumes"
    },
    "CheckVolumes": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.LambdaResult.body",
          "StringMatches": "*No gp2 volumes*",
          "Next": "NoVolumesFound"
        }
      ],
      "Default": "SendNotification"
    },
    "NoVolumesFound": {
      "Type": "Pass",
      "Result": "No gp2 volumes found. Skipping SNS.",
      "End": true
    },
    "SendNotification": {
      "Type": "Task",
      "Resource": "arn:aws:states:::sns:publish",
      "Parameters": {
        "TopicArn": "arn:aws:sns:<your-region>:<your-account-id>:EBSVolumeConverted",
        "Message.$": "$.LambdaResult.body",
        "Subject": "EBS Volume Conversion Notification"
      },
      "ResultPath": "$.SNSResult",
      "End": true
    }
  }
}
