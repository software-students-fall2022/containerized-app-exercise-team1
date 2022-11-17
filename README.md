[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=9334070&assignment_repo_type=AssignmentRepo)
# Containerized App Exercise

Build a containerized app that uses machine learning. See [instructions](./instructions.md) for details.

# Teammates

* Jonason Wu (jw5911): [Github Profile](https://github.com/JonasonWu)

# Set up the virtual environment

* Create python virtual environment
    ```
    python -m venv .venv
    ```
* Activate virtual environment on bash
    ```
    source .venv/Scripts/activate
    ```
* Install dependencies
    ```
    pip install opencv-python
    pip install mediapipe
    pip install tensorflow
    ```

# Run machine-learning-client project locally

* Make sure that virtual environment is activated
    ```
    source .venv/Scripts/activate
    ```
* cd to the correct folder (assuming you are currently at this directory)
    ```
    cd machine-learning-client
    ```
* Run the project
    ```
    python -m TechVidvan-hand_gesture_detection.py
    ```
