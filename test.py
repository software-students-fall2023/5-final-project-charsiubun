import requests
from datetime import datetime, timezone, timedelta

def get_github_user_year_contributions(username, github_token):
    # Define the GraphQL query
    graphql_query = """
    query ContributionsView($username: String!, $from: DateTime!, $to: DateTime!) {
        user(login: $username) {
            contributionsCollection(from: $from, to: $to) {
                totalCommitContributions
                totalIssueContributions
                totalPullRequestContributions
                totalPullRequestReviewContributions
            }
        }
    }
    """

    # Define the date range
    to_date = datetime.now().isoformat()
    from_date = (datetime.now() - timedelta(days=365)).isoformat()

    # Prepare the request payload
    json = {
        "query": graphql_query,
        "variables": {
            "username": username,
            "from": from_date,
            "to": to_date
        }
    }

    headers = {"Authorization": f"Bearer {github_token}"}

    response = requests.post("https://api.github.com/graphql", json=json, headers=headers)

    if response.status_code == 200:
        return response.json()['data']['user']['contributionsCollection']
    else:
        return {"error": f"Failed to fetch data, status code: {response.status_code}"}


def get_user_contributed_repos(username, github_token):
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.cloak-preview'  # Required for commit search
    }

    # Define the date range (last year)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    query = f'author:{username} committer-date:{start_date_str}..{end_date_str}'
    search_url = f'https://api.github.com/search/commits?q={query}'

    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        search_results = response.json()
        repos_info = {}

        for item in search_results['items']:
            repo_name = item['repository']['full_name']
            if repo_name not in repos_info:
                # Fetch languages for this repository
                languages_url = f'https://api.github.com/repos/{repo_name}/languages'
                lang_response = requests.get(languages_url, headers=headers)
                if lang_response.status_code == 200:
                    repos_info[repo_name] = lang_response.json()
                else:
                    repos_info[repo_name] = "Failed to fetch languages"

        return repos_info
    else:
        return {"error": f"Failed to fetch data, status code: {response.status_code}"}


def get_github_user_details(username, github_token):
    headers = {'Authorization': f'token {github_token}'}
    user_response = requests.get(f'https://api.github.com/users/{username}', headers=headers)

    if user_response.status_code == 200:
        user_data = user_response.json()
        cleaned_data = {
            'Username': username,
            'Public Repos': user_data['public_repos'],
            'Followers': user_data['followers'],
            'Account Created': user_data['created_at'],
            'Last Updated': user_data['updated_at'],
            'Recent Activity': (datetime.now(timezone.utc) - timedelta(days=365)).day,
            'Following Count': len(requests.get(user_data['following_url'].replace('{/other_user}', ''), headers=headers).json())
        }
    
        year_contributions = get_github_user_year_contributions(username, github_token)
        cleaned_data['Year Contributions'] = year_contributions
        contributed_repos = get_user_contributed_repos(username, github_token)
        cleaned_data['Contributed Repos'] = contributed_repos

        one_year_ago = datetime.now(timezone.utc) - timedelta(days=365)
        recent_repos_data = []

        repos_url = user_data.get('repos_url', '')
        repos_response = requests.get(repos_url, headers=headers)
        if repos_response.status_code == 200:
            repos_data = repos_response.json()

            # Filter for repositories updated in the last year
            one_year_ago = datetime.now(timezone.utc) - timedelta(days=365)
            recent_repos_data = []

            for repo in repos_data:
                updated_at = datetime.fromisoformat(repo['updated_at'].rstrip('Z')).replace(tzinfo=timezone.utc)
                if updated_at >= one_year_ago:
                    repo_detail = {
                        'Name': repo['name'],
                        'Last Updated': repo['updated_at'],
                        'Stars': repo['stargazers_count'],
                        'Forks': repo['forks_count']
                    }

                    # Fetch languages for this repository
                    languages_url = f'https://api.github.com/repos/{repo["full_name"]}/languages'
                    lang_response = requests.get(languages_url, headers=headers)
                    if lang_response.status_code == 200:
                        repo_detail['Languages'] = lang_response.json()
                    else:
                        repo_detail['Languages'] = "Failed to fetch languages"

                    recent_repos_data.append(repo_detail)

            cleaned_data['Recent Repositories'] = recent_repos_data
        else:
            print(f"Error fetching repositories: {repos_response.status_code}")

        return cleaned_data
    else:
        return {"error": "User not found"}


# Replace with your GitHub token
GITHUB_TOKEN = "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"

# Replace with a GitHub username to test
#TEST_USERNAME = "PatrickZhao0"
TEST_USERNAME = "BREADLuVER"
#TEST_USERNAME = "Spectraorder"
#BREADLuVER
#Spectraorder

user_details = get_github_user_details(TEST_USERNAME, GITHUB_TOKEN)

print(user_details)

def calculate_rating(data):
    # Extract distinct languages
    languages = set()
    for repo in data['Contributed Repos'].values():
        languages.update(repo.keys())
    for repo in data['Recent Repositories']:
        languages.update(repo['Languages'].keys())

    # Calculate the total repository count
    total_repo_count = len(data['Contributed Repos']) + data['Public Repos']

    # Pull request activities
    total_pr_activities = data['Year Contributions']['totalPullRequestContributions'] + data['Year Contributions']['totalPullRequestReviewContributions']

    # Assign weights (example weights, can be adjusted)
    W1, W2, W3, W4 = 0.1, 1, 0.5, 0.3

    # Calculate rating
    rating = (W1 * len(languages)) + (W2 * data['Year Contributions']['totalCommitContributions']) 
    + (W3 * total_pr_activities) + (W4 * total_repo_count)

    return rating

rating = calculate_rating(user_details)
print(f"GitHub User Rating: {rating}")
