[![Coverage Status](https://coveralls.io/repos/github/fulder/cloudformation-policy-generator/badge.svg?branch=master)](https://coveralls.io/github/fulder/cloudformation-policy-generator?branch=master)

# Python versions
2.6, 2.7, 3.3+

# Installation

* `pip install -r requirements.txt`

# Usage

### Generate policy
* `python generate.py -f cloud_formation.yml`

### Save policy to file
* `python generate.py -f cloud_formation.yml -o policy.json`