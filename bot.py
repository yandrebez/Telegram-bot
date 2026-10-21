import asyncio
import json
import os
import random
import re
import time

from dotenv import load_dotenv
from telethon import TelegramClient, events

load_dotenv()

CONFIG_PATH = os.environ.get("BOT_CONFIG", "config.json")
SESSION_NAME = os.environ.get("TG_SESSION", "autoresponder")


def load_config():
    with open(CONFIG_PATH, encoding="utf-8") as f:
        cfg = json.load(f)
    cfg["_required"] = [
        [re.compile(p, re.IGNORECASE) for p in group] for group in cfg["must_match"]
    ]
    return cfg


def matches(cfg, text):
    return all(any(p.search(text) for p in group) for group in cfg["_required"])


def main():
    cfg = load_config()
    client = TelegramClient(
        SESSION_NAME, int(os.environ["TG_API_ID"]), os.environ["TG_API_HASH"]
    )
    last_user_reply = {}
    last_chat_reply = {}

    @client.on(events.NewMessage(incoming=True))
    async def handler(event):
        # Groups only, never private chats or channels
        if not event.is_group or not event.raw_text:
            return
        allow = cfg.get("chat_allowlist", [])
        if allow and event.chat_id not in allow:
            return
        sender = await event.get_sender()
        if sender is None or getattr(sender, "bot", False):
            return
        if not matches(cfg, event.raw_text):
            return

        now = time.time()
        if now - last_user_reply.get(sender.id, 0) < cfg["cooldown_per_user_seconds"]:
            return
        if now - last_chat_reply.get(event.chat_id, 0) < cfg["cooldown_per_chat_seconds"]:
            return
        # Claim the slots before sleeping so a burst can't double-reply
        last_user_reply[sender.id] = now
        last_chat_reply[event.chat_id] = now

        lo, hi = cfg["reply_delay_seconds"]
        await asyncio.sleep(random.uniform(lo, hi))
        await event.reply(cfg["reply_text"])
        print(f"Replied to {sender.id} in chat {event.chat_id}")

    with client:
        print("Auto-responder running. Ctrl+C to stop.")
        client.run_until_disconnected()


if __name__ == "__main__":
    main()
