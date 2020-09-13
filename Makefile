STACK_NAME := BillingNotifier 

build:
	sam build

package: build
	sam package \
		--output-template-file packaged.yaml \
		--s3-bucket ${AWS_S3_BUCKET}

deploy: package
	sam deploy \
		--template-file packaged.yaml \
		--stack-name $(STACK_NAME) \
		--capabilities CAPABILITY_IAM \
		--parameter-overrides SlackWebhookUrl=${SLACK_WEBHOOK_URL} \
		--region ${AWS_REGION}

destroy:
	aws cloudformation delete-stack \
		--profile ${AWS_PROFILE} \
		--region ${AWS_REGION} \
		--stack-name $(STACK_NAME)

clean:
	rm -f ./packaged.yaml
	rm -rf ./.aws-sam

.PHONY: build package deploy destroy clean