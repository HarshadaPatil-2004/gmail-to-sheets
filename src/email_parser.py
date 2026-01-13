import base64
from bs4 import BeautifulSoup
from email.utils import parsedate_to_datetime


def extract_headers(headers):
    data = {}
    for h in headers:
        data[h["name"]] = h["value"]
    return data


def get_body(payload):
    if "data" in payload.get("body", {}):
        return decode(payload["body"]["data"])

    for part in payload.get("parts", []):
        mime = part.get("mimeType", "")
        if mime == "text/plain":
            return decode(part["body"]["data"])
        if mime == "text/html":
            html = decode(part["body"]["data"])
            return BeautifulSoup(html, "html.parser").get_text()

    return ""


def decode(data):
    return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")


def parse_email(message):
    headers = extract_headers(message["payload"]["headers"])

    body = get_body(message["payload"])

    return {
        "from": headers.get("From", ""),
        "subject": headers.get("Subject", ""),
        "date": str(parsedate_to_datetime(headers.get("Date"))),
        "content": body.strip()
    }
