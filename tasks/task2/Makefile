SHELL = /usr/bin/env bash -xeuo pipefail

stack_name:=create-metadata

init:
	@pipenv install --dev

clean:
	@rm -rf src/requirements.txt
	@rm -rf .aws-sam

build: clean
	@pipenv lock --requirements > src/requirements.txt
	@pipenv run sam build --use-container --template sam/template.yaml --base-dir src

package: build
	@pipenv run sam package --s3-bucket $$SAM_ARTIFACT_BUCKET --output-template-file template.yaml

deploy: package
	@pipenv run sam deploy \
		--template-file template.yaml \
		--stack-name $(stack_name) \
		--capabilities CAPABILITY_IAM \
		--no-fail-on-empty-changeset
	@pipenv run aws cloudformation describe-stacks \
		--stack-name $(stack_name) \
		--query Stacks[0].Outputs

destroy:
	@aws s3 rb --force s3://$$(pipenv run aws cloudformation describe-stacks \
    		--stack-name $(stack_name) \
    		--query 'Stacks[].Outputs[?OutputKey==`DataBucketName`].[OutputValue]' --output text) || true
	@pipenv run aws cloudformation delete-stack --stack-name $(stack_name)
	@pipenv run aws cloudformation wait stack-delete-complete --stack-name $(stack_name)

info:
	@echo -n "StackName: "
	@echo $(stack_name)

.PHONY: \
	build \
	package \
	deploy \
	info \
	clean \
	destroy
