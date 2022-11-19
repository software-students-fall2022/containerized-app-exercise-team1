Code related to the machine learning client goes in this folder.

The machine learning program was downloaded from this link and then modified: https://techvidvan.com/tutorials/hand-gesture-recognition-tensorflow-opencv/

# Set up the virtual environment

* Create python virtual environment
    ```
    python -m venv .venv
    ```
* Activate virtual environment on bash
    ```
    source .venv/Scripts/activate
    ```
* Download dependencies
    ```
    pip install -r requirements.txt
    ```

# Run machine-learning-client project locally

* Make sure that virtual environment is activated
    ```
    source .venv/Scripts/activate
    ```
* cd to this directory
    ```
    cd machine-learning-client
    ```
* Run the project
    ```
    python -m hand_gesture_rock_paper_scissor
    ```
