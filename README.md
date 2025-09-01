# Champz
## Overview
This project is a FIFA tournament organizer. Users can create a tournament with any number of participants (minimum of 4), and each participant builds their own team through an auction-style process. Each participant is given a budget (default: 250), and the auction proceeds by iterating through FIFA player positions. Participants can bid on and purchase the best players in the game to assemble their teams.

<img width="1641" height="908" alt="image" src="https://github.com/user-attachments/assets/7b561ae1-b09c-4e46-af89-af1567444069" />

After the teams are built, the project generates a group stage where every participant plays against each other. Once all matches are completed, the top four players advance to the semifinals: first place faces fourth, and second faces third. The winners of the semifinals then compete in the final to determine the tournament champion.

<img width="1755" height="922" alt="image" src="https://github.com/user-attachments/assets/0196c0ea-ee93-4e63-aeb8-d9f13fd8dd7e" />

## Setup
To populate your database with players and all the images used in this project, make sure to run the [Fifa-Players-Scrapping](https://github.com/caiomelo22/Fifa-Players-Scrapping) project first. To define the image directory as a volume in this project, copy the `IMAGE_DIR_PATH` environment variable from the scrapping project's .env file and paste it into a .env file at the root of this repository:
```
IMAGE_DIR_PATH=C:\default_path
```
You'll also need to define two more .env files for the backend and frontend, but those are explained in detail inside their respective folders.
Once everything is set up, just run the following command from the root directory and enjoy:
```
>> docker-compose up
```

## Final Considerations
This project started as a simple console application I built back in early 2019 for a CS class at university. After the semester ended, I kept improving it and using it to run FIFA tournaments with my friends.

In 2022, after gaining a few years of coding experience, I decided to refactor most of the project—since, well, the code was kind of a mess. This is my first big project published here, so apologies in advance if the documentation isn't perfect.

Even though I mainly use C# these days, working on this project in Django was a really fun challenge.

EDIT (2023): A year later, I refactored the backend again—this time using FastAPI. I think it’s much cleaner now. Also, fun fact: Python has become my main language lately. 😄
