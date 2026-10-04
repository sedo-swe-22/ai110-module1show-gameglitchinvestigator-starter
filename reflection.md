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
| Guess higher than the secret | "Go LOWER!" hint | "Go HIGHER!" hint (hints swapped) | None, no error |
| Finish a game, then click "New Game" | A fresh game starts | Stuck on the old "You already won" / "Game over" screen | None, `st.stop()` ran silently |
| Make several guesses in a row | Every guess compared as a number | On even attempts the secret was turned into a string, so comparisons were wrong | None, no exception shown |
| Type a guess and press Enter | The guess is submitted | Nothing happened until I clicked Submit | None, no error |

---

## 2. How did you use AI as a teammate?

I used Claude Code in agent mode as my pair-programming partner for the whole repair: it read `app.py`, proposed fixes for each FIXME, edited the files directly, and ran `pytest`/`py_compile` after every change to confirm nothing broke.

**A suggestion that was correct:** For FIXME 4 (the guess box said "Press Enter to apply" but Enter did nothing), the AI explained that a plain `st.text_input` outside a form only reruns the script on Enter - it never sets a separate `st.button`'s return value to `True`. It suggested wrapping the input and the Submit button in an `st.form`, since Streamlit forms are specifically built so that pressing Enter anywhere inside them triggers the `form_submit_button`. I verified this with Streamlit's `AppTest` framework (simulating the form submit and checking `session_state`): the guess was correctly evaluated, the score updated, and `status` flipped to `"won"` on a correct guess - confirming the fix actually wires Enter up to the same code path as clicking the button.

**A suggestion I didn't accept as written:** To verify the FIXME 4 fix, the AI first suggested using a live Chrome browser session (via a browser-automation skill) to literally type a guess and press Enter. I declined to install the browser extension that required, since it was heavier setup than the check needed. The AI adjusted and instead verified the fix using Streamlit's built-in `AppTest` testing utility, which drives the actual script without any browser dependency. This wasn't a "wrong" suggestion, just a poor fit given I didn't want to install new tooling for a one-off check - and the `AppTest` route turned out to be just as convincing since it exercises the real form-submission code path.

---

## 3. Debugging and testing your fixes

I counted a bug as fixed only when the symptom I had reproduced was gone and `pytest tests/` still passed. For the state bugs (FIXME 3 and 4) I also used Streamlit's `AppTest` to run the app headlessly and check `st.session_state`. For example, after fixing FIXME 3 I submitted the winning guess, clicked "New Game", and asserted `status == "playing"`, `attempts == 0` and `history == []`. I asked the AI to list the untested behaviors in `logic_utils.py` before writing tests, which grew the suite from 3 to 18 passing tests, and three more edge-case tests later brought it to 21. One caveat: the tests assert that a "Too High" guess scores +5 on even attempts and -5 on odd ones, which I first took as intended but now suspect is another leftover bug that the tests simply lock in.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  Every time you click a button or type something, Streamlit runs the whole script again from the top, so any normal variable goes back to its starting value. `st.session_state` is a small memory that survives those reruns, so things like the secret number, attempts, score and history have to live there. Several of the original bugs came from state being reset, or only partly reset, between reruns.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
  - I'll ask the AI to list which behaviors have no tests before it writes any, and I'll verify each fix with `pytest` or `AppTest` rather than trusting that it looks right. I also liked making one small commit per fix.
- What is one thing you would do differently next time you work with AI on a coding task?
  - I'd read the surrounding code myself before accepting a change, and question behavior the AI calls intentional, like the even/odd scoring rule I almost let through.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
  - AI-generated code can look finished while hiding bugs, so it needs the same tests and review as code I wrote myself.
