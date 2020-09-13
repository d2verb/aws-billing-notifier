# aws-billing-notifier
Sending billing info to your slack channel everyday.

## How to use
1. fill in all the contents in .envrc
```
export AWS_PROFILE=
export AWS_REGION=
export AWS_S3_BUCKET=
export SLACK_WEBHOOK_URL=
```

2. deploy it
```
$ make deploy
```