import requests
import pandas as pd

# GitHub API URL template
BASE_URL = "https://api.github.com/users/{username}/repos"
h = open("config.txt")
username = h.readline().strip()
data_dir = h.readline().strip()
h.close()

# Function to get repository data
def fetch_repos(username):
    # URL for the GitHub API call
    url = BASE_URL.format(username=username)
    
    # Make the API request
    response = requests.get(url)
    
    # Check for successful response
    if response.status_code != 200:
        print(f"Error: Unable to fetch data for user {username}. Status Code: {response.status_code}")
        return None
    
    # Parse JSON response
    repos = response.json()

    # If no repositories are found
    if len(repos) == 0:
        print(f"No repositories found for user {username}")
        return None

    # Create a list to store the repository details
    repo_data = []
    
    # Loop through repositories and extract key information
    for repo in repos:
        repo_info = {
            "Repository Name": repo["name"],
            "Description": repo["description"],
            "Stars": repo["stargazers_count"],
            "Forks": repo["forks_count"],
            "Watchers": repo["watchers_count"],
            "Primary Language": repo["language"],
            "Repo Size (KB)": repo["size"],
            "URL": repo["html_url"]
        }
        repo_data.append(repo_info)

    # Convert the data to a pandas DataFrame for easy viewing
    df = pd.DataFrame(repo_data)

    return df

# Fetch and display the repository data
repo_df = fetch_repos(username)

# Check if data was returned
if repo_df is not None:
    print(f"\nRepositories for user {username}:")
    print(repo_df)
    # Optionally save the data to CSV
    repo_df.to_csv(f"{data_dir}/{username}_repos.csv", index=False)