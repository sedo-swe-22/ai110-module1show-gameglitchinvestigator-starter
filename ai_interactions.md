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
