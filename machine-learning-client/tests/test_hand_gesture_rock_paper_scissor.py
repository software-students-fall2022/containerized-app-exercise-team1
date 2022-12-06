import pytest
import hand_gesture_rock_paper_scissor as mlgame
import cv2
import numpy as np

# Benji's edits
# import pymongo
import mongomock

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
            assert mlgame.computer_plays() in props, "Expected computer to play one of the props for any round (rock, paper, scissor)."

    def test_establish_web_cam_connection(self):
        with pytest.raises(mlgame.WebCamConnection):
            cap = mlgame.establish_web_cam_connection()
            assert cap.read()[0] == True, "Expected web cam to be functional"
            raise mlgame.WebCamConnection("Test Passes")
        
    def test_handle_play(self):
        user_play = ['rock', 'paper', 'scissor']
        cp_play = ['rock', 'paper', 'scissor']
        for u, c in zip(user_play, cp_play):
            assert mlgame.handle_play(u, c) == 'tie', f"Expected tie to happen for user playing {u} and computer playing {c}."
        cp_play = ['paper', 'scissor', 'rock']
        for u, c in zip(user_play, cp_play):
            assert mlgame.handle_play(u, c) == 'cp', f"Expected computer to win for user playing {u} and computer playing {c}."
        cp_play = ['scissor', 'rock', 'paper']
        for u, c in zip(user_play, cp_play):
            assert mlgame.handle_play(u, c) == 'user', f"Expected user to win for user playing {u} and computer playing {c}."
        user_play = ['', 'random-stuff', 'str']
        for u, c in zip(user_play, cp_play):
            assert not mlgame.handle_play in ['tie', 'cp', 'user'], f"Expected invalid user input to result in other values"

    def test_final_result_text(self):
        user_victories = [0, 1, 2, 3, 4, 5]
        cp_victories = [5, 4, 3, 2, 1]
        win_starting = "You have Won!!!"
        lose_starting = "The computer has won"
        for u, c in zip(user_victories, cp_victories):
            if u > c:
                assert mlgame.final_result_text(u, c)[0].startswith(win_starting), "Expected the text display to express that the user has won."
            elif u < c:
                assert mlgame.final_result_text(u, c)[0].startswith(lose_starting), "Expected the text display to express that the computer won"
            else:
                assert False, "The game should not tie"

    def test_correct_props(self):
        expected = ['rock', 'paper', 'scissor']
        actual = mlgame.StaticVariables.props
        assert len(expected) == len(actual), "Expected the number of props to be equal"
        for e, a in zip(sorted(expected), sorted(actual)):
            assert e == a, "Expected all props to exist"
    
    def test_correct_position(self):
        expected_separation = 40
        positions = mlgame.StaticVariables.position
        for i, p in enumerate(positions):
            assert i*expected_separation == p[1], f"Expected {expected_separation} pixels of distance between the text positions"

    def test_end_program(self):
        frame = cv2.imread('./tests/mock_img/rock.jpg')
        assert type(frame) == np.ndarray, "Expected frame to be successfully fetched"
        
        mlgame.show_frame(frame)
        assert cv2.getWindowProperty("Output", cv2.WND_PROP_VISIBLE) > 0.5, "The Output frame should exist"
        mlgame.end_program(MockCamConnection())
        assert cv2.getWindowProperty("Output", cv2.WND_PROP_VISIBLE) < 0.5, "The Output frame should no longer exist"

    def test_show_frame(self):
        frame = cv2.imread('./tests/mock_img/rock.jpg')
        assert type(frame) == np.ndarray, "Expected frame to be successfully fetched"
        
        assert cv2.getWindowProperty("Output", cv2.WND_PROP_VISIBLE) < 0.5, "The Output frame should not exist yet"
        mlgame.show_frame(frame)
        cv2.getWindowProperty("Output", cv2.WND_PROP_VISIBLE) > 0.5, "The Output frame should exist now"

# -----------------------------------------------------------------------------------------
# Benji's edits
    @pytest.mark.parametrize("round, user_score, user_gesture, cp_score, cp_gesture, result", [
        (1, 0, 'rock', 0, 'paper', 'cp'),
        (2, 0, 'paper', 1, 'paper', 'tie'),
        (3, 0, 'scissor', 1, 'paper', 'user'),
    ])

    def test_storeRound(self, round, user_score, user_gesture, cp_score, cp_gesture, result) :
        # # Establish the connection to the database
        # cxn = pymongo.MongoClient("mongodb://127.0.0.1:27017")
        # db = cxn['ml_client']

        db = mongomock.MongoClient().db.collection
        
        # Run storeRound() and check if the collection's actual rounds are the expected rounds.
        game_id = mlgame.storeGame(db)
        mlgame.storeRound(game_id, round, user_score, user_gesture, cp_score, cp_gesture, result, db)

        # Access the rounds collection and initialize the round that should be stored in the rounds collection.
        roundsCollection = db["rounds"]
        # expectedRound = {"round":round,"user_score":user_score,"user_gesture":user_gesture,"cp_score":cp_score,"cp_gesture":cp_gesture,"result":result}
        
        numRounds = roundsCollection.count_documents({})
        rndTracker = 1
        for rnd in roundsCollection.find():
            if rndTracker == numRounds:
                assert rnd["round"] is round
                assert rnd["user_score"] is user_score
                assert rnd["user_gesture"] == user_gesture
                assert rnd["cp_score"] is cp_score
                assert rnd["cp_gesture"] == cp_gesture
                assert rnd["result"] == result
            rndTracker += 1

    @pytest.mark.parametrize("round, user_score, user_gesture, cp_score, cp_gesture, result", [
        (1, 0, 'rock', 0, 'paper', 'cp'),
        (2, 0, 'paper', 1, 'paper', 'tie'),
        (3, 0, 'scissor', 1, 'paper', 'user'),
    ])

    def test_storeAllRounds(self, round, user_score, user_gesture, cp_score, cp_gesture, result) :
            # # Establish the connection to the database
            # cxn = pymongo.MongoClient("mongodb://127.0.0.1:27017")
            # db = cxn['ml_client']

            db = mongomock.MongoClient().db.collection
            
            # Run storeAllRounds() and check if the collection's actual rounds are the expected rounds.
            game_id = mlgame.storeGame(db)
            mlgame.storeAllRounds(game_id, round, user_score, user_gesture, cp_score, cp_gesture, result, db)

            # Access the allRounds collection and initialize the round that should be stored in the collection.
            allRoundsCollection = db["allRrounds"]

            numRounds = allRoundsCollection.count_documents({})
            rndTracker = 1
            for rnd in allRoundsCollection.find():
                if rndTracker == numRounds:
                    assert rnd["round"] is round
                    assert rnd["user_score"] is user_score
                    assert rnd["user_gesture"] == user_gesture
                    assert rnd["cp_score"] is cp_score
                    assert rnd["cp_gesture"] == cp_gesture
                    assert rnd["result"] == result
                rndTracker += 1

    @pytest.mark.parametrize("move, counterMove", [
        ('rock', 'paper'),
        ('scissor', 'rock'),
        ('paper', 'scissor'),
        (None, None)
    ])
    
    def test_counterMove(self, move, counterMove) :
        assert mlgame.counterMove(move) == counterMove
        

class MockCamConnection:
    def __init__(self):
        pass
    def release(self):
        pass