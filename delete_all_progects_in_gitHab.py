import requests

# Set your GitHub details
github_username = "..."
github_token = "...."  # Make sure this token has the 'delete_repo' scope

# Get the list of your repositories
github_repos_url = f"https://api.github.com/users/{github_username}/repos"
headers = {
    "Authorization": f"token {github_token}",
    "Accept": "application/vnd.github.v3+json"
}

response = requests.get(github_repos_url, headers=headers)

if response.status_code != 200:
    print(f"Failed to fetch GitHub repositories. Status code: {response.status_code}")
    print(response.text)
    exit()

github_repos = response.json()

# Delete each repository
for repo in github_repos:
    repo_name = repo["name"]
    repo_url = f"https://api.github.com/repos/{github_username}/{repo_name}"

    response = requests.delete(repo_url, headers=headers)

    if response.status_code == 204:
        print(f"Repository '{repo_name}' deleted successfully.")
    else:
        print(f"Failed to delete repository '{repo_name}'. Status code: {response.status_code}")
        print(response.text)
