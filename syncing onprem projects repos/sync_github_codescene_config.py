import time
import sys
import threading
import json

try:
    import requests
except ImportError:
    print("Module 'requests' is not installed. Please install it using 'pip install requests'.")
    sys.exit(1)

def loading_spinner(message, stop_event):
    spinner = ['|', '/', '-', '\\']
    while not stop_event.is_set():
        for symbol in spinner:
            if stop_event.is_set():
                break
            sys.stdout.write(f'\r{message} {symbol}')
            sys.stdout.flush()
            time.sleep(0.1)
    sys.stdout.write(f'\r{message} Done!          \n') 
    sys.stdout.flush()

def fetch_github_repos(github_token, github_org):
    github_api_url = f"https://api.github.com/orgs/{github_org}/repos"
    headers = {'Authorization': f'token {github_token}'}
    repos = {}
    page = 1

    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=loading_spinner, args=("Fetching GitHub repositories...", stop_event))
    spinner_thread.start()

    while True:
        response = requests.get(github_api_url, headers=headers, params={'page': page, 'per_page': 100})
        
        if response.status_code == 200:
            page_repos = response.json()
            if not page_repos:
                break 
            for repo in page_repos:
                repos[repo['name']] = repo['html_url']
            page += 1
        else:
            print(f"Error fetching repositories: {response.status_code} {response.text}")
            break

    stop_event.set() 
    spinner_thread.join()
    return repos

def fetch_codescene_projects(url, username, password):
    api_url = f"{url}/api/v2/projects"
    headers = {'accept': 'application/json'}
    
    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=loading_spinner, args=("Fetching CodeScene projects...", stop_event))
    spinner_thread.start()

    response = requests.get(api_url, headers=headers, auth=(username, password))
    
    if response.status_code == 200:
        projects_data = response.json()
        projects = projects_data.get("projects", [])
        project_details = {}

        for project in projects:
            project_name = project['name']
            project_detail_url = f"{url}{project['ref']}"  
            
            detail_response = requests.get(project_detail_url, headers=headers, auth=(username, password))
            
            if detail_response.status_code == 200:
                project_details_data = detail_response.json()
                remote_urls = project_details_data.get('configured_git_remote_urls', [])
                project_details[project_name] = remote_urls
            else:
                print(f"Error fetching details for project {project_name}: {detail_response.status_code} {detail_response.text}")

        stop_event.set()
        spinner_thread.join()
        return project_details
    else:
        print(f"Error fetching projects: {response.status_code} {response.text}")
        stop_event.set()
        spinner_thread.join()
        return {}

def find_missing_github_repos(codescene_projects, github_repos):
    missing_github = {
        project_name: [
            remote_url for remote_url in remote_urls
            if remote_url.split('/')[-1].replace('.git', '') not in github_repos
        ]
        for project_name, remote_urls in codescene_projects.items()
    }
    
    return {k: v for k, v in missing_github.items() if v}

def find_unlinked_github_repos(github_repos, codescene_projects):
    unlinked_github = [
        (repo_name, repo_url) for repo_name, repo_url in github_repos.items()
        if not any(repo_name in remote_urls for remote_urls in codescene_projects.values())
    ]
    
    return unlinked_github

def write_missing_repos_to_file(missing_github):
    with open("missing_github_repos.txt", "w") as file:
        file.write("Projects without corresponding GitHub repositories:\n")
        file.write("---------------------------------------------------\n")
        for project, repos in missing_github.items():
            file.write(f"{project}\n")
            for repo in repos:
                file.write(f"- {repo}\n")
            file.write("---------------------------------------------------\n")
        file.write("---------------------------------------------------\n")
    print(f"Missing GitHub repositories saved to 'missing_github_repos.txt'.")

def write_unlinked_repos_to_file(unlinked_github):
    with open("unlinked_github_repos.txt", "w") as file:
        file.write("GitHub repositories without corresponding CodeScene projects:\n")
        for repo_name, repo_url in unlinked_github:
            file.write(f"- {repo_name} ({repo_url})\n")
    print(f"Unlinked GitHub repositories saved to 'unlinked_github_repos.txt'.")

def compare_repos(github_repos, codescene_projects):
    missing_github = find_missing_github_repos(codescene_projects, github_repos)
    unlinked_github = find_unlinked_github_repos(github_repos, codescene_projects)

    write_missing_repos_to_file(missing_github)
    write_unlinked_repos_to_file(unlinked_github)

def load_config(filename='config.json'):
    try:
        with open(filename, 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print(f"Error: The '{filename}' file was not found.")
        sys.exit(1) 
    except json.JSONDecodeError:
        print(f"Error: The '{filename}' file contains invalid JSON.")
        sys.exit(1)

if __name__ == "__main__":
    config = load_config()

    codescene_config = config.get('codescene')
    github_config = config.get('github')

    if not codescene_config or not github_config:
        print("Error: Missing required configuration for CodeScene or GitHub.")
        sys.exit(1)

    required_codescene_keys = ['url', 'username', 'password']
    required_github_keys = ['token', 'org']

    for key in required_codescene_keys:
        if key not in codescene_config:
            print(f"Error: Missing required CodeScene configuration item '{key}'.")
            sys.exit(1)

    for key in required_github_keys:
        if key not in github_config:
            print(f"Error: Missing required GitHub configuration item '{key}'.")
            sys.exit(1)

    github_repos = fetch_github_repos(github_config['token'], github_config['org'])
    codescene_projects = fetch_codescene_projects(codescene_config['url'], codescene_config['username'], codescene_config['password'])
    
    compare_repos(github_repos, codescene_projects)
