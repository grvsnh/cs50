from project import ttt_winner, ttt_ai_move, rps_result


def test_ttt_winner():
    board = ["X", "X", "X", " ", " ", " ", " ", " ", " "]
    assert ttt_winner(board, "X")
    assert not ttt_winner(board, "O")


def test_ttt_ai_blocks():
    board = ["X", "X", " ", " ", "O", " ", " ", " ", " "]
    assert ttt_ai_move(board) == 2


def test_rps_result():
    assert rps_result("Rock", "Scissors") == "You Win"
    assert rps_result("Rock", "Paper") == "You Lose"
    assert rps_result("Rock", "Rock") == "Draw"
