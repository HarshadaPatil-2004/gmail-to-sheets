## Project Overview :

This project is a Python automation system that connects to the Gmail API and Google Sheets API to read real incoming emails from a Gmail account and log them into a Google Sheet.

The script fetches unread emails, extracts relevant details, and appends them as new rows in Google Sheets while ensuring:
1.No duplicate processing
2.Emails are marked as read after logging
3.Only new emails are processed on every run


## Objective

Each qualifying email is logged into Google Sheets with the following columns:

Column	Description
From  -	Sender email address
Subject -	Email subject
Date -	Date & time received
Content -	Email body (plain text)



## High-Level Architecture

+-------------+        OAuth 2.0        +----------------+
|   Gmail     |  ------------------->  |   Python App   |
|   Inbox     |                        | (gmail_service)|
+-------------+                        +----------------+
                                            |
                                            | Parsed Data
                                            v
                                    +------------------+
                                    | Google Sheets API|
                                    | (sheets_service) |
                                    +------------------+


## Tech Stack
    1.Language: Python 3
    2.APIs Used:
    3.Gmail API
    4.Google Sheets API
    5.Authentication: OAuth 2.0 (User-based, no service accounts)


    gmail-to-sheets/


## Project Structure

│
├── src/
│   ├── gmail_service.py
│   ├── sheets_service.py
│   ├── email_parser.py
│   └── main.py
│
├── proof/
│   ├── gmail_unread.png
│   ├── sheet_rows.png
│   ├── oauth_screen.png
│   └── cmd_success.png
│
├── .gitignore
├── requirements.txt
├── README.md
└── config.py


## Setup Instructions

1. Clone the repository:
```bash
git clone <https://github.com/HarshadaPatil-2004/gmail-to-sheets.git>
cd gmail-to-sheets


Install dependencies:
pip install -r requirements.txt
Google Cloud Setup:

Create a Google Cloud project

Enable Gmail API and Google Sheets API

Configure OAuth consent screen (External)

Download credentials.json

Place it inside a local credentials/ folder (not committed)

Run the script:
bash
Copy code
python src/main.py


---

### OAuth Flow Explanation 
```md
## OAuth Flow Used
OAuth 2.0 user authentication is used. On first execution, the user is redirected to a Google consent screen to grant Gmail and Sheets access. Tokens are stored locally and reused in subsequent runs. Sensitive OAuth files are excluded from version control using `.gitignore`.

## Duplicate Prevention Logic
Only unread emails are fetched from the Gmail inbox. After processing, each email is marked as read. This ensures the same email is never processed twice even if the script is executed multiple times.

## State Persistence
Processed email state is maintained locally to ensure emails are not reprocessed on future executions. This lightweight approach avoids the need for a database and is suitable for single-user automation.

## Challenges Faced
Configuring OAuth correctly and handling permission errors was challenging. This was resolved by carefully setting OAuth scopes, configuring the consent screen properly, and testing token reuse across executions.

## Limitations
- Only unread inbox emails are processed
- Designed for single Gmail account
- Requires initial OAuth authentication

## Proof of Execution
Screenshots and demo video are included in the `proof/` folder showing:
- Gmail inbox with unread emails
- Google Sheet populated by the script
- OAuth consent screen
- Terminal execution output


## Demo Video Link
https://drive.google.com/file/d/1_d7x76nU67Qg6H7lmnjeyffp3uWCUsIC/view?usp=sharing
