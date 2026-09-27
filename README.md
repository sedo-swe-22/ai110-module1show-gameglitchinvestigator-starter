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
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] Describe the game's purpose.
- [ ] Detail which bugs you found.
  - FIXME 1: `secret` was being stringified on even attempts, which broke the win comparison against the numeric `guess`.
  - FIXME 2: the "Too High"/"Too Low" feedback messages were swapped, telling the player to go the wrong direction.
  - FIXME 3: clicking "New Game" reset `attempts` and `secret` but left `status` and `history` untouched, so the app immediately hit `st.stop()` on the stale "won"/"lost" status and looked stuck in the previous game.
  - FIXME 4: the guess input showed "Press Enter to apply" but pressing Enter did nothing, since a plain `st.text_input` outside a form only reruns the script on Enter - it doesn't set the Submit button's return value to `True`. Wrapped the input and Submit button in an `st.form` so Enter now submits the guess like clicking the button.
- [ ] Explain what fixes you applied.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Run `python -m streamlit run app.py` and open the app in the browser. Pick a difficulty from the sidebar (Easy/Normal/Hard) and note the range and attempts allowed.
2. Open the "Developer Debug Info" expander to see the secret number, current attempts, score, and guess history.
3. Type a guess that's too high and press **Enter** (no need to click the button) - the app submits immediately and shows the correct "📉 Go LOWER!" hint.
4. Type a guess that's too low and submit - the app now correctly shows "📈 Go HIGHER!" instead of the old swapped message.
5. Enter the exact secret number - the app shows balloons, a "You won!" message with the final score, and the debug info confirms the win.
6. Click **New Game 🔁** - a fresh secret is drawn, attempts/score/history all reset to zero, and the "You already won" screen is gone, so you can immediately play again.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
pytest tests/
============================= test session starts ==============================
platform darwin -- Python 3.13.14, pytest-9.1.1, pluggy-1.6.0
collected 18 items

tests/test_game_logic.py ..................                              [100%]

============================== 18 passed in 0.04s ===============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
