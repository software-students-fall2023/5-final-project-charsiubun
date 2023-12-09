import random

def get_feedback(username, score):
    high_score_roasts = [
        f"{username}'s GitHub is so dense, even black holes are taking notes.",
        f"If there was a 'commit-ment' award, {username} would be a lifetime achiever.",
        f"Hey {username}, ever thought of 'branching' out to a social life?",
        f"I guess for {username}, 'social network' means Git branches talking to each other.",
        f"{username} codes like they're trying to solve world hunger through pull requests.",
        f"Is 'Ctrl+C, Ctrl+V' {username}'s idea of a balanced diet?",
        f"Someone tell {username} that 'Merge Conflicts' isn't a new Netflix series.",
        f"Legend says {username} once exited Vim, and it's been a folklore since.",
        f"If code cleanliness was next to godliness, {username} would be a deity.",
        f"{username} might be the only person to read GitHub docs for bedtime stories."
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
        f"{username} treats their repositories like cacti – water them once a year and hope for the best."
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
        f"In the repository of life, {username}’s the star contributor."
    ]

    if score > 75:
        return random.choice(high_score_roasts)
    elif score > 40:
        return random.choice(medium_score_roasts)
    else:
        return random.choice(low_score_compliments)

# Example Usage
username = "Spectraorder"
score = 85  # Replace with the actual score
print(get_feedback(username, score))