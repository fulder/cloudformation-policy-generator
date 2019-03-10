[![Build Status](https://travis-ci.com/fulder/cloudformation-policy-generator.svg?branch=master)](https://travis-ci.com/fulder/cloudformation-policy-generator)
[![Coverage Status](https://coveralls.io/repos/github/fulder/cloudformation-policy-generator/badge.svg?branch=master)](https://coveralls.io/github/fulder/cloudformation-policy-generator?branch=master)
[![Python Version](https://img.shields.io/badge/python-2.6%2C2.7%2C3.3%2B-blue.svg)](https://www.python.org/)

# Description

This generator reads a CloudFormation template and generates the needed IAM policy needed to deploy all the specified resources.

While creating e.g. a VPC lambda the role need to be able to not only `lambda:CreateFunction` is required but also `lambda:DeleteFunction` if CloudFormation needs to be rolled back or `ec2:ReleaseAddress` to release the elastic IP address given to the lambda in the background.

# Implemented resources

See: [IMPLEMENTATED_RESOURCES.md](https://github.com/fulder/cloudformation-policy-generator/blob/master/IMPLEMENTED_RESOURCES.md) for a list of currently implemented resources.

# Python versions
2.6, 2.7, 3.3+

# Installation

* `pip install -r requirements.txt`

# Usage

### Generate policy
* `python generate.py -f cloud_formation.yml`

### Save policy to file
* `python generate.py -f cloud_formation.yml -o policy.json`