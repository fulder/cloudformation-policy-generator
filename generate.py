from __future__ import annotations
import argparse
import json
import logging

import yaml

logger = logging.getLogger()


class PolicyGenerator:

    def __init__(self, cloud_formation: dict):
        self.cloud_formation = cloud_formation
        self.policy = {"Version": "2012-10-17", "Statements": []}

    def generate(self) -> dict:
        for resource_name in self.cloud_formation["Resources"]:
            logger.debug("Generating policy for resource: [%s]", resource_name)

            res = self.cloud_formation["Resources"][resource_name]
            logger.debug("Resource type: [%s]", res["Type"])

            if res["Type"] == "AWS::S3::Bucket":
                self._s3_bucket(resource_name, res)

        return self.policy

    def _s3_bucket(self, name: str, res: dict):
        resource = "*"
        if "BucketName" in res:
            resource = "arn:aws:s3:::{}".format(res["BucketName"])

        actions = ["s3:CreateBucket", "s3:DeleteBucket"]
        self._add_policy_statement(name, res, actions, resource)

    def _add_policy_statement(self, res_name: str, res: dict, actions: list, resource: str):
        res_type = res["Type"].split("AWS::")[1].replace("::", "-")
        self.policy["Statements"].append({
            "Sid": "Policy-Generator-{}-{}".format(res_type, res_name),
            "Statement": {
                "Effect": "Allow",
                "Action": actions,
                "Resource": resource
            }
        })


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CloudFormation Generator")
    parser.add_argument("-f", "--file", help="Path to the CloudFormation JSON/YAML template", required=True)
    parser.add_argument("-o", "--out", help="Save output to the specified file")
    args = parser.parse_args()

    cloud_formation_dict = yaml.safe_load(open(args.file, "r"))
    generated_policy = PolicyGenerator(cloud_formation_dict).generate()

    if args.out is not None:
        with open(args.out, "w") as outfile:
            json.dump(generated_policy, outfile, indent=4)
    else:
        print(generated_policy)
