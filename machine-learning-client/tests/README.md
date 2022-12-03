# Prerequisite

* Make sure that you have completed the [README.md](../README.md) steps for setting up the virtual environment for the machine-learning-client.

# Get Code Coverage information

* cd to the machine-learning-client directory. Assuming you are currently at this directory, run the following:
    ```
    cd ../
    ```
* Run pytest with coverage
    ```
    pytest --cov
    ```

# Alternative way to get coverage information

* Go to GitHub Actions.
* Look at the most recent job and find a machine learning workflow. Click on it.
* Open the details of the job. It is under the "Jobs" section of the navigation bar.
* Click on "execute unit tests" section.
* You will then see the coverage details.
* Note: Looking at hand_gesture_rock_paper_scissor.py file, you should see that the coverage is over 50%.
