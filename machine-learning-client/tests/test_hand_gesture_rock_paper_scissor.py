import pytest
import hand_gesture_rock_paper_scissor as mlgame
import cv2
import numpy as np

class TestGameFunctions:

    def test_sanity(self):
        assert True == True, "Sanity check failed"
    def test_sanity_call(self):
        assert mlgame.StaticVariables.BLACK == (0,0,0), "Expected correct call to variable"

    def test_predict_gesture_rock(self):
        frame = cv2.imread('./tests/mock_img/rock.jpg')
        assert type(frame) == np.ndarray, "Expected frame to be successfully fetched"
        gesture, frame = mlgame.predict_gesture(frame)
        assert gesture == 'rock', "Expected gesture predicted to be rock"

    def test_predict_gesture_scissor(self):
        frame = cv2.imread('./tests/mock_img/scissor.jpg')
        assert type(frame) == np.ndarray, "Expected frame to be successfully fetched"
        gesture, frame = mlgame.predict_gesture(frame)
        assert gesture == 'scissor', "Expected gesture predicted to be scissor"
    
    def test_predict_gesture_paper(self):
        frame = cv2.imread('./tests/mock_img/paper.jpg')
        assert type(frame) == np.ndarray, "Expected frame to be successfully fetched"
        gesture, frame = mlgame.predict_gesture(frame)
        assert gesture == 'paper', "Expected gesture predicted to be paper"

    def test_computer_plays(self):
        props = ['rock', 'paper', 'scissor']
        for i in range(10):
            assert mlgame.computer_plays() in props, "Expected computer to play one of the props (rock, paper, scissor)."

    def test_establish_web_cam_connection(self):
        try:
            cap = mlgame.establish_web_cam_connection()
            assert cap != None, "Expected web cam to be fetched"
        except mlgame.WebCamConnection as e:
            assert True
        assert False, "Expected exception to be thrown since web cam cannot be successfully fetched."
        


class TestFrameFunctions:
    pass