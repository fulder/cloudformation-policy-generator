import logging

logger = logging.getLogger()


class PolicyGenerator:

    def __init__(self, cloud_formation):
        self.cloud_formation = cloud_formation
        self.policy = {"Version": "2012-10-17", "Statements": []}

    def generate(self):
        for resource_name in self.cloud_formation["Resources"]:
            logger.debug("Generating policy for resource: [%s]", resource_name)

            res = self.cloud_formation["Resources"][resource_name]
            logger.debug("Resource type: [%s]", res["Type"])

            if res["Type"] == "AWS::S3::Bucket":
                self._s3_bucket(resource_name, res)

        return self.policy

    def _s3_bucket(self, name, res):
        resource = "*"
        if "BucketName" in res:
            resource = "arn:aws:s3:::{}".format(res["BucketName"])

        actions = ["s3:CreateBucket", "s3:DeleteBucket"]
        self._add_policy_statement(name, res, actions, resource)

    def _add_policy_statement(self, res_name, res, actions, resource):
        res_type = res["Type"].split("AWS::")[1].replace("::", "-")
        self.policy["Statements"].append({
            "Sid": "Policy-Generator-{}-{}".format(res_type, res_name),
            "Statement": {
                "Effect": "Allow",
                "Action": actions,
                "Resource": resource
            }
        })
