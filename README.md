Description
This AWS stack creates resources for securely hosting SOPS. It is built for personal use by an IAM user (stack parameter).

Components
AWS KMS Key: A key is created for use within the SOPS application. This key is also used to encrypt the storage of the CodeCommit repo.
AWS CodeCommit Repository: A private repo for hosting a SOPS nix flake.

Outputs
KmsKeyARN: The ARN of the KMS key.
RepoURL: The URL of the CodeCommit repository.

Parameters
IAMUserParam: The name of the secure AWS CodeCommit repository that will be created.

Deployment example
`aws cloudformation deploy --template-file cloudformation/sops.yaml --stack-name sops-ryan --parameter-overrides "IAMUserParam=ryan"`
