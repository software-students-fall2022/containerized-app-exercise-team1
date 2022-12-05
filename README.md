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
    * Displays the results and the moves of each rock paper scissor game played on the ML client.
* DB
    * Stores the rounds of each game of rock paper scissor played on the ML client.

# Setting up the docker container for the web app and database

Download Docker Desktop.[link](https://www.docker.com/)

Inside the directory of the project
```
docker-compose up
```

## Running the ML Client

* cd to machine-learning-client
    ```
    cd machine-learning-client
    ```
* Run the project
    ```
    python -m hand_gesture_rock_paper_scissor
    ```

# Shortcut Links

* How to run the programs locally:
    * machine-learning-client: Look at [README.md](./machine-learning-client) file.
    * web-app: Look at [README.md](./web-app) file.
* To get coverage information:
    * Look at [README.md](./machine-learning-client/tests) file for steps to get machine-learning-client coverage.
    * Look at [README.md](./web-app/tests) file for steps to get web-app coverage.

