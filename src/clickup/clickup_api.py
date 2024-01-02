import re
import sys
import requests

from urllib.parse import urljoin

from typing import List


def get_workspaces(api_token: str, endpoint: str) -> List[object]:
    url = urljoin(endpoint, "team")

    headers = {"Authorization": api_token}

    response = requests.get(url, headers=headers)

    assert (
        response.status_code == 200
    ), f"expected response to indicate success, got {response}"

    workspaces = response.json()["teams"]

    return workspaces


def get_spaces(workspace_id: str, api_token: str, endpoint: str) -> List[object]:
    url = urljoin(endpoint, f"team/{workspace_id}/space")

    headers = {"Authorization": api_token}

    query = {"archived": "false"}

    response = requests.get(url, headers=headers, params=query)

    assert (
        response.status_code == 200
    ), f"expected response to indicate success, got {response}"

    spaces = response.json()["spaces"]

    return spaces


def get_folders(space_id: str, api_token: str, endpoint: str) -> List[object]:
    url = urljoin(endpoint, f"space/{space_id}/folder")

    headers = {"Authorization": api_token}

    query = {"archived": "false"}

    response = requests.get(url, headers=headers, params=query)

    assert (
        response.status_code == 200
    ), f"expected response to indicate success, got {response}"

    folders = response.json()["folders"]

    return folders


def get_lists(folder_id: str, api_token: str, endpoint: str) -> List[object]:
    url = urljoin(endpoint, f"folder/{folder_id}/list")

    headers = {"Authorization": api_token}

    query = {"archived": "false"}

    response = requests.get(url, headers=headers, params=query)

    assert (
        response.status_code == 200
    ), f"expected response to indicate success, got {response}"

    lists = response.json()["lists"]

    return lists


def get_tasks_in_list(list_id: str, api_token: str, endpoint: str) -> List[object]:
    url = urljoin(endpoint, f"list/{list_id}/task")

    headers = {"Authorization": api_token}

    query = {"archived": "false"}

    response = requests.get(url, headers=headers, params=query)

    assert (
        response.status_code == 200
    ), f"expected response to indicate success, got {response}"

    tasks = response.json()["tasks"]

    return tasks


def get_tasks_in_workspace(workspace: str, api_token: str, api_endpoint: str):
    for space in get_spaces(workspace, api_token, api_endpoint):
        space_id = space["id"]
        space_name = space["name"]

        for folder in get_folders(space_id, api_token, api_endpoint):
            folder_id = folder["id"]
            folder_name = folder["name"]

            for list in get_lists(folder_id, api_token, api_endpoint):
                list_id = list["id"]
                list_name = list["name"]
                print(
                    f"Searching list {list_name} in {space_name}/{folder_name}",
                    file=sys.stderr,
                )

                for task in get_tasks_in_list(list_id, api_token, api_endpoint):
                    yield task


def find_tasks_in_workspace(
    workspace: str,
    filter: str,
    stop_after_first_match: bool,
    api_token: str,
    api_endpoint: str,
):
    tasks = get_tasks_in_workspace(workspace, api_token, api_endpoint)

    filter = simplify_string(filter)

    matches = []

    for task in tasks:
        if stop_after_first_match and len(matches) >= 1:
            break

        task_name = simplify_string(task["name"])
        task_id = simplify_string(task["id"])

        if filter in task_id or filter in task_name:
            print(
                f"Found match for '{filter}' task id: '{task_id}' task name: '{task_name}'",
                file=sys.stderr,
            )
            matches.append(task)

    return matches


def simplify_string(s: str) -> str:
    s = s.strip()  # remove leading and trailing whitespace
    s = s.lower()  # lowercase
    s = re.sub(r"\s+", " ", s)  # remove excessive whitespace between words

    return s
