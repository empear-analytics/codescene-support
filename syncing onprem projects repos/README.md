
# Instruction Guide for Using the Scripts for Syncing On-Prem Projects Repos and Git Provider Repos

## Prerequisites
- **Python Installation:** Ensure you have Python installed on your machine. You can download it from [python.org](https://www.python.org/).
- **Install Required Libraries:** This script uses the `requests` library to make HTTP requests. Create the virtual environment using the following command:

```bash
    python3 -m venv venv
    source venv/bin/activate
    python3 -m pip install requests
```

## How to Create a GitHub Access Token
To create a GitHub access token, follow these steps:
1. **Log in to GitHub:** Log in to your GitHub Account and [create a new fine-grained personal access token](https://github.com/settings/personal-access-tokens/new)
2. **Set Permissions:**  Read-only access to Metadata is recommended with all repository access. 

## How to Create a CodeScene REST API User
To create a user intended for REST API consumption in CodeScene, follow this [link to CodeScene REST API Documentation](https://docs.enterprise.codescene.io/latest/integrations/rest-api.html#the-rest-api-user).

---

## 1. Configuration File
**File:** `config.json`  
**Description:** Stores the configuration for both CodeScene and GitHub settings.

Edit the `config.json` file to input your configuration details:

```json
{
    "codescene": {
        "url": "https://your-codescene-domain.io",
        "username": "your_username",
        "password": "your_password"
    },
    "github": {
        "org": "your_github_org",
        "token": "your_github_token"
    }
}
```

*** DO NOT COMMIT TOKENS AND PASSWORDS  *** 

---

## 2. Syncing GitHub and CodeScene automated using config
**File:** `sync_github_codescene_config.py`  
**Description:** Compares the repositories between GitHub and CodeScene, identifying any missing or unlinked repositories.

Run the script:

```bash
python sync_github_codescene_config.py
```

The output will be saved to:
- `missing_github_repos.txt`: Lists projects without corresponding GitHub repositories. This file identifies which projects in CodeScene do not have linked repositories in GitHub, meaning that the associated GitHub repository may have been deleted or never existed.
- `unlinked_github_repos.txt`: Lists GitHub repositories without corresponding CodeScene projects. This file highlights GitHub repositories that are not linked to any projects in CodeScene, ensuring you are aware of which repositories need to be associated.
---

## 3. Syncing GitHub and CodeScene with input
**File:** `sync_github_codescene_input.py`  
**Description:** Use this script if you prefer not to use the configuration file. You can input the required data via prompts. This script compares the repositories between GitHub and CodeScene, identifying any missing or unlinked repositories.

Run the script:

```bash
python sync_github_codescene_input.py
```

- Enter your GitHub organization name and access token when prompted.
- Enter the CodeScene API URL, username, and password when prompted.

The output will be saved to:
- `missing_github_repos.txt`: Lists projects without corresponding GitHub repositories. This file identifies which projects in CodeScene do not have linked repositories in GitHub, meaning that the associated GitHub repository may have been deleted or never existed.
- `unlinked_github_repos.txt`: Lists GitHub repositories without corresponding CodeScene projects. This file highlights GitHub repositories that are not linked to any projects in CodeScene, ensuring you are aware of which repositories need to be associated.
---

## The following scripts help you easily retrieve project information from CodeScene and GitHub

## 4. Fetching CodeScene Projects
**File:** `fetch_codescene_repos.py`  
**Description:** Retrieves a list of projects from your CodeScene instance.

### Usage
Run the script:

```bash
python fetch_codescene_repos.py
```

- Enter the CodeScene API URL, username, and password when prompted.
- The list of CodeScene projects and their remote URLs will be saved to `codescene_projects.txt`.

---

## 5. Fetching GitHub Repositories
**File:** `fetch_github_repos.py`  
**Description:** Retrieves the list of repositories from your specified GitHub organization.

### Usage
Run the script:

```bash
python fetch_github_repos.py
```

- Enter your GitHub organization name and access token when prompted.
- The list of repositories will be saved to `list_of_github_repos.txt`.

---

