# TechVidvan hand Gesture Recognizer

# import necessary packages

import cv2
import numpy as np
import math
import mediapipe as mp
import tensorflow as tf
import tensorflow_hub as hub
import time
import pymongo
import gridfs
from bson.objectid import ObjectId

# initialize mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Load the gesture recognizer model
# model = tf.keras.models.load_model('mp_hand_gesture')
model = tf.keras.Sequential([
    hub.KerasLayer('mp_hand_gesture')
])
model.build((None, 21, 2))

# Load class names
f = open('gesture.names', 'r')
classNames = f.read().split('\n')
f.close()
print(classNames)


cxn = pymongo.MongoClient("mongodb://127.0.0.1:27017")
try:
    # verify the connection works by pinging the database
    cxn.admin.command('ping') # The ping command is cheap and does not require auth.
    db = cxn['ml_client'] # store a reference to the database
    print(' *', 'Connected to MongoDB!') # if we get here, the connection worked!

except Exception as e:
    # the ping command failed, so the connection is not available.
    # render_template('error.html', error=e) # render the edit template
    print('Database connection error:', e) # debug



class StaticVariables:
    '''
    Variables that should not be modified throughout lifetime of the game.
    '''

    props = ['rock', 'paper', 'scissor']
    '''
    The props for the game. Contains list of 3 elements: 'rock', 'paper', 'scissor'.
    '''

    user_win_conditions = {'rock': 'scissor', 'paper': 'rock', 'scissor': 'paper'}
    '''
    The key of the dictionary is what the user plays. 
    The value is what the computer needs to play for the user to win.
    '''

    BLACK = (0, 0, 0)
    RED = (0, 0, 255)
    BLUE = (255, 0, 0)
    GREEN = (0, 255, 0)
    ORANGE = (0, 165, 255)

    # note: if you are confused about what this does, just open python and test it out.
    position = [(10, int(text_height*y)) for y, text_height in enumerate([40]*7)]
    '''
    Gives out the position coordinates for where to place the text on the frames.

    Indices from 1 to 6 all work out for the placement of text on the frames.
    '''

    font_size_scale = 1
    '''
    This is the font size scale for the text.
    '''
    font_thickness = 2
    '''
    This is the thickness of the text.
    '''



def predict_gesture(frame):
    '''
    This is the ml prediction of the gesture based on the frame. 
    Source: https://techvidvan.com/tutorials/hand-gesture-recognition-tensorflow-opencv/
    '''

    # print("starting prediction of gesture")
    
    x, y, c = frame.shape

    # print(x, y, c)

    # Flip the frame vertically
    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # print("processing result for prediction")

    # Get hand landmark prediction
    result = hands.process(framergb)

    # print(result)
    
    className = ''

    # print("drawing on frame")
    
    # post process the result
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                # print(id, lm)
                lmx = int(lm.x * x)
                lmy = int(lm.y * y)

                landmarks.append([lmx, lmy])

            # print("Completed one lm")

            # Drawing landmarks on frames
            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

            # print("Finding prediction for model")
            
            # Predict gesture
            prediction = model.predict([landmarks])
            # print(prediction)
            classID = np.argmax(prediction)
            className = classNames[classID]
    return (className, frame)

def display_content(frame, text: str, location: tuple, color: tuple):
    '''
    Render a text onto the frame at the specific location with a specific color and display it to the user.

    frame is the frame to display to the user.

    text is the string to render onto the frame.

    location is a tuple with 2 elements, representing the x and y coordinates.
    
    color is a tuple with 3 elements, representing Blue, Green, Red in that order.
    '''

    # put the text at the location with the specified color formatted as bgr.
    cv2.putText(frame, str(text), location, cv2.FONT_HERSHEY_SIMPLEX, 
            StaticVariables.font_size_scale, color, StaticVariables.font_thickness, cv2.LINE_AA)
    # show the frame with the time
    show_frame(frame)

def computer_plays() -> str:
    '''
    Determine what the computer plays.

    Returns either a 'rock', 'paper', or 'scissor'.
    '''
    cp_play = StaticVariables.props[math.floor(np.random.random()*3)]
    return cp_play

def handle_play(user_play, cp_play):
    '''
    user_play is either 'rock', 'paper', 'scissor', or ''.

    cp_play is either 'rock', 'paper', or 'scissor'.

    Returns 'user' for user victory. Returns 'cp' for computer victory. Returns 'tie' for a tie.
    Anything else means that a tie or invalid input was detected.
    '''

    #If user did not play a valid prop value, then return None
    if not user_play in StaticVariables.props:
        return None
    
    # if user played the same prop as the computer, we have a tie
    if user_play == cp_play:
        return 'tie'
    # check condition for user victory
    elif StaticVariables.user_win_conditions[user_play] == cp_play:
        return 'user'
    # otherwise, the computer wins.
    else:
        return 'cp'

def show_frame(frame):
    '''
    Display the current frame to the user.
    '''

    cv2.imshow("Output", frame)
    if cv2.waitKey(1) == ord('q'):
        raise Exception("Exiting")

def establish_web_cam_connection():
    '''
    Attempts to establish web cam connection for a number of times.
    '''

    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    print("Cap:", cap)
    for i in range(10):
        print("Trying to establish connection. Trial", i)
        if not cap.read()[0]:
            time.sleep(2)
            cap = cv2.VideoCapture(0)
        else:
            return cap
    raise WebCamConnection("Cannot connect to camera.")

def end_program(cap):
    '''
    Performs action before exiting the program. Releases resources that program is using.
    '''

    # release the webcam and destroy all active windows
    cap.release()
    cv2.destroyAllWindows()
    print("Completed Exit steps")

def final_result_text(user_victory, cp_victory):
    '''
    Processes the number of victories and returns a tuple of what to display to the user.
    The first element of the tuple is the string to display to the user.
    The second element of the tuple is the color that the text to display should be.
    '''

    if user_victory > cp_victory:
        display_text = "You have Won!!!"
        color = StaticVariables.GREEN
    elif user_victory == cp_victory:
        display_text = "It is a tie"
        color = StaticVariables.ORANGE
    else:
        display_text = "The computer has won"
        color = StaticVariables.RED
    display_text += " " + str(user_victory) + ' : ' + str(cp_victory)
    return (display_text, color)

def storeGame():
    game_id = db.games.insert_one({"rounds": []}).inserted_id
    return game_id


def storeRound(game_id,round, user_score, user_gesture, cp_score, cp_gesture,frame):
    round_id = db.rounds.insert_one({"round":round,"user_score":user_score,"user_gesture":user_gesture,"cp_score":cp_score,"cp_gesture":cp_gesture}).inserted_id
    #storing image
    file = "./images/" + str(round_id) + ".jpg"
    cv2.imwrite(file,frame)
    fs = gridfs.GridFS(db)
    with open(file, 'rb') as f:
        contents = f.read()
    fs.put(contents,filename=(str(round_id) + ".jpg"))#image is now in ml_client db fs.files
    #can search for these images by 'round id + .jpg'
    
    game = db.games.find_one({"_id":ObjectId(game_id)})
    rounds_arr = game["rounds"]
    rounds_arr.append(round_id)
    filter = {"_id":ObjectId(game_id)}
    new_values = {"$set": {"rounds":rounds_arr}}
    db.games.update_one(filter,new_values)
    
        
def main(seconds_per_round, num_of_rounds):
    print("Game is starting...")
    # number of computer victories
    cp_victory = 0 
    # number of user victories
    user_victory = 0
    # number of ties
    tie_victory = 0
    #keep track of id for game 
    game_id = None
    #keep_track of round #
    curr_round = 0
    try:
        # start off with a new round
        new_round = True
        # try establishing web cam connection
        cap = establish_web_cam_connection()
        # while we have not completed numOfRounds
        while num_of_rounds:
            if new_round:
                new_round = False
                oldTime = time.time()
                curTime = time.time()
            else:
                curTime = time.time()

            display_text = int(seconds_per_round + oldTime - curTime) + 1

            # Read each frame from the webcam
            _, frame = cap.read()
            # print("This is cap read:", cap.read())

            # get the predicted gesture along with the modified frame.
            gesture, frame = predict_gesture(frame)

            # display the gesture of the user.
            display_content(frame, gesture, StaticVariables.position[1], StaticVariables.BLACK)

            # display the time left for the user to play
            display_content(frame, display_text, StaticVariables.position[2], StaticVariables.RED)

            # if the time is up
            if display_text <= 0:
                # let the computer make its move
                cp_play = computer_plays()

                # tell the user what the computer played
                display_text = "Computer Plays " + cp_play
                display_content(frame, display_text, StaticVariables.position[3], StaticVariables.BLACK)

                # get the current time
                curTime = time.time()

                # get result of who has won the current round
                result = handle_play(gesture, cp_play)
                
                # sleep for the leftover time
                time.sleep(2 + curTime - time.time())

                # render the results based on the status
                if result == 'user':
                    display_content(frame, "You Win!!!", StaticVariables.position[4], StaticVariables.GREEN)
                    # decrement the number of rounds left
                    num_of_rounds -= 1
                    user_victory += 1
                elif result == 'cp':
                    display_content(frame, "You Lose", StaticVariables.position[4], StaticVariables.RED)
                    # decrement the number of rounds left
                    num_of_rounds -= 1
                    cp_victory += 1
                elif result == 'tie':
                    display_content(frame, "Tie! Try again!", StaticVariables.position[4], StaticVariables.ORANGE)
                else:
                    display_content(frame, "Try again!", StaticVariables.position[4], StaticVariables.ORANGE)
                # we are ready for a new round
                new_round = True
                # give the user 3 seconds to see the results
                time.sleep(3)
                if result == 'cp' or result == "user":
                    curr_round += 1
                    if curr_round == 1:
                        game_id = storeGame()
                    storeRound(game_id,curr_round,user_victory, gesture, cp_victory,cp_play,frame)
    except WebCamConnection as e:
        print(e)
    except Exception as e:
        print(e)
        end_program(cap)
    else:
        # at successful completion, display frame with all results
        display_text, color = final_result_text(user_victory, cp_victory)
        display_content(frame, display_text, StaticVariables.position[5], color)

        display_text = "Press any key to quit"
        display_content(frame, display_text, StaticVariables.position[6], StaticVariables.BLACK)
        cv2.waitKey(0)
        end_program(cap)

class WebCamConnection(Exception):
    pass

if __name__ == '__main__':
    main(5, 5)