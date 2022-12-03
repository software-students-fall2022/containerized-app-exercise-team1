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

