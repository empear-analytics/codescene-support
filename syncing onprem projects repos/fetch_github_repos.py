import getpass
import argparse

try:
    import requests
except ImportError:
    print("Module 'requests' is not installed. Please install it using 'pip install requests'.")
    sys.exit(1)

parser = argparse.ArgumentParser(description="Fetch repositories from GitHub")
parser.add_argument("--org", help="GitHub organization")
args = parser.parse_args()

if args.org is None:
    github_org = input("Enter your GitHub organization: ")
else:
    github_org = args.org

github_token = getpass.getpass("Enter your GitHub access token: ")


github_api_url = f"https://api.github.com/orgs/{github_org}/repos"

def fetch_github_repos():
    headers = {'Authorization': f'token {github_token}'}
    repos = []
    page = 1

    while True:
        response = requests.get(github_api_url, headers=headers, params={'page': page, 'per_page': 100})
        
        if response.status_code == 200:
            page_repos = response.json()
            if not page_repos:
                break 
            repos.extend(page_repos)
            page += 1
        else:
            print(f"Error fetching repositories: {response.status_code} {response.text}")
            break

    with open("list_of_github_repos.txt", "w") as file:
        file.write("List of repositories on GitHub:\n")
        for repo in repos:
            file.write(f"- {repo['name']} ({repo['html_url']})\n")

    print(f"\nRepository list saved to 'list_of_github_repos.txt'.")

if __name__ == "__main__":
    fetch_github_repos()