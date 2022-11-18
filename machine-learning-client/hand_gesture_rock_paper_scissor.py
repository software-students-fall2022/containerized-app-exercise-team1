# TechVidvan hand Gesture Recognizer

# import necessary packages

import cv2
import numpy as np
import random
import math
import mediapipe as mp
import tensorflow as tf
import time
from tensorflow.keras.models import load_model

# initialize mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Load the gesture recognizer model
model = load_model('mp_hand_gesture')

# Load class names
f = open('gesture.names', 'r')
classNames = f.read().split('\n')
f.close()
print(classNames)

def predict_gesture(frame):
    x, y, c = frame.shape

    # Flip the frame vertically
    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Get hand landmark prediction
    result = hands.process(framergb)

    # print(result)
    
    className = ''

    # post process the result
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                # print(id, lm)
                lmx = int(lm.x * x)
                lmy = int(lm.y * y)

                landmarks.append([lmx, lmy])

            # Drawing landmarks on frames
            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

            # Predict gesture
            prediction = model.predict([landmarks])
            # print(prediction)
            classID = np.argmax(prediction)
            className = classNames[classID]
    return (className, frame)

def display_content(frame, text, location, color):
    # put the text at the location with the specified color formatted as bgr.
    cv2.putText(frame, str(text), location, cv2.FONT_HERSHEY_SIMPLEX, 
            1, color, 2, cv2.LINE_AA)
    # show the frame with the time
    show_frame(frame)

def computer_plays(frame):
    # this should be a static variable
    props = ['rock', 'paper', 'scissor']
    cp_play = props[math.floor(random.random()*3)]
    display_text = "Computer Plays " + cp_play
    display_content(frame, display_text, (10, 150), (255, 0, 0))
    return cp_play

def handle_play(user_play, cp_play):
    '''
    user_play is either 'rock', 'paper', 'scissor', or ''.

    cp_play is either 'rock', 'paper', or 'scissor'.

    Returns 'user' for user victory. Returns 'cp' for computer victory. Returns 'tie' for a tie.
    Anything else means that a tie or invalid input was detected.
    '''
    # TODO: Compute the results, process the mongo db stuff here, return

    user_wins = {'rock': 'scissor', 'paper': 'rock', 'scissor': 'paper'}
    if user_play == cp_play:
        return 'tie'
    elif user_play == '':
        return None
    elif user_wins.get(user_play, 'rock') == cp_play:
        return 'user'
    else:
        return 'cp'

def show_frame(frame):
    cv2.imshow("Output", frame)
    if cv2.waitKey(1) == ord('q'):
        raise Exception("Exiting")

def establish_web_cam_connection():
    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    print("Cap:", cap)
    for i in range(10):
        if not cap.read()[0]:
            time.sleep(2)
            cap = cv2.VideoCapture(0)
        else:
            break
    return cap

def end_program(cap):
    # release the webcam and destroy all active windows
    cap.release()
    cv2.destroyAllWindows()
    print("Completed Exit steps")

def main(seconds_per_round, num_of_rounds):
    print("Game is starting...")
    BLACK = (0, 0, 0)
    RED = (0, 0, 255)
    BLUE = (255, 0, 0)
    GREEN = (0, 255, 0)
    ORANGE = (0, 165, 255)
    # number of computer victories
    cp_victory = 0 
    # number of user victories
    user_victory = 0
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
            display_content(frame, gesture, (10, 50), BLACK)

            # display the time left for the user to play
            display_content(frame, display_text, (100, 100), RED)

            # if the time is up
            if display_text <= 0:
                # let the computer make its move
                cp_play = computer_plays(frame)

                # get the current time
                curTime = time.time()

                # process results, save details into the db, etc.
                result = handle_play(gesture, cp_play)
                
                # sleep for the leftover time
                time.sleep(4 + curTime - time.time())

                # render the results based on the status
                if result == 'user':
                    display_content(frame, "You Win!!!", (10, 200), GREEN)
                     # decrement the number of rounds left
                    num_of_rounds -= 1
                    user_victory += 1
                elif result == 'cp':
                    display_content(frame, "You Lose", (10, 200), RED)
                    # decrement the number of rounds left
                    num_of_rounds -= 1
                    cp_victory += 1
                elif result == 'tie':
                    display_content(frame, "Tie", (10, 200), ORANGE)
                else:
                    display_content(frame, "Try again", (10, 200), ORANGE)
                # we are ready for a new round
                new_round = True

                # give the user 3 seconds to see the results
                time.sleep(3)
    except WebCamConnection as e:
        print(e)
    except Exception as e:
        print(e)
        end_program(cap)
    else:
        # at successful completion, display frame with all results
        if user_victory > cp_victory:
            display_text = "You have Won!!!"
            color = GREEN
        elif user_victory == cp_victory:
            display_text = "It is a tie"
            color = ORANGE
        else:
            display_text = "The computer has won"
            color = RED
        display_text += " ("+ user_victory + ':' + cp_victory + ')'
        display_content(frame, display_text, (10, 250), color)
        display_text = "Press any key to quit"
        display_content(frame, display_text, (10, 300), BLACK)
        cv2.waitKey(0)
        end_program(cap)

class WebCamConnection(Exception):
    pass

if __name__ == '__main__':
    main(5, 5)