from dotenv import load_dotenv
load_dotenv()

import requests
from datetime import datetime, timezone, timedelta
import random
import os

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
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')

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
    total_pr_activities = (data['Year Contributions']['totalPullRequestReviewContributions'] 
                          + data['Year Contributions']['totalIssueContributions'])

    # Total contributions
    total_contributions = (data['Year Contributions']['totalPullRequestContributions'] 
                          + data['Year Contributions']['totalCommitContributions'])

    total_forks = sum([repo.get('Forks', 0) for repo in data['Recent Repositories']])

    total_lines_contributed = sum([lines for repo in data['Recent Repositories'] for _, lines in repo.get('Languages', {}).items()])

    # Adjusted weights for new metrics
    W1 = 0.05  # Languages Used
    W2 = 0.5  # Total Contributions
    W3 = 0.02  # PR Activities
    W4 = 0.02  # Repository Count
    W6 = 0.01  # Forks
    W9 = 0.40  # Total Lines Contributed

    # Calculate raw rating with new metrics
    raw_rating = (W1 * len(languages)) + (W2 * total_contributions) + (W3 * total_pr_activities) 
    + (W4 * total_repo_count) + (W6 * total_forks)
    + (W9 * total_lines_contributed)

    # Print weighted values for debugging
    #print(f"Weighted Language Count: {W1 * len(languages)}")
    #print(f"Weighted Total Contributions: {W2 * total_contributions}")
    #print(f"Weighted PR Activities: {W3 * total_pr_activities}")
    #print(f"Weighted Repository Count: {W4 * total_repo_count}")
    #print(f"Weighted Forks: {W6 * total_forks}")
    #print(f"Weighted Lines Contributed: {W9 * total_lines_contributed}")

    max_languages = 10
    max_commit_contributions = 450
    max_pr_activities = 100
    max_repo_count = 30
    max_forks = 30
    max_lines_contributed = 400000

    # Calculate maximum possible rating
    max_rating = (W1 * max_languages) + (W2 * max_commit_contributions) + (W3 * max_pr_activities) 
    + (W4 * max_repo_count) + (W6 * max_forks)
    + (W9 * max_lines_contributed)

    # Print max values for debugging
    #print(f"Max Language: {W1 * max_languages}")
    #print(f"Max Total Contributions: {W2 * max_commit_contributions}")
    #print(f"Max PR Activities: {W3 * max_pr_activities}")
    #print(f"Max Repository Count: {W4 * max_repo_count}")
    #print(f"Max Forks: {W6 * max_forks}")
    #print(f"Max Lines Contributed: {W9 * max_lines_contributed}")

    # Normalize the rating to a 0-100 scale
    normalized_rating = round(((raw_rating / max_rating) * 40) + 60, 2)

    #print(f"Raw Rating: {raw_rating}")
    #print(f"Max Rating: {max_rating}")
    #print(f"Normalized Rating: {normalized_rating}")

    return normalized_rating


def get_feedback(username, score):
    high_score_roasts = [
        "🤓",
        "🤓",
        f"{username}'s GitHub is so dense, even black holes are taking notes.",
        f"If there was a 'commit-ment' award, {username} would be a lifetime achiever.",
        f"Hey {username}, ever thought of 'branching' out to a social life?",
        f"I guess for {username}, 'social network' means Git branches talking to each other.",
        f"{username} codes like they're trying to solve world hunger through pull requests.",
        f"Is 'Ctrl+C, Ctrl+V' {username}'s idea of a balanced diet?",
        f"Someone tell {username} that 'Merge Conflicts' isn't a new Netflix series.",
        f"Legend says {username} once exited Vim, and it's been a folklore since.",
        f"If code cleanliness was next to godliness, {username} would be a deity.",
        f"{username} might be the only person to read GitHub docs for bedtime stories.",
        f"{username}'ve got more commits than a book has words!",
        f"Is {username}'s home address localhost?",
        f"{username}'re the human embodiment of 'It works on my machine.'",
        f"{username}'s keyboard must be applying for a restraining order any day now.",
        f"I bet {username} dream in code, don’t {username}?",
        f"{username}'s GitHub is so active, it needs its own social life!",
        f"{username}'ve got more branches than a tree in spring.",
        f"I’d tell {username} to go outside, but {username} might just find a way to commit from there too.",
        f"{username}'s coffee machine is probably the only one that understands {username} best.",
        f"{username} must mistake the sound of typing for applause.",
        f"If GitHub stars were money, {username}'d be on Forbes.",
        f"Do {username} wear sunglasses to protect from the brightness of {username}'s own screen?",
        f"I guess {username}'s first word was 'commit', wasn’t it?",
        f"{username} don't get bugs; {username} get 'unexpected features', right?",
        f"If {username} were a movie, {username}'d be called 'Lord of the Commits: The Fellowship of the Code'.",
        f"{username}'s codebase is bigger than my future.",
        f"Even {username}'s pet knows how to push to GitHub, huh?",
        f"Is {username}'s favorite snack a byte?",
        f"{username}'s love for coding is the only thing not needing debugging.",
        f"{username} might be the only person who read the entire terms and conditions before accepting."
    ]

    medium_score_roasts = [
        f"Is {username}'s code editor just a glorified diary?",
        f"Looks like {username} treats their GitHub like a gym membership – rarely used but always there.",
        f"For {username}, 'git commit' is as elusive as a UFO sighting.",
        f"Hey {username}, heard you were looking for the 'commit' button under the couch cushions.",
        f"{username}’s coding philosophy: Why do today what you can push to the next sprint?",
        f"{username} plays hide-and-seek with their code – now you see a commit, now you don't.",
        f"I guess {username} thinks GitHub is a place where you store vintage, unused code.",
        f"It seems {username} likes their coffee more than their IDE.",
        f"Is {username}’s favorite Git command 'git –-take-a-break'?",
        f"{username} treats their repositories like cacti – water them once a year and hope for the best.",
        f"So, {username} code occasionally? Like every leap year?",
        f"{username}'s GitHub graph has more breaks than a Kit-Kat bar.",
        f"{username} must be a ninja; {username} leave no traces in {username} repositories.",
        f"Are {username} playing hard to get with {username} code editor?",
        f"{username} and GitHub sitting in a tree, C-O-M-M-I-T-T-I-N-G... occasionally.",
        f"Is {username}'s IDE just a glorified notepad for {username}?",
        f"{username} must be a part-time coder and a full-time '404 not found'.",
        f"{username}'re the 'I’ll fix this bug later' kind of person, aren't {username}?",
        f"{username}'s commit history is like a mysterious novel – updated rarely but interesting.",
        f"{username} treat coding like a treadmill – great intentions but rarely used.",
        f"I bet {username}'s favorite Git command is 'blame'.",
        f"{username}'re like a Monday morning coder – a slow start but gets there eventually.",
        f"Is {username}'s coding philosophy 'Less is more'?",
        f"{username}'s code is like a shooting star – rare and surprising.",
        f"{username} must be an artist; {username} leave so much whitespace.",
        f"Looks like {username} maintain a healthy balance between the real world and the matrix.",
        f"{username}’re not a coder; {username}’re a ‘coding enthusiast’.",
        f"Are {username} repositories just for decoration?",
        f"{username}'s favorite part of coding must be the 'end'.",
        f"{username} only code on days that end in 'y', but only if {username} feel like it."
    ]


    low_score_compliments = [
        f"{username}’s life is so colorful even their code is jealous.",
        f"While we’re debugging, {username} is busy living the dream.",
        f"In a world full of programming, {username} chooses to script their own adventure.",
        f"{username}: Because sometimes the best commit is to real life.",
        f"Who needs GitHub when you’re busy contributing to life’s repository, right {username}?",
        f"{username} knows life’s best algorithms can’t be coded.",
        f"The only thing {username} pushes more than code is the boundaries of adventure.",
        f"{username} is living proof that the best code is written off-screen.",
        f"While we compile code, {username} compiles experiences.",
        f"In the repository of life, {username}’s the star contributor.",
        f"{username} must have an amazing social life!",
        f"It's great that {username} value real human connections over screen time.",
        f"{username}'re probably the person who actually goes outside and enjoys the sun.",
        f"{username}'s life is too exciting to just stare at code all day.",
        f"{username} must have interesting hobbies beyond the realm of 0s and 1s.",
        f"It’s cool to see someone who’s not a slave to the machine.",
        f"{username}'re too busy making real-life memories!",
        f"{username} know there's more to life than just staring at a computer screen.",
        f"{username}'s eyes must be so well-rested without all that screen glare.",
        f"{username}’re living proof there’s a world beyond the keyboard.",
        f"{username} probably have amazing stories that don’t start with 'So I was coding...'",
        f"It's refreshing to meet someone who doesn't speak in code.",
        f"{username}'s ability to disconnect is admirable.",
        f"{username}'re the kind of person who makes tech-free zones cool.",
        f"It's awesome {username}'re not chained to the digital world.",
        f"{username} understand life is about experiences away from the console.",
        f"{username} must have a rich life full of diverse experiences!",
        f"{username}'re like a rare gem in today's digital-dominated world.",
        f"{username} bring balance to the force... and to screen time.",
        f"{username} prove there's more to life than just pushing commits.",
        f"{username}'s digital detox is an inspiration.",
        f"{username}'ve probably mastered the art of work-life balance.",
        f"{username} must have a lot of interesting stories to tell that don’t involve debugging.",
        f"{username} know that the best memories are made offline.",
        f"{username}’re the person everyone wants at a dinner party – no tech talk!",
        f"{username}'s presence is probably more real-world than virtual – how refreshing!",
        f"{username}’re too busy being a main character in real life.",
        f"{username} remind us there's a whole world outside GitHub's walls.",
        f"{username}'re living proof that not all heroes wear capes; some just log off.",
        "Did you forget your GitHub password, or are you just coding incognito?",
        "Rumor has it you once saw the inside of a GitHub repo!",
        "I heard you and GitHub are in an 'it's complicated' relationship."
    ]


    if score >= 87:
        return random.choice(high_score_roasts)
    elif score >= 73:
        return random.choice(medium_score_roasts)
    else:
        return random.choice(low_score_compliments)


#TEST_USERNAME = "PatrickZhao0"
#TEST_USERNAME = "BREADLuVER"
#TEST_USERNAME = "Spectraorder"
u_names = ["PatrickZhao0", "BREADLuVER", "Spectraorder", "ni2050", "Yucheng-XPH", "RichardFuuu", "AlexXiang604", "YimengDuan2002",
            "DarrenLe20", "hillarydavis1", "paulasera", "Leo6016", "shl622", "sarah-altowaity1", "rachel0lehcar", "danilo-montes"]
#u_names = ["PatrickZhao0", "BREADLuVER", "Spectraorder", "ni2050"]


for n in u_names:
    print(n)
    user_details = get_github_user_details(n, GITHUB_TOKEN)
    ratings = calculate_rating(user_details)
    feed_back = get_feedback(n, ratings)
    print(f"GitHub User Rating: {ratings}")
    print(feed_back)
    print("")
