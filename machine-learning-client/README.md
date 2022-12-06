Code related to the machine learning client goes in this folder.

# Source of ML Program

The machine learning program was downloaded from this link and then modified: https://techvidvan.com/tutorials/hand-gesture-recognition-tensorflow-opencv/

# Set up the virtual environment

* cd to the current directory
    ```
    cd machine-learning-client
    ```

* Create python virtual environment
    ```
    python -m venv .venv
    ```

* Activate virtual environment on bash
    * On Windows
    ```
    source .venv/Scripts/activate
    ```
    * On Mac
    ```
    source .venv/bin/activate
    ```

* Download dependencies
    ```
    pip install -r requirements.txt
    ```

# Run machine-learning-client project locally

* Make sure that you are at the current directory
    ```
    cd machine-learning-client
    ```

* Make sure that virtual environment is activated
    * On Windows
    ```
    source .venv/Scripts/activate
    ```
    * On Mac
    ```
    source .venv/bin/activate
    ```

* Run the project
    ```
    python -m hand_gesture_rock_paper_scissor
    ```

# How to handle these errors

* AttributeError: '_UserObject' object has no attribute 'predict'
    * Try to re-download the files: https://techvidvan.s3.amazonaws.com/machine-learning-projects/hand-gesture-recognition-code.zip
    * Delete the current mp_hand_gesture directory in the repository and replace it with a copy of the mp_hand_gesture in the zip file
    * Delete the data.pickle file and replace it with a copy of the data.pickle in the zip file.
    * Note: This error may or may not be resolved completely.
    
