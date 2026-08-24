# Improvements Checklist

Recommended changes for this bot, roughly ordered by priority. Check items off as they're done.

## Bugs

- [x] **Reaction roles don't work** (`main.py:184`) — `/reactionroles` posts the embed and reactions, but there's no `on_raw_reaction_add` / `on_raw_reaction_remove` handler that reads a user's reaction and calls `add_roles`/`remove_roles`. Needs that handler, keyed off `reaction_roles` and the message ID it posted. *(fixed in a46c010 — message ID tracked in memory; persistence across restarts still open, see below)*
- [x] **`GUILD_ID` isn't validated** (`main.py:26`) — `os.getenv('GUILD_ID')` returns `None` if the env var is missing, and `discord.Object(id=None)` will fail with a confusing error deep in `on_ready`. Fail fast with a clear message if `DISCORD_TOKEN` or `GUILD_ID` isn't set. *(fixed in a46c010)*

## Code quality

- [ ] **Duplicate function names for error handlers** (`main.py:157-172`) — `secret_error` is defined three times for `secret1.error`, `secret2.error`, `secret3.error`. Each decorator binds correctly at definition time so it isn't currently broken, but the shadowed name is confusing to read and easy to break during edits (e.g. copy-pasting a fourth one). Rename to `secret1_error`, `secret2_error`, `secret3_error`.
- [ ] **Remove or relocate `pythontest.py`** — looks like a scratch file unrelated to the bot; either delete it or move it under `tests/` if it's meant to stay.
- [ ] **Pin dependency versions** (`requirements.txt`) — `discord.py` has no version pin (only `python-dotenv` does). Pin it so a breaking release doesn't silently change bot behavior.
- [ ] **Logging level** (`main.py:209`) — `log_level=logging.DEBUG` dumps full guild/member/presence payloads into `discord.log` on every run. Fine for local debugging; switch to `logging.INFO` (or gate by an env var) before running unattended.

## Testing

- [ ] **`tests/bot_test.py` doesn't test the bot** — currently just demonstrates `AsyncMock` usage. Add real tests for command logic (e.g. blacklist regex matching, role-assignment branches) using `discord.py`'s test patterns or mocked `Interaction`/`ctx` objects.

## Config / hygiene

- [ ] **Document `bad_words.py` format** in README once the real word list exists (currently just a placeholder empty list).
- [ ] **Decide long-term home for role names vs role IDs** — commands currently look up roles by name (`Role_test_1`, etc.), which breaks silently if someone renames a role in Discord. Consider storing role IDs in `.env` or a config file instead.

## Possible features (optional, discuss before building)

- [ ] Slash-command equivalents for the remaining `!` prefix commands, for consistency.
- [ ] Persist `reaction_roles` message ID (e.g. to a small JSON/SQLite store) so the reaction-role handler survives bot restarts.
