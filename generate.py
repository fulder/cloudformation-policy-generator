import argparse
import json
import yaml

from policy_generator.policy_generator import PolicyGenerator

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
