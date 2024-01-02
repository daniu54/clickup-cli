import argparse
import json
import sys
from clickup import clickup_api, clickup_api_endpoint


def main():
    api_endpoint = clickup_api_endpoint.DEFAULT

    args = parse_args()

    api_token = args.api_token
    workspace = args.workspace_id
    stop_after_first_match = args.stop_after_first_match
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

    matches = clickup_api.find_tasks_in_workspace(
        workspace, filter, stop_after_first_match, api_token, api_endpoint
    )

    if matches:
        print(json.dumps(matches, indent=2))
        print(f"Found {len(matches)} matches", file=sys.stderr)
        sys.exit(0)

    print("Could not find any good matches, try to specify query more", file=sys.stderr)
    sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Searches tasks whose names match filter in given workspace. The search is case-insensitive and removes special characters"
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
    parser.add_argument(
        "--stop-after-first-match",
        action="store_true",
        help="Abort the search after first match is found",
    )

    return parser.parse_args()


if __name__ == "__main__":
    main()
