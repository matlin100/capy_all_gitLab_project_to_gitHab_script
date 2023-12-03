import os
import requests

# Set your GitLab and GitHub details
gitlab_url = "https://gitlab.com/api/v4"
gitlab_token = "...."
github_username = "..."
github_token = "...."

responses = []
# Get the list of GitLab projects
gitlab_project_ids = [
  # add yor id progect list here
]

# Iterate through specified GitLab projects and migrate to GitHub
for project_id in gitlab_project_ids:
    gitlab_repo_url = f"{gitlab_url}/projects/{project_id}"
    gitlab_headers = {"PRIVATE-TOKEN": gitlab_token}

    response = requests.get(gitlab_repo_url, headers=gitlab_headers)
    if response.status_code != 200:
        print(f"conet get requests for id ${project_id}")
    else:
        responses.append(response.json())


if len(responses) <= 0:
    print("There are no projects to copy.")
    exit()


# print("GitLab Projects:")
# for project in responses:
#     print(project)
# Iterate through GitLab projects and migrate to GitHub
for project in responses :
    gitlab_repo_url = project["http_url_to_repo"]
    gitlab_repo_name = project["name"]

    # Replace spaces with underscores in the repository name
    gitlab_repo_name_no_spaces = gitlab_repo_name.replace(" ", "_")

    # Step 1: Create a new repository on GitHub
    github_create_repo_url = "https://api.github.com/user/repos"
    github_create_repo_data = {
        "name": gitlab_repo_name_no_spaces,  # Use the modified name without spaces
        "private": False,  # Set to True if you want a private repository
    }
    github_create_repo_headers = {
        "Authorization": f"token {github_token}",
    }

    response = requests.post(
        github_create_repo_url,
        json=github_create_repo_data,
        headers=github_create_repo_headers,
    )

    if response.status_code != 201:
        print(f"Failed to create GitHub repository for {gitlab_repo_name}. Status code: {response.status_code}")
        print(response.text)
        continue

    print(f"GitHub repository '{gitlab_repo_name}' created successfully.")

    # Step 2: Clone the GitLab repository
    clone_command = f"git clone {gitlab_repo_url} {gitlab_repo_name_no_spaces}"  # Use the modified name without spaces
    os.system(clone_command)

    # Step 3: Change directory to the cloned repository
    os.chdir(gitlab_repo_name_no_spaces)  # Use the modified name without spaces

    # Step 4: Add the GitHub repository as a remote
    github_repo_url = f"https://github.com/{github_username}/{gitlab_repo_name_no_spaces}.git"  # Use the modified name without spaces
    os.system(f"git remote add github {github_repo_url}")

    # ... (your existing code)

    # Move back to the parent directory for the next iteration
    os.chdir("..")

print("All repository migrations completed successfully.")
