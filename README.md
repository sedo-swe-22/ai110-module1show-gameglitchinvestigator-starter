# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.**
   - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Game purpose:** a Streamlit number-guessing game. The player picks a difficulty (Easy/Normal/Hard), which sets the number range and attempt limit. They guess a secret number, get "Go HIGHER!" / "Go LOWER!" hints, and earn a score that rewards winning in fewer attempts.
- [x] **Bugs found:**
  - FIXME 1: `secret` was being stringified on even attempts, which broke the win comparison against the numeric `guess`.
  - FIXME 2: the "Too High"/"Too Low" feedback messages were swapped, telling the player to go the wrong direction.
  - FIXME 3: clicking "New Game" reset `attempts` and `secret` but left `status` and `history` untouched, so the app immediately hit `st.stop()` on the stale "won"/"lost" status and looked stuck in the previous game.
  - FIXME 4: the guess input showed "Press Enter to apply" but pressing Enter did nothing, since a plain `st.text_input` outside a form only reruns the script on Enter - it doesn't set the Submit button's return value to `True`.
  - FIXME 5: "Too High" guesses added 5 points on even attempts and subtracted 5 on odd ones, so a wrong guess could raise the score.
- [x] **Fixes applied:**
  - FIXME 1: removed the branch that converted `secret` to a string, so guesses are always compared as integers.
  - FIXME 2: corrected the swapped branches in `check_guess` so a high guess returns "Too High" (shown as "Go LOWER!") and a low guess returns "Too Low" (shown as "Go HIGHER!").
  - FIXME 3: "New Game" now also resets `status`, `history` and `score`, so a fresh game starts cleanly.
  - FIXME 4: wrapped the input and Submit button in an `st.form`, so Enter now submits the guess like clicking the button.
  - FIXME 5: `update_score` now subtracts 5 for every wrong guess ("Too High" or "Too Low"), with a regression test.
  - Refactored the game logic (`parse_guess`, `check_guess`, `update_score`, difficulty ranges) out of `app.py` into `logic_utils.py`, and added 20 pytest tests covering difficulty ranges, guess parsing and scoring edge cases.

## 📸 Demo Walkthrough

A sample game on **Normal** difficulty, where the secret number happens to be 55 (visible in the "Developer Debug Info" expander):

1. Run `python -m streamlit run app.py`, open the app and pick **Normal** in the sidebar. Score starts at 0 and attempts at 0.
2. The user enters a guess of **70** and presses Enter. The game shows "📉 Go LOWER!" and the score becomes **-5**.
3. The user enters **40**. The game shows "📈 Go HIGHER!" and the score becomes **-10**.
4. The user enters **55**. The game shows balloons and "You won! The secret was 55. Final score: 50" (60 points for winning on attempt 3, minus the 10 from earlier misses).
5. Any further guess is blocked with "You already won. Start a new game to play again."
6. The user clicks **New Game 🔁**. A new secret is drawn, and attempts, score and history reset to zero, so they can play again immediately.

## 🧪 Test Results

Challenge 1 (advanced edge-case tests):

```
pytest tests/
============================= test session starts ==============================
platform darwin -- Python 3.13.14, pytest-9.1.1, pluggy-1.6.0
collected 20 items

tests/test_game_logic.py ....................                            [100%]

============================== 20 passed in 0.04s ==============================
```

## 🚀 Stretch Features

Not attempted.
