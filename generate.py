import argparse
import json
import yaml

from policy_generator.role_generator import RoleGenerator

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CloudFormation Role Generator")
    parser.add_argument("-f", "--file", help="Path to the CloudFormation JSON/YAML template", required=True)
    parser.add_argument("-r", "--region", help="AWS Region name e.g. 'us-east-1'", required=True)
    parser.add_argument("-a", "--account", help="AWS Account number", required=True)
    parser.add_argument("-cff", "--cloud_formation_format", help="json/yaml, default yaml", default="yaml")
    parser.add_argument("-o", "--out", help="Save output to the specified file")
    args = parser.parse_args()

    cloud_formation_dict = yaml.safe_load(open(args.file, "r"))
    generated_policy = RoleGenerator(cloud_formation_dict, args.region, args.account).generate()

    if args.out is not None:
        with open(args.out, "w") as outfile:
            if args.cloud_formation_format == "yaml":
                yaml.safe_dump(generated_policy, outfile, default_flow_style=False)
            elif args.cloud_formation_format == "json":
                json.dump(generated_policy, outfile, indent=2)
    else:
        print(generated_policy)
