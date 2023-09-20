# Champz
## Overview
This project consists in a FIFA tournament organizer. In this project, the user can create a tournament with any number of participants (6 minimum), and each participant can build your own team with an auction type process. In this process, we set a budget for each participant (the default value is 250), and we iterate through the player positions in FIFA, allowing the participants to bid and buy the best players in the game to use in their teams. 

![image](https://github.com/caiomelo22/Champz/assets/49076270/333ef0d2-7ff5-4cbc-9cac-787c3eebecc2)

After the teams are built, the project generates a group stage where every participant faces each other. When all games are ended, there will be a semifinals stage where the first of the group is going to face the fourth, and the second will face the third. After that, there'll be a final between the two winners.

![image](https://github.com/caiomelo22/Champz/assets/49076270/83a041d5-ae32-4bcd-903e-5162df4bf4e2)

## Setup
To fill your database with the players and all of the images shown in this project, please run the the [Fifa-Players-Scrapping](https://github.com/caiomelo22/Fifa-Players-Scrapping) project. In order to define the images directory as a volume in this project, copy the `IMAGE_DIR_PATH` env variable defined in the scrapping project and paste it in a .env file in the root directory of this repository:
```
IMAGE_DIR_PATH=C:\default_path
```
There are two more .env files that you'll have to define for the backend and frontend, but I'll leave those detailed in each of their folders.

## Final Considerations
This project idea started as a console application that I've developed in early 2019 for a CS class in university. After the semester ended, I kept improving the project and using it to play FIFA tournaments with my friends. In 2022, after I got a few years of experience in coding, I decided to refactor most of the project because the code was kind of messy. I apologize in advance for the documentation because this is my first big project published here. Despite refactoring most of it recently, my main programming language right now is C# and developing this project in Django has been a really cool challenge.
EDIT (2023): After a year, I decided to refactor the backend to use the fastapi framework. I think its a lot cleaner now. Oh, and my main programming language right now is Python, btw :) .
