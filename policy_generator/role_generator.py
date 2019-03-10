import json
import logging

from policy_generator.resources.cloudformation.cloud_formation import CloudFormation
from policy_generator.resources.ec2.instance import EC2Instance
from policy_generator.resources.s3.bucket import S3Bucket
from policy_generator.resources.aws_lambda.function import LambdaFunction

logger = logging.getLogger(__name__)


class RoleGenerator(object):

    def __init__(self, cloud_formation, region, account):
        self.cloud_formation = cloud_formation
        self.region = region
        self.account = account
        self.role_cloud_formation = {
            "AWSTemplateFormatVersion": "2010-09-09",
            "Description": "Policy Generator Role",
            "Resources": {
                "PolicyGeneratorRole": {
                    "Type": "AWS::IAM::Role",
                    "Properties": {
                        "Policies": []
                    },
                    "RoleName": "PolicyGeneratorRole"
                }
            }
        }
        self.policies = []

    def generate(self):
        self.policies.append(CloudFormation().create_policy())

        for resource_name in self.cloud_formation["Resources"]:
            logger.debug("Generating policy for resource: [%s]", resource_name)

            res = self.cloud_formation["Resources"][resource_name]
            logger.debug("Resource type: [%s]", res["Type"])

            if res["Type"] == "AWS::EC2::Instance":
                self.policies.append(EC2Instance(resource_name, res, self.region, self.account).create_policy())
            if res["Type"] == "AWS::Lambda::Function":
                self.policies.append(LambdaFunction(resource_name, res, self.region, self.account).create_policy())
            if res["Type"] == "AWS::S3::Bucket":
                self.policies.append(S3Bucket(resource_name, res).create_policy())

        self.role_cloud_formation["Resources"]["PolicyGeneratorRole"]["Properties"]["Policies"] = self.policies

        self._check_ref_params()

        return self.role_cloud_formation

    def _check_ref_params(self):
        role_cloudformation_str = json.dumps(self.role_cloud_formation)
        if "Parameters" in self.cloud_formation:
            for param_name in self.cloud_formation["Parameters"]:
                if param_name in role_cloudformation_str:
                    logger.debug("Copy parameter: [%s] from input cloudformation", param_name)
                    if "Parameters" not in self.role_cloud_formation:
                        self.role_cloud_formation["Parameters"] = {}
                    self.role_cloud_formation["Parameters"][param_name] = self.cloud_formation["Parameters"][param_name]
