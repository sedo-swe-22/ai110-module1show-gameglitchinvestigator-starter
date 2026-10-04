# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
  It seems it works, but after playing couple of games, it turned out not to work.
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
  1. The hint was wrong, it gives the opposite direction.
  2. 'New Game' button didn't work, so I had to refresh the game page after the game was done.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| | | | |
| | | | |
| | | | |

---

## 2. How did you use AI as a teammate?

I used Claude Code in agent mode as my pair-programming partner for the whole repair: it read `app.py`, proposed fixes for each FIXME, edited the files directly, and ran `pytest`/`py_compile` after every change to confirm nothing broke.

**A suggestion that was correct:** For FIXME 4 (the guess box said "Press Enter to apply" but Enter did nothing), the AI explained that a plain `st.text_input` outside a form only reruns the script on Enter - it never sets a separate `st.button`'s return value to `True`. It suggested wrapping the input and the Submit button in an `st.form`, since Streamlit forms are specifically built so that pressing Enter anywhere inside them triggers the `form_submit_button`. I verified this with Streamlit's `AppTest` framework (simulating the form submit and checking `session_state`): the guess was correctly evaluated, the score updated, and `status` flipped to `"won"` on a correct guess - confirming the fix actually wires Enter up to the same code path as clicking the button.

**A suggestion I didn't accept as written:** To verify the FIXME 4 fix, the AI first suggested using a live Chrome browser session (via a browser-automation skill) to literally type a guess and press Enter. I declined to install the browser extension that required, since it was heavier setup than the check needed. The AI adjusted and instead verified the fix using Streamlit's built-in `AppTest` testing utility, which drives the actual script without any browser dependency. This wasn't a "wrong" suggestion, just a poor fit given I didn't want to install new tooling for a one-off check - and the `AppTest` route turned out to be just as convincing since it exercises the real form-submission code path.

---

## 3. Debugging and testing your fixes

I considered a bug fixed only after two things lined up: the specific symptom I'd reproduced was gone, and `pytest tests/` still passed (or, for a new fix, started passing) with no regressions elsewhere. For state-related bugs (FIXME 3 and FIXME 4) I also used Streamlit's `AppTest` to run the app headlessly and inspect `st.session_state` directly before and after clicking a button, since those bugs weren't visible in unit tests alone.

One concrete test: after fixing FIXME 3 (New Game not resetting the game), I ran an `AppTest` script that clicked "Submit Guess" with the correct answer, confirmed `status == "won"`, then clicked "New Game" and asserted `status == "playing"`, `attempts == 0`, and `history == []`. Before the fix, `status` stayed `"won"` after New Game, which meant the app hit `st.stop()` on the very next rerun and looked frozen - the test made that failure obvious instead of me having to guess from the UI.

For `logic_utils.py`, I ran `pytest tests/ -v` after every change. Once `check_guess`, `get_range_for_difficulty`, `parse_guess`, and `update_score` were all refactored in, the suite went from 3 tests (only covering `check_guess`) to 18 passing tests in `0.04s`.

AI did help design the tests: I asked it to first review `logic_utils.py` and report which behaviors had no test coverage before writing anything. It identified several non-obvious rules I hadn't thought to test myself - the score floor of `10` on a late win, the deliberately different even/odd scoring for "Too High", `parse_guess` truncating (not rounding) decimal strings like `"50.9"` to `50`, and the silent fallback to `(1, 100)` for an unrecognized difficulty. I reviewed that list, asked for tests covering all of them, and confirmed all 18 passed together.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
