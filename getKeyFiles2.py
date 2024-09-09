import requests

# GitHub API base URL for repository contents
CONTENTS_URL = "https://api.github.com/repos/{username}/{repo}/contents"

# File types to prioritize for analysis
KEY_CODE_FILE_TYPES = ['.py', '.js', '.java', '.cpp', '.c', '.rb', '.go', '.rs']

# Maximum file size threshold (in KB)
MAX_FILE_SIZE = 100  # Files larger than this size will be skipped

# Initialize an empty list to store file URLs
file_urls = []
h = open("config.txt")
username = h.readline().strip()
data_dir = h.readline().strip()
h.close()

# Function to get the file tree of a repository
def fetch_repo_contents(username, repo, path=""):
    """
    Fetch the contents of the repository at the specified path.
    If path is empty, it fetches the root directory.
    """
    url = CONTENTS_URL.format(username=username, repo=repo)
    if path:
        url += f"/{path}"

    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error: Unable to fetch contents for {repo}. Status Code: {response.status_code}")
        return None

    return response.json()

# Function to identify and filter key code files based on type and size
def extract_key_files(username, repo, path=""):
    """
    Recursively fetch files from the repository and filter by file type and size.
    """
    contents = fetch_repo_contents(username, repo, path)
    if not contents:
        return []

    key_files = []

    for item in contents:
        # If the item is a directory, recursively fetch its contents
        if item['type'] == 'dir':
            key_files += extract_key_files(username, repo, item['path'])
        # If the item is a file, check the file type and size
        elif item['type'] == 'file':
            file_name = item['name']
            file_size_kb = item['size'] / 1024  # Convert size from bytes to KB

            # Only include files that match the desired types and are within size threshold
            if any(file_name.endswith(ext) for ext in KEY_CODE_FILE_TYPES) and file_size_kb <= MAX_FILE_SIZE:
                key_files.append({
                    "File Name": file_name,
                    "Path": item['path'],
                    "Size (KB)": round(file_size_kb, 2),
                    "Download URL": item['download_url']
                })
                # Append the download URL to the global list
                file_urls.append(item['download_url'])

    return key_files

# Function to extract key files from all repos of a user
def fetch_key_files_for_all_repos(username):
    # Fetch user's repositories
    repos_url = f"https://api.github.com/users/{username}/repos"
    repos_response = requests.get(repos_url)

    if repos_response.status_code != 200:
        print(f"Error: Unable to fetch repos for {username}. Status Code: {repos_response.status_code}")
        return None

    repos = repos_response.json()

    # Loop through all repositories and extract key files
    all_key_files = []
    for repo in repos:
        print(f"\nFetching key files for repository: {repo['name']}")
        key_files = extract_key_files(username, repo['name'])
        if key_files:
            all_key_files.append({
                "Repository": repo['name'],
                "Key Files": key_files
            })

    return all_key_files

# Fetch key files from all repositories for the user
key_files_data = fetch_key_files_for_all_repos(username)

with open(f"{data_dir}/{username}_fileUrls.txt","a") as f:
    f.write(username+"\n")
    for i in file_urls:
        f.write(i+"\n")