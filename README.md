# Final Project

## Badges


A web app to post/blog that is targeted to developers and is tied to GitHub. Users can share to their friends any news, updates, or projects they're working on. The web-app also provides useful stats regarding users' GitHub activity, and generates personalized jokes for users based on their GitHub account.

##This is the Figma link for the project Blog App
https://www.figma.com/file/WoGAi1nOVTMWqwCrJaPn3y/Blog-APP?type=design&mode=design&t=2vILJdjZo6fXMX77-1





## Instructions

## Set-up Instructions

### Step 1, Clone the directory:
```
git clone https://github.com/software-students-fall2023/5-final-project-charsiubun.git
```
### Step 2, Docker Compose:
```
docker-compose up --build
```
### Step 3, Access the web-app
Now, you can access http://localhost:5000/
### Docker Hub
Alternatively, You can also pull the images from the docker hub
```
docker pull ***Link here***
```
Download the docker-compose file from here and run 

```
docker-compose up
```


## User-guide

### Logging In
- When starting, you will be prompted to login/create an account

### Main Screen
- The main screen serves as the dashboard and starting point.
- You will be able to see your profile name, along with the "Joke of the Day", which is done by a joke generator, and is based of your user profile
- From here, you can navigate to 3 different functionalities: Your Blog, Friends' Blogs, Checking your GitHub "rating".

### Publishing a Blogpost
- Navigate to the “Add Notes” section from the main menu.
- You can capture an image using your device's camera, which will be interpreted by our ML function.
- You will then be redirected to a new page where the interpreted note title and body will be shown.
- Click add note if they're satisfactory. If successful, a success message will show.
- The extracted notes will be stored and can be accessed in all notes, search note.

### All Notes
- Access all your saved notes through the “View Notes” section.
- Each note can be edited or deleted.

### Search Notes (case sensitive)
- Use the search functionality to quickly find specific notes.
- Enter part of the note's title or the full title in the search bar to filter out notes.
- Case sensitive

## Team Members

Nicolas Izurieta: https://github.com/ni2050

Patrick Zhao: https://github.com/PatrickZhao0

Brad Yin: https://github.com/BREADLuVER

Yucheng Xu: https://github.com/Yucheng-XPH