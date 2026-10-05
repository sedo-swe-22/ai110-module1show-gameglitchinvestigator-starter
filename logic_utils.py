import json


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return the outcome.

    outcome examples: "Win", "Too High", "Too Low"
    """
    # FIXME 2 (fixed): "Too High"/"Too Low" messages were swapped in the original
    # app.py, telling the player to go the wrong direction.
    # FIX: AI helped trace the swapped branches during refactor; corrected the
    # direction and simplified the return value to just the outcome string (no
    # message tuple) to match the test contract in tests/test_game_logic.py.
    if guess == secret:
        return "Win"

    if guess > secret:
        return "Too High"

    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    # FIXME 5 (fixed): "Too High" used to add 5 points on even attempts and
    # subtract 5 on odd ones, rewarding a wrong guess on alternating turns.
    # FIX: AI flagged the leftover even/odd rule during review; wrong guesses
    # now always cost 5 points, same as "Too Low".
    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score


# Challenge 2 (High Score tracker): AI agent mode wrote these file helpers so the
# save/load logic stays out of app.py and can be tested with a temp file.
def load_high_scores(path):
    """Return {difficulty: best_score} from a JSON file, or {} if unusable."""
    try:
        with open(path) as f:
            data = json.load(f)
    except (OSError, ValueError):
        return {}
    if not isinstance(data, dict):
        return {}
    return data


def save_high_score(path, difficulty: str, score: int) -> bool:
    """Save score if it beats the stored best for difficulty; True if it did."""
    scores = load_high_scores(path)
    if difficulty in scores and score <= scores[difficulty]:
        return False
    scores[difficulty] = score
    with open(path, "w") as f:
        json.dump(scores, f)
    return True
