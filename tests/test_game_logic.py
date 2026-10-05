from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    load_high_scores,
    parse_guess,
    save_high_score,
    update_score,
)

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


def test_range_easy():
    assert get_range_for_difficulty("Easy") == (1, 20)

def test_range_normal():
    assert get_range_for_difficulty("Normal") == (1, 100)

def test_range_hard():
    assert get_range_for_difficulty("Hard") == (1, 50)

def test_range_unknown_falls_back_to_default():
    # Any unrecognized difficulty should silently fall back to (1, 100)
    assert get_range_for_difficulty("Nightmare") == (1, 100)


def test_parse_guess_none():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None
    assert err == "Enter a guess."

def test_parse_guess_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err == "Enter a guess."

def test_parse_guess_valid_int_string():
    ok, value, err = parse_guess("50")
    assert ok is True
    assert value == 50
    assert err is None

def test_parse_guess_non_numeric_string():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err == "That is not a number."

def test_parse_guess_float_string_truncates_towards_zero():
    # Floats are truncated (via int(float(...))), not rounded:
    # "50.9" should parse to 50, not 51.
    ok, value, err = parse_guess("50.9")
    assert ok is True
    assert value == 50
    assert err is None


def test_update_score_win_normal_case():
    # attempt_number=0 -> points = 100 - 10*(0+1) = 90
    assert update_score(current_score=0, outcome="Win", attempt_number=0) == 90

def test_update_score_win_floors_at_ten():
    # A late win (e.g. attempt_number=20) would compute negative points
    # from the raw formula, but the score is never reduced below +10.
    assert update_score(current_score=0, outcome="Win", attempt_number=20) == 10

def test_update_score_too_high_always_subtracts_points():
    # Regression test for FIXME 5: even attempts used to add 5 instead.
    assert update_score(current_score=0, outcome="Too High", attempt_number=2) == -5
    assert update_score(current_score=0, outcome="Too High", attempt_number=3) == -5

def test_update_score_too_low_always_subtracts_points():
    assert update_score(current_score=0, outcome="Too Low", attempt_number=1) == -5
    assert update_score(current_score=0, outcome="Too Low", attempt_number=2) == -5

def test_update_score_unknown_outcome_is_unchanged():
    assert update_score(current_score=42, outcome="Something Else", attempt_number=1) == 42


# Challenge 1: edge-case inputs for parse_guess
def test_parse_guess_negative_number_is_accepted_as_int():
    # parse_guess only parses; range checking is not its job.
    ok, value, err = parse_guess("-5")
    assert ok is True
    assert value == -5
    assert err is None

def test_parse_guess_extremely_large_number():
    ok, value, err = parse_guess("99999999999999999999")
    assert ok is True
    assert value == 99999999999999999999
    assert err is None

def test_parse_guess_whitespace_padded_number_is_trimmed():
    ok, value, err = parse_guess("  42  ")
    assert ok is True
    assert value == 42
    assert err is None


# Challenge 2: high score tracker (uses pytest's tmp_path, never the real file)
def test_load_high_scores_missing_file_returns_empty(tmp_path):
    assert load_high_scores(tmp_path / "scores.json") == {}

def test_load_high_scores_corrupt_file_returns_empty(tmp_path):
    path = tmp_path / "scores.json"
    path.write_text("not json {")
    assert load_high_scores(path) == {}

def test_save_high_score_first_score_is_a_record(tmp_path):
    path = tmp_path / "scores.json"
    assert save_high_score(path, "Normal", 50) is True
    assert load_high_scores(path) == {"Normal": 50}

def test_save_high_score_higher_score_replaces_old(tmp_path):
    path = tmp_path / "scores.json"
    save_high_score(path, "Normal", 50)
    assert save_high_score(path, "Normal", 70) is True
    assert load_high_scores(path) == {"Normal": 70}

def test_save_high_score_lower_or_equal_score_is_ignored(tmp_path):
    path = tmp_path / "scores.json"
    save_high_score(path, "Normal", 50)
    assert save_high_score(path, "Normal", 30) is False
    assert save_high_score(path, "Normal", 50) is False
    assert load_high_scores(path) == {"Normal": 50}

def test_save_high_score_tracks_difficulties_separately(tmp_path):
    path = tmp_path / "scores.json"
    save_high_score(path, "Easy", 80)
    save_high_score(path, "Hard", 20)
    assert load_high_scores(path) == {"Easy": 80, "Hard": 20}
