from policy_generator.resources.policy import Policy


class CloudFormation(Policy):

    def __init__(self):
        super(CloudFormation, self).__init__("MainCloudFormation", {"Type": "AWS::CloudFormation"})

    def create_policy(self):
        resource = "*"
        actions = ["cloudformation:CreateStack", "cloudformation:UpdateStack", "cloudformation:DescribeStacks"]
        self._add_policy_statement(actions, resource)
        return self.cloudformation_policies
