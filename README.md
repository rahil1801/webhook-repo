# Webhook Repo – GitHub Webhook Receiver

This repository receives GitHub webhook events from the `action-repo`, stores required event data into MongoDB, and displays the activity in a clean UI that polls every 15 seconds.

---

## Supported Events

The webhook receiver handles the following GitHub events:

- Push
- Pull Request (Opened)
- Pull Request (Merged → stored as `MERGE` action)

---

## Recommended Folder Structure


webhook-repo/  
│  
├── app/  
│ ├── init.py  
│ ├── routes.py  
│ ├── models.py  
│ └── extensions.py  
│   
├── .env  
├── requirements.txt  
├── run.py  
└── README.md  


This structure keeps the application modular and clean.

---

## MongoDB Schema

Each event is stored in MongoDB with the following structure:

```json
{
  "request_id": "string",
  "author": "string",
  "action": "PUSH | PULL_REQUEST | MERGE",
  "from_branch": "string",
  "to_branch": "string",
  "timestamp": "UTC formatted string"
}
```

# Setup Instructions
1. Clone the Repository  
```bash
git clone https://github.com/rahil1801/webhook-repo.git

cd webhook-repo
```

2. Create Virtual Environment
```bash
python -m venv venv

Activate it:

Windows:

venv\Scripts\activate

Mac/Linux:

source venv/bin/activate
```

3. Install Dependencies
```bash
pip install -r requirements.txt
```

4. Create .env File

Create a .env file in the root directory:
```bash
MONGO_URI=mongodb://localhost:27017/github_webhooks
SECRET_KEY=your_secret_key
```
5. Run the Server
```bash
python run.py

The server will start at:

http://localhost:5000
```

Using ngrok
1. Install ngrok from microsoft Store

Or you can also Download and install it from https://ngrok.com/

2. Start Flask App

Make sure your app is running on port 5000.

3. Expose Local Server
```bash
ngrok http 5000
```
You will receive a public HTTPS URL.

4. Configure Webhook in action-repo

Go to:

action-repo → Settings → Webhooks → Add Webhook

Set:
```bash
Payload URL: https://your-ngrok-url/webhook/receiver

Content Type: application/json

Check these two Events:
Push
Pull Requests
```
Save the webhook.

# UI Dashboard

Visit:

http://localhost:5000/webhook/ui or https://your-ngrok-url/webhook/ui

# Features:

• Displays latest GitHub activity

• Polls MongoDB every 15 seconds

• Shows latest entries first

• Clean formatted event messages

# Example

If a Pull Request is merged, it is stored as:

action: "MERGE"

Formatted Display:
```bash
{author} merged branch {from_branch} to {to_branch} on {timestamp}
```
This differentiates normal PR creation from actual merges.

# Repositories for Submission
```bash
action-repo: https://github.com/rahil1801/action-repo

webhook-repo: https://github.com/rahil1801/webhook-repo
```
