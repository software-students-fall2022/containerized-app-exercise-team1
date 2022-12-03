# Prerequisite

* Make sure that you have completed the [README.md](../README.md) steps for setting up the virtual environment.

# Get Code Coverage information

* cd to the web-app directory. Assuming you are currently at this directory, run the following:
    ```
    cd ../
    ```
* pip install the following packages:
    ```
    pip install pytest
    pip install pytest-flask
    pip install pytest-cov
    pip install mongomock
    ```
* Run pytest with coverage
    ```
    pytest --cov
    ```

# Alternative way to get coverage information

* Go to GitHub Actions.
* Look at the most recent job and find a web app workflow. Click on it.
* Open the details of the job. It is under the "Jobs" section of the navigation bar.
* Click on "execute unit tests" section.
* You will then see the coverage details.
