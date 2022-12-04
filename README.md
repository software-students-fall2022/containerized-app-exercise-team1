![machine learning workflow](https://github.com/software-students-fall2022/containerized-app-exercise-team1/actions/workflows/machine-learning-tests.yml/badge.svg)

![web app workflow](https://github.com/software-students-fall2022/containerized-app-exercise-team1/actions/workflows/web-app-tests.yml/badge.svg)

# Containerized App Exercise

Build a containerized app that uses machine learning. See [instructions](./instructions.md) for details.

# Teammates

* Jonason Wu (jw5911): [Github Profile](https://github.com/JonasonWu)
* Brian Lin (bl2814): [Github Profile](https://github.com/blin007)
* Robert Chen (yc3363): [Github Profile](https://github.com/RobertChenYF)
* Alejandro Olazabal (ajo351): [Github Profile](https://github.com/aleolazabal)
* Mark Chen (xc2097): [Github Profile](https://github.com/markizenlee)
* Benji Luo (hjl464): [Github Profile](https://github.com/BenjiLuo) 

# Product Vision Statement

* ML client
    * Allow users to use the camera to play a game of rock paper scissors with the computer.
* Web App
    * Displays the results and the moves of each rock paper scissor game played on the ML client as well as some analytics.
* DB
    * Stores the rounds of each game of rock paper scissor played on the ML client.

# Run the app

Please start the web app and database before running the ML client.<br>

The ML client use packages not supported on **Apple silicon machine**, so our app does not work on Apple silicon Mac.

## Run the web app and database

Download Docker Desktop.[link](https://www.docker.com/)

Inside the directory of the project
```
docker-compose up
```

## Run the ML Client

Look at [README.md](./machine-learning-client) file.

# Test the app locally
* Look at [README.md](./machine-learning-client/tests) file for steps to test the machine-learning-client.
* Look at [README.md](./web-app/tests) file for steps to test the web-app.

# Other Links
* How to run the web-app without docker:
    * Look at [README.md](./web-app) file.



