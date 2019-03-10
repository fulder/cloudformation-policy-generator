import logging

logger = logging.getLogger()


class PolicyGenerator:

    def __init__(self, cloud_formation, region, account):
        self.cloud_formation = cloud_formation
        self.region = region
        self.account = account
        self.policy = {"Version": "2012-10-17", "Statements": []}

    def generate(self):
        for resource_name in self.cloud_formation["Resources"]:
            logger.debug("Generating policy for resource: [%s]", resource_name)

            res = self.cloud_formation["Resources"][resource_name]
            logger.debug("Resource type: [%s]", res["Type"])

            if res["Type"] == "AWS::S3::Bucket":
                self._s3_bucket(resource_name, res)
            if res["Type"] == "AWS::Lambda::Function":
                self._lambda_function(resource_name, res)

        return self.policy

    def _s3_bucket(self, name, res):
        resource = "*"
        if "BucketName" in res:
            resource = "arn:aws:s3:::{0}".format(res["BucketName"])

        actions = ["s3:CreateBucket", "s3:DeleteBucket"]
        self._add_policy_statement(name, res, actions, resource)

    def _lambda_function(self, name, res):
        resource = "*"
        actions = ["lambda:CreateFunction"]
        if "VpcConfig" in res:
            actions += ["ec2:AllocateAddress", "ec2:AssociateAddress", "ec2:DisassociateAddress"]
        self._add_policy_statement(name, res, actions, resource, name_suffix="Global")

        resource = "*"
        if "FunctionName" in res:
            resource = "arn:aws:lambda:{0}:{1}:function:{2}".format(self.region, self.account, res["FunctionName"])
        actions = ["lambda:DeleteFunction"]
        self._add_policy_statement(name, res, actions, resource)

    def _add_policy_statement(self, res_name, res, actions, resource, name_suffix=None):
        res_type = res["Type"].split("AWS::")[1].replace("::", "-")
        sid = "Policy-Generator-{0}-{1}".format(res_type, res_name)
        if name_suffix is not None:
            sid += "-" + name_suffix
        self.policy["Statements"].append({
            "Sid": sid,
            "Statement": {
                "Effect": "Allow",
                "Action": actions,
                "Resource": resource
            }
        })
