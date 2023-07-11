# Champz
## Overview
This project consists in a FIFA tournament organizer. In this project, the user can create a tournament with any number of participants (6 minimum), and each participant can build your own team with an auction type process. In this process, we set a budget for each participant (the default value is 250), and we iterate through the player positions in FIFA, allowing the participants to bid and buy the best players in the game to use in their teams. 

![3](https://user-images.githubusercontent.com/49076270/158083938-37c12b2a-0135-4bd9-9fb6-d4bab88037e7.PNG)

After the teams are built, the project generates a group stage where every participant faces each other. When all games are ended, the first two participants in the standing will move directly to the semifinals and the second to sixth participants will play the wildcard stage. In the wildcard stage, the third participant will face de sixth and the fourth will face the fifth. The winners will move to the semifinals and then the final.

![4](https://user-images.githubusercontent.com/49076270/158084604-2389694c-8f38-4c42-969b-e91868c14a29.PNG)

## Instructions
In order to run the project, you'll need to: 
- Create a virtual environment in the Back directory, in order to install the requirements described in the requirements.txt file; 
- Run the 'yarn install' command in the Front directory, in order to install the packages used in the frontend;
- Create a config.py file in the Back directory, specifying the information needed for the MySQL connection and the django secret key used in the settings.py file. The variable's names are: 'db_name', 'user', 'password', 'host', 'port' and 'django_secret_key'.
- Run the 'python manage.py makemigrations' and 'python manage.py migrate' commands with the virtual environment activated in order to configurate the database tables.
- Make a POST request to the following endpoint in the backend: '/api/update-players'. This request will scrape the fifacm website in order to fill the database with players, teams, leagues and nations. This part can be buggy sometimes due to the website.
- Have fun :)

## Final Considerations
I've developed this project in early 2019 for a CS class in university. After the semester ended, I kept improving the project and using it to play FIFA tournaments with my friends. In 2022, after I got a few years of experience in coding, I decided to refactor most of the project because the code was kind of messy. I apologize in advance for the documentation because this is my first big project published here. Despite refactoring most of it recently, my main programming language right now is C# and developing this project in Django has been a really cool challenge.
