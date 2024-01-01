import argparse
import json
import sys
from clickup import clickup_api, clickup_api_endpoint


def main():
    api_endpoint = clickup_api_endpoint.DEFAULT

    args = parse_args()

    api_token = args.api_token
    workspace = args.workspace_id
    filter = " ".join(args.filter)

    if not workspace:
        workspaces = clickup_api.get_workspaces(api_token, api_endpoint)

        workspaces_pretty = [
            {"id": workspace["id"], "name": workspace["name"]}
            for workspace in workspaces
        ]

        print(
            "You did not provide a --workspace-id argument. Available workspaces include:"
        )
        print(workspaces_pretty)

        sys.exit(1)

    match = clickup_api.find_task_in_workspace(
        workspace, filter, api_token, api_endpoint
    )

    if match is not None:
        print("Found match:", file=sys.stderr)
        print(json.dumps(match, indent=2))
        sys.exit(0)

    print("Could not find good match, try to specify query more", file=sys.stderr)
    sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Searches tasks whose names match filter in given workspace. The search is case-insensitive"
    )

    parser.add_argument("filter", nargs="+", help="Search terms for task name")
    parser.add_argument(
        "--api-token",
        required=True,
        help="Your personal API token. See https://clickup.com/api/developer-portal/authentication for more info",
    )
    parser.add_argument(
        "--workspace-id",
        required=False,
        help="Workspace id to search in. Run with no value to see which workspaces are available",
    )

    return parser.parse_args()


if __name__ == "__main__":
    main()
