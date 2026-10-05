# AI Interactions Log

## Test Generation (Challenge 1: Advanced Edge-Case Testing)

**Prompt used:**

```
Review parse_guess in logic_utils.py and identify three edge-case inputs that
could still break the game (for example negative numbers, extremely large
values, odd whitespace). Add pytest cases to tests/test_game_logic.py that
check them, based on how the function actually behaves.
```

| Edge Case | Why I chose it | AI-Suggested Test | Did It Pass? |
|-----------|----------------|-------------------|--------------|
| `"-5"` | Players can type negatives, which are outside every difficulty range. | `test_parse_guess_negative_number_is_accepted_as_int` | Yes |
| `"99999999999999999999"` | Checks that a huge value does not crash or overflow the parser. | `test_parse_guess_extremely_large_number` | Yes |
| `"  42  "` | Players often paste or type stray spaces around a number. | `test_parse_guess_whitespace_padded_number_is_trimmed` | Yes |

**Note:** `parse_guess` only parses; it does not range-check, so negative and huge values count as valid guesses and the game logic treats them as ordinary "Too High"/"Too Low" results.

---

## Agent Workflow (Challenge 2: High Score tracker)

**Files modified:** `logic_utils.py` (new `load_high_scores` / `save_high_score`), `app.py` (sidebar "Best score" and a save on win), `tests/test_game_logic.py` (6 new tests), `.gitignore` (ignore `highscores.json`), `README.md` and this file (docs).

**What I asked the agent to do:**

```
Plan and implement a meaningful new feature, such as a "High Score" tracker that
saves your best score to a file. Plan first, then build it.
```

I picked the High Score tracker from the options the agent offered, and approved its written plan before any code was changed.

**What the agent completed:**
- Added `load_high_scores(path)`, which returns `{}` for a missing, unreadable or corrupt file, and `save_high_score(path, difficulty, score)`, which only writes when the score beats the stored best and returns `True` for a new record.
- Added six `tmp_path`-based pytest cases covering missing file, corrupt file, first score, higher score, lower or equal score, and separate difficulties (26 tests total at that point).
- Wired it into `app.py`: the sidebar shows the best score for the selected difficulty, and a win saves the score and shows "🏆 New high score!" on a record.
- Verified the whole flow headlessly with Streamlit's `AppTest`: a first win created `highscores.json`, a later worse win left it unchanged, and a corrupt file did not crash the app.
- Committed in three steps (logic and tests, UI, docs).

**What I had to verify or fix manually:** I made no code corrections to the agent's work. Its first headless test script failed with `ModuleNotFoundError: No module named 'logic_utils'` because the script lived outside the repo; it was rerun with `PYTHONPATH` set to the repo and then passed. I have not yet played the feature in a real browser session.
