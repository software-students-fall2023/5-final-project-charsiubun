# Final Project

## Badges
![Python build & test](https://github.com/software-students-fall2023/5-final-project-charsiubun/actions/workflows/webapp.yml/badge.svg) 


A web app to post/blog that is targeted to developers and is tied to GitHub. Users can share to their friends any news, updates, or projects they're working on. The web-app also provides useful stats regarding users' GitHub activity, and generates personalized jokes for users based on their GitHub account.

## Figma Link
https://www.figma.com/file/WoGAi1nOVTMWqwCrJaPn3y/Blog-APP?type=design&mode=design&t=2vILJdjZo6fXMX77-1





## Instructions

## Set-up Instructions

### Step 1, Clone the directory:
```
git clone https://github.com/software-students-fall2023/5-final-project-charsiubun.git
```
### Step 2, set up .env, get token from us
### Step 3, Docker Compose:
```
docker-compose build
```
```
docker-compose up
```
### Step 4, Access the web-app
Now, you can access the web app via http://localhost:5001/
## Docker Hub
https://hub.docker.com/r/bailongzhao/github_blog/tags

## Digital Ocean
http://104.236.198.88:5001/

## User-guide (Use Digital Ocean's Link)

### Logging In
- When starting, you will be prompted to login/register an account.
- If you don't have an account, click on register, which will take you to a new screen to set up your username and password.
- **Please Note** that your username **MUST** be the same as your GitHub account username
- Please note it may take a while to process this request, so be patient.
- Note your password will be hashed and safely stored in a database.

### Main Screen
- The main screen serves as the dashboard and starting point.
- You will be able to see your profile name, along with the "Joke of the Day", which is done by a joke generator, and is based of your user profile.
- From here, you can navigate to 5 different functionalities: Your Blog, Friends' Blogs, All Blogs Checking your GitHub "rating", and adding a friend.

### Viewing Your Blogpsts
- Navigate to the “Your Blog” section from the main menu.
- Everyone of your brilliant posts will be organized for you to go over!

### Publishing a Blogpost
- Navigate to the “Your Blog” section from the main menu.
- You will then be redirected to a new page where all of your publishd blogposts will show up.
- Click add blogpost, and you will be prompted to enter a new blog entry.
- The new blogpost will be published and will be viewable to all your friends!

### Deleting a Blogpost
- Navigate to the “Your Blog” section from the main menu.
- You will then be redirected to a new page where all of your publishd blogposts will show up.
- Click on the desired blogpost, and then delete.
- Deleting will automatically remove the blogpost permanently.

### Adding Friends
- Click on the "+" in the upper right corner of the home page.
- You will be prompted to enter a user you want to add as a friend.
- Feel free to add us as friends. Add PatrickZhao0, BREADLuVER, and Yucheng-XPH if you want to see some of the first posts ever!

### Viewing Friends' Blogposts
- Navigate to the "Friends' Blogs" section from the main menu.
- You will be redirected to a new page that shows all your friends' insightful blogposts.

### Viewing all Blogposts
- Navigate to the "All Blogs" section from the main menu
- All notifications regarding friends joining, yours as well as their blogs will all show up here. Blogs from users that are not added as your friend are also found here.

### Checking GitHub User Ratings
- Navigate to "Find out Github Users" from the homepage.
- You will be prompted to enter a GitHub username.
- The app will fetch data from that GitHub user, analyze it and rate it based on yearly contributions, number of repositories, among other criteria, and then generate a joke based on the information it gathers.




## Team Members

Nicolas Izurieta: https://github.com/ni2050

Patrick Zhao: https://github.com/PatrickZhao0

Brad Yin: https://github.com/BREADLuVER

Yucheng Xu: https://github.com/Yucheng-XPH
