import json
import os
import sys
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
from colorama import Fore, Style, init
from gmail_service import (
    get_gmail_service,
    fetch_unread_emails,
    get_email,
    mark_as_read
)
from email_parser import parse_email
from sheets_service import get_sheets_service, append_row
from config import SUBJECT_KEYWORD, STATE_FILE

init(autoreset=True)


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def main():
    print(Fore.CYAN + Style.BRIGHT + " Gmail → Sheets Automation Started")

    gmail_service = get_gmail_service()
    sheets_service = get_sheets_service(gmail_service._http.credentials)

    state = load_state()
    last_history_id = state.get("last_history_id", "0")

    messages = fetch_unread_emails(gmail_service)
    print(Fore.YELLOW + f" Unread emails found: {len(messages)}")

    for msg in messages:
        email = get_email(gmail_service, msg["id"])

        history_id = email["historyId"]
        if history_id <= last_history_id:
            continue

        parsed = parse_email(email)

        if SUBJECT_KEYWORD and SUBJECT_KEYWORD not in parsed["subject"]:
            continue

        append_row(
            sheets_service,
            [parsed["from"], parsed["subject"], parsed["date"], parsed["content"]]
        )

        mark_as_read(gmail_service, msg["id"])

        print(Fore.GREEN + f"✔ Logged: {parsed['subject']}")

        state["last_history_id"] = history_id

    save_state(state)
    print(Fore.MAGENTA + Style.BRIGHT + " Automation Completed Successfully")


if __name__ == "__main__":
    main()
