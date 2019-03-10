from policy_generator.resources.policy import Policy


class LambdaFunction(Policy):

    def __init__(self, name, res, region, account):
        super(LambdaFunction, self).__init__(name, res, region, account)

    def create_policy(self):
        resource = "*"
        actions = ["lambda:CreateFunction"]
        if "VpcConfig" in self.res:
            actions += ["ec2:AllocateAddress", "ec2:ReleaseAddress", "ec2:DescribeAddresses"]
        self._add_policy_statement(actions, resource, name_suffix="Global")

        actions = ["iam:PassRole"]
        resource = self._create_resource("{res_value}", self.res["Role"])
        self._add_policy_statement(actions, resource, name_suffix="Role")

        resource = "*"
        if "FunctionName" in self.res:
            resource = self._create_resource("arn:aws:lambda:{region}:{account}:function:{res_value}",
                                             self.res["FunctionName"])
        actions = ["lambda:DeleteFunction"]
        self._add_policy_statement(actions, resource)
        return self.cloudformation_policies
