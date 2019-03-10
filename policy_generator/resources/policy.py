import logging

logger = logging.getLogger(__name__)


class Policy:

    def __init__(self, name, res, region=None, account=None):
        self.name = name
        self.res = res
        self.region = region
        self.account = account

        self.res_type = res["Type"].split("AWS::")[1].replace("::", "-")
        self.cloudformation_policies = {
            "PolicyDocument": {
                "Version": "2012-10-17",
                "Statements": []
            },
            "PolicyName": "Policy-Generator-{0}-{1}".format(self.res_type, self.name)
        }

    def create_policy(self):
        raise NotImplementedError("Please Implement create_policy")

    def _create_resource(self, resource_format, res_value):
        if type(res_value) == str and "!" not in res_value:
            logger.debug("Resource is a string, creating simple string resource")
            return resource_format.format(region=self.region, account=self.account, res_value=res_value)

        logger.debug("Resource is not a string, re-using same CloudFormation functions in !Sub")
        sub_variable_name = "{0}-{1}".format(self.res_type, self.name)
        resource_format = resource_format.format(res_value="${{{0}}}".format(sub_variable_name),
                                                 region=self.region,
                                                 account=self.account)

        return {
            "Fn::Sub": [
                resource_format,
                {sub_variable_name: res_value}
            ]
        }

    def _add_policy_statement(self, actions, resource, name_suffix=None):
        sid = "Policy-Generator-{0}-{1}".format(self.res_type, self.name)
        if name_suffix is not None:
            sid += "-" + name_suffix
        self.cloudformation_policies["PolicyDocument"]["Statements"].append({
            "Sid": sid,
            "Statement": {
                "Effect": "Allow",
                "Action": actions,
                "Resource": resource
            }
        })
