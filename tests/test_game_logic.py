from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
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

def test_update_score_too_high_even_attempt_adds_points():
    assert update_score(current_score=0, outcome="Too High", attempt_number=2) == 5

def test_update_score_too_high_odd_attempt_subtracts_points():
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
