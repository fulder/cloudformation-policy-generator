[![Build Status](https://travis-ci.com/fulder/cloudformation-policy-generator.svg?branch=master)](https://travis-ci.com/fulder/cloudformation-policy-generator)
[![Coverage Status](https://coveralls.io/repos/github/fulder/cloudformation-policy-generator/badge.svg?branch=master)](https://coveralls.io/github/fulder/cloudformation-policy-generator?branch=master)
[![Python Version](https://img.shields.io/badge/python-2.6%2C2.7%2C3.3%2B-blue.svg)](https://www.python.org/)

# Description

This generator reads a CloudFormation template and generates a new CloudFormation only with an IAM role with all policies needed to deploy the initial CloudFormation.

To deploy the IAM Role CloudFormation the following policy actions are needed:
* `cloudFormation:CreateStack`
* `cloudFormation:UpdateStack`
* `iam:CreateRole` 
* `iam::DeleteRole`

## Why/When to use this generator
If you want to have an IAM role with more strict permissions only allowing to deploy a specific CloudFormation instead of always running with full Administrator permissions.

It can somehow be hard to know exacly what permissions are needed for a resource. As an example creating a VPC lambda, the role need to be allowed `lambda:CreateFunction`, `lambda:DeleteFunction` but also e.g. `ec2:ReleaseAddress` to release the elastic IP address given to the lambda in the background and when the CloudFormation need to rollback.

# Implemented resources

This project is still in beta and all help/PRs are welcome.
See: [IMPLEMENTATED_RESOURCES.md](https://github.com/fulder/cloudformation-policy-generator/blob/master/IMPLEMENTED_RESOURCES.md) for a list of currently implemented resources.

# Python versions
2.6, 2.7, 3.3+

# Installation

* `pip install -r requirements.txt`

# Usage

### Generate policy
* `python generate.py -f cloud_formation.yml -r us-east-1 -a <AWS_ACCOUNT_NUMBER>`

### Save policy to file
* `python generate.py -f cloud_formation.yml -r us-east-1 -a <AWS_ACCOUNT_NUMBER> -o iam_cloudformation.yml`