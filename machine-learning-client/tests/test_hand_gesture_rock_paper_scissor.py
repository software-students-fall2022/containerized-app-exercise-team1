import pytest
import hand_gesture_rock_paper_scissor as mlgame
import cv2

class TestGameFunctions:

    def test_sanity(self):
        assert True == True, "Sanity check failed"
    def test_sanity_call(self):
        assert mlgame.StaticVariables.BLACK == (0,0,0), "Expected correct call to variable"
    def test_display_img(self):
        frame = cv2.flip(cv2.imread('mock_img/rock.jpg'), 1)
        mlgame.show_frame(frame)

class TestFrameFunctions:
    pass