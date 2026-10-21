# Telegram Group Auto-Responder

Replies from your own Telegram account when someone in a group asks for a local group.

## Setup
1. Get `api_id` / `api_hash` at https://my.telegram.org -> API development tools.
2. `cp .env.example .env` and fill in both values.
3. `cp config.example.json config.json` and edit your reply text, patterns and area words.
4. `pip install -r requirements.txt`
5. `python bot.py` — first run asks for your phone number and login code, then keeps a local `.session` file.

## Config (`config.json`)
- `reply_text`: message sent as a reply to the person asking.
- `must_match`: list of groups of regexes (case-insensitive). A message triggers a reply only if **every** group has at least one match, i.e. the phrase AND the age range AND one of the areas.
- `chat_allowlist`: list of chat IDs to respond in; empty means all groups you're in.
- `reply_delay_seconds`: random [min, max] pause before replying.
- `cooldown_per_user_seconds` / `cooldown_per_chat_seconds`: limits to avoid repeat replies and spam flags.

Keep `.env` and `*.session` private; they give full access to your account.
