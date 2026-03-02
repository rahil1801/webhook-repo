# Webhook Repo – GitHub Webhook Receiver

This repository receives GitHub webhook events from `action-repo`,
stores minimal required data into MongoDB,
and displays updates in a clean UI polling every 15 seconds.

---

## Supported Events

- PUSH
- PULL_REQUEST
- MERGE

---

## MongoDB Schema

{
  request_id: string,
  author: string,
  action: "PUSH" | "PULL_REQUEST" | "MERGE",
  from_branch: string,
  to_branch: string,
  timestamp: string (UTC formatted)
}

---

## Setup Instructions

1. Clone the repo
2. Create virtual environment

   python -m venv venv
   source venv/bin/activate  (or venv\Scripts\activate on Windows)

3. Install dependencies

   pip install -r requirements.txt

4. Create .env file

   MONGO_URI=mongodb://localhost:27017/github_webhooks
   SECRET_KEY=your_secret

5. Run the server

   python run.py

---

## Using ngrok

1. Install ngrok
2. Start Flask app on port 5000
3. Run:

   ngrok http 5000

4. Copy the HTTPS URL
5. Go to action-repo → Settings → Webhooks
6. Add new webhook:

   Payload URL:
   https://your-ngrok-url/webhook/receiver

   Content Type:
   application/json

   Events:
   - Push
   - Pull Requests

---

## UI

Visit:

http://localhost:5000/webhook/ui

The UI polls MongoDB every 15 seconds and displays latest activity.

---

## Application Flow

Action Repo → GitHub Webhook → Flask Endpoint → MongoDB → UI (Polling every 15 sec)

---

## Brownie Point Implemented

If a Pull Request is merged, it is stored as:

MERGE action

Format:
{author} merged branch {from_branch} to {to_branch} on {timestamp}

---

## Repositories for Submission

- action-repo: (Add Link)
- webhook-repo: (Add Link)