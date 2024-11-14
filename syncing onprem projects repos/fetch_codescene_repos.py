
import getpass

try:
    import requests
except ImportError:
    print("Module 'requests' is not installed. Please install it using 'pip install requests'.")
    sys.exit(1)

# Input CodeScene API
def get_user_input():
    url = input("Enter the CodeScene API URL: ")
    username = input("Enter your CodeScene username: ")
    password = getpass.getpass("Enter your CodeScene password: ")
    return url, username, password

def fetch_project_details(url, project_ref, headers, auth):
    project_detail_url = f"{url}{project_ref}"
    detail_response = requests.get(project_detail_url, headers=headers, auth=auth)
    
    if detail_response.status_code == 200:
        return detail_response.json().get('configured_git_remote_urls', [])
    else:
        print(f"Error fetching details for project {project_ref}: {detail_response.status_code} {detail_response.text}")
        return []

def fetch_codescene_projects(url, username, password):
    api_url = f"{url}/api/v2/projects"
    headers = {'accept': 'application/json'}
    auth = (username, password)

    response = requests.get(api_url, headers=headers, auth=auth)
    
    if response.status_code == 200:
        projects = response.json().get("projects", [])
        save_projects_to_file(projects, url, headers, auth)
    else:
        print(f"Error fetching projects: {response.status_code} {response.text}")

def save_projects_to_file(projects, url, headers, auth):
    with open("codescene_projects.txt", "w") as file:
        for project in projects:
            project_name = project['name']
            project_ref = project['ref']
            remote_urls = fetch_project_details(url, project_ref, headers, auth)

            file.write(f"{project_name}\n")
            for remote_url in remote_urls:
                file.write(f"- {remote_url}\n")
            file.write("\n")
    
    print(f"Project list saved to 'codescene_projects.txt'.")

# Main execution
if __name__ == "__main__":
    url, username, password = get_user_input()
    fetch_codescene_projects(url, username, password)
