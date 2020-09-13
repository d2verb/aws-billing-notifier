# aws-billing-notifier
Sending billing info to your slack channel everyday.

## How to use
0. install AWS SAM CLI (see: [here](https://docs.aws.amazon.com/ja_jp/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html))

1. fill in all the contents in .envrc (you need [direnv](https://github.com/direnv/direnv))
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

## Invoke function locally
You can invoke lambda function in your local environment.
```
$ make invoke
```

## References
- https://qiita.com/sotoiwa/items/fa3070f5c84f4538e774
- https://dev.classmethod.jp/articles/notify-slack-aws-billing/
- https://amezou.com/categories/slack%e3%82%b3%e3%82%b9%e3%83%88%e9%80%9a%e7%9f%a5/