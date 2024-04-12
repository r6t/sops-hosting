from troposphere import Template, Parameter, Output, Ref, GetAtt, Join, Sub
from troposphere.kms import Key
from troposphere.codecommit import Repository

template = Template()

template.set_description("SOPS hosting stack: KMS, CodeCommit")

iam_user_parameter = template.add_parameter(Parameter(
    "IAMUserParam",
    Type="String",
    Description="Name of the local IAM user that owns these SOPS resources"
))

sops_key = template.add_resource(Key(
    "SOPSKey",
    Description="KMS Key used for: repository storage, encryption of secrets within SOPS",  
    KeyPolicy={
        "Version": "2012-10-17",
        "Id": "key-default-1",
        "Statement": [
            {
                "Sid": "SOPS Key ownership",
                "Effect": "Allow",
                "Principal": {"AWS": {"Fn::Join": [":", ["arn:aws:iam:", {"Ref": "AWS::AccountId"}, "root"]]}},
                "Action": "kms:*",
                "Resource": "*"
            },
            {
                "Sid": "SOPS Key use",
                "Effect": "Allow",
                "Principal": {"AWS": Join("", ["arn:aws:iam::", {"Ref": "AWS::AccountId"}, ":user/", Ref(iam_user_parameter)])},
                "Action": [
                    "kms:Encrypt",
                    "kms:Decrypt",
                    "kms:ReEncrypt*",
                    "kms:GenerateDataKey*",
                    "kms:DescribeKey"
                ],
                "Resource": "*"
            }
        ]
    }
))

sops_repo = template.add_resource(Repository(
    "SOPSRepo",
    RepositoryName=Join("-", [Ref(iam_user_parameter), "sops"]),
    RepositoryDescription=Join("", ["SOPS repo for user/", Ref(iam_user_parameter)]),
    KmsKeyId=Ref(sops_key)
))

template.add_output([
    Output(
        "RepoURL",
        Description="SOPS CodeCommit repo URL",
        Value=GetAtt(sops_repo, "CloneUrlHttp")
    ),
    Output(
        "KmsKeyARN",
        Description="SOPS KMS Key ARN",
        Value=GetAtt(sops_key, "Arn")
    )
])

with open('cloudformation/sops.yaml', 'w') as file:
    file.write(template.to_yaml())
