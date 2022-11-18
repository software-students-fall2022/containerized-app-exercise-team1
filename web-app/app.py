from flask import Flask
from pymongo import MongoClient
import os


# connect to the database
cxn = MongoClient('localhost', 27017)
try:
    # verify the connection works by pinging the database
    cxn.admin.command('ping') # The ping command is cheap and does not require auth.
    db = cxn['sample_airbnb'] # store a reference to the database
    print(' *', 'Connected to MongoDB!') # if we get here, the connection worked!

except Exception as e:
    # the ping command failed, so the connection is not available.
    # render_template('error.html', error=e) # render the edit template
    print(' *', "Failed to connect to MongoDB at", 'mongodb+srv://RobertChen:adOuu8E6S9G7Cwbo@cluster0.2swudzk.mongodb.net/?retryWrites=true&w=majority')
    print('Database connection error:', e) # debug


app = Flask(__name__)

@app.route('/')
def home():
    return 'test123'


if __name__ == "__main__":
    app.run(debug=True)