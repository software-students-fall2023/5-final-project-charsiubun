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
        f"{username} might be the only person to read GitHub docs for bedtime stories.",
        "You've got more commits than a book has words!",
        "Is your home address localhost?",
        "You're the human embodiment of 'It works on my machine.'",
        "Your keyboard must be applying for a restraining order any day now.",
        "I bet you dream in code, don’t you?",
        "Your GitHub is so active, it needs its own social life!",
        "You've got more branches than a tree in spring.",
        "I’d tell you to go outside, but you might just find a way to commit from there too.",
        "Your coffee machine is probably the only one that understands you best.",
        "You must mistake the sound of typing for applause.",
        "If GitHub stars were money, you'd be on Forbes.",
        "Do you wear sunglasses to protect from the brightness of your own screen?",
        "I guess your first word was 'commit', wasn’t it?",
        "You don't get bugs; you get 'unexpected features', right?",
        "If you were a movie, you'd be called 'Lord of the Commits: The Fellowship of the Code'.",
        "Your codebase is bigger than my future.",
        "Even your pet knows how to push to GitHub, huh?",
        "Is your favorite snack a byte?",
        "Your love for coding is the only thing not needing debugging.",
        "You might be the only person who read the entire terms and conditions before accepting."
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
        "So, you code occasionally? Like every leap year?",
        "Your GitHub graph has more breaks than a Kit-Kat bar.",
        "You must be a ninja; you leave no traces in your repositories.",
        "Are you playing hard to get with your code editor?",
        "You and GitHub sitting in a tree, C-O-M-M-I-T-T-I-N-G... occasionally.",
        "Is your IDE just a glorified notepad for you?",
        "You must be a part-time coder and a full-time '404 not found'.",
        "You're the 'I’ll fix this bug later' kind of person, aren't you?",
        "Your commit history is like a mysterious novel – updated rarely but interesting.",
        "You treat coding like a treadmill – great intentions but rarely used.",
        "I bet your favorite Git command is 'blame'.",
        "You're like a Monday morning coder – a slow start but gets there eventually.",
        "Is your coding philosophy 'Less is more'?",
        "Your code is like a shooting star – rare and surprising.",
        "You must be an artist; you leave so much whitespace.",
        "Looks like you maintain a healthy balance between the real world and the matrix.",
        "You’re not a coder; you’re a ‘coding enthusiast’.",
        "Are your repositories just for decoration?",
        "Your favorite part of coding must be the 'end'.",
        "You only code on days that end in 'y', but only if you feel like it."
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
        "You must have an amazing social life!",
        "It's great that you value real human connections over screen time.",
        "You're probably the person who actually goes outside and enjoys the sun.",
        "Your life is too exciting to just stare at code all day.",
        "You must have interesting hobbies beyond the realm of 0s and 1s.",
        "It’s cool to see someone who’s not a slave to the machine.",
        "You're too busy making real-life memories!",
        "You know there's more to life than just staring at a computer screen.",
        "Your eyes must be so well-rested without all that screen glare.",
        "You’re living proof there’s a world beyond the keyboard.",
        "You probably have amazing stories that don’t start with 'So I was coding...'",
        "It's refreshing to meet someone who doesn't speak in code.",
        "Your ability to disconnect is admirable.",
        "You're the kind of person who makes tech-free zones cool.",
        "It's awesome you're not chained to the digital world.",
        "You understand life is about experiences away from the console.",
        "You must have a rich life full of diverse experiences!",
        "You're like a rare gem in today's digital-dominated world.",
        "You bring balance to the force... and to screen time.",
        "You prove there's more to life than just pushing commits.",
        "Your digital detox is an inspiration.",
        "You've probably mastered the art of work-life balance.",
        "You must have a lot of interesting stories to tell that don’t involve debugging.",
        "You know that the best memories are made offline.",
        "You’re the person everyone wants at a dinner party – no tech talk!",
        "Your presence is probably more real-world than virtual – how refreshing!",
        "You’re too busy being a main character in real life.",
        "You remind us there's a whole world outside GitHub's walls.",
        "You're living proof that not all heroes wear capes; some just log off."
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