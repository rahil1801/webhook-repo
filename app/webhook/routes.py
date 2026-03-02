from flask import Blueprint, request, jsonify, render_template_string
from app.extensions import mongo
from datetime import datetime
import pytz

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

def format_timestamp():
    utc_now = datetime.utcnow().replace(tzinfo=pytz.UTC)
    return utc_now.strftime("%d %B %Y - %I:%M %p UTC")

#WEBHOOOK RECEIVER
@webhook.route('/receiver', methods=["POST"])
def receiver():
    data = request.json

    event_type = request.headers.get('X-GitHub-Event')

    document = {}

    # PUSH EVENT
    if event_type == "push":
        document = {
            "request_id": data.get("after"),
            "author": data.get("pusher", {}).get("name"),
            "action": "PUSH",
            "from_branch": None,
            "to_branch": data.get("ref").split("/")[-1],
            "timestamp": format_timestamp()
        }

    # PULL REQUEST EVENT
    elif event_type == "pull_request":
        pr = data.get("pull_request", {})

        document = {
            "request_id": str(pr.get("id")),
            "author": pr.get("user", {}).get("login"),
            "action": "PULL_REQUEST",
            "from_branch": pr.get("head", {}).get("ref"),
            "to_branch": pr.get("base", {}).get("ref"),
            "timestamp": format_timestamp()
        }

        #MERGE EVENT
        if pr.get("merged") is True:
            document["action"] = "MERGE"

    else:
        return jsonify({"message": "Event ignored"}), 200

    mongo.db.events.insert_one(document)

    return jsonify({"message": "Webhook received"}), 200

#API TO FETCH EVENTS
@webhook.route('/events', methods=["GET"])
def get_events():
    events = list(mongo.db.events.find().sort("_id", -1).limit(20))

    for event in events:
        event["_id"] = str(event["_id"])

    return jsonify(events)

#UI CODE
# UI CODE
@webhook.route('/ui', methods=["GET"])
def ui():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>GitHub Activity Dashboard</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, #667eea, #764ba2);
                min-height: 100vh;
                padding: 50px 20px;
            }

            h2 {
                text-align: center;
                color: white;
                font-weight: 600;
                margin-bottom: 40px;
                font-size: 28px;
                letter-spacing: 1px;
            }

            .container {
                max-width: 900px;
                margin: auto;
            }

            .card {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                padding: 20px 25px;
                margin-bottom: 18px;
                border-radius: 12px;
                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
                transition: all 0.25s ease;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .card:hover {
                transform: translateY(-4px);
                box-shadow: 0 12px 28px rgba(0, 0, 0, 0.2);
            }

            .event-text {
                font-size: 15px;
                font-weight: 500;
                color: #333;
            }

            .timestamp {
                font-size: 13px;
                color: #666;
                margin-top: 6px;
            }

            .badge {
                padding: 6px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 600;
                color: white;
                white-space: nowrap;
            }

            .push { background: #3b82f6; }
            .pull { background: #f59e0b; }
            .merge { background: #10b981; }

            .empty {
                text-align: center;
                color: white;
                font-weight: 500;
                opacity: 0.9;
            }

            @media (max-width: 768px) {
                .card {
                    flex-direction: column;
                    align-items: flex-start;
                    gap: 10px;
                }
            }
        </style>
    </head>
    <body>

        <h2>GitHub Activity Dashboard</h2>

        <div class="container">
            <div id="events"></div>
        </div>

        <script>
            async function fetchEvents() {
                const res = await fetch('/webhook/events');
                const data = await res.json();
                const container = document.getElementById('events');
                container.innerHTML = "";

                if (!data.length) {
                    container.innerHTML = `<div class="empty">No recent GitHub activity found.</div>`;
                    return;
                }

                data.forEach(event => {
                    let text = "";
                    let badgeClass = "";
                    let badgeText = "";

                    if (event.action === "PUSH") {
                        text = `<strong>${event.author}</strong> pushed new commits to <strong>${event.to_branch}</strong>.`;
                        badgeClass = "push";
                        badgeText = "PUSH";
                    }
                    else if (event.action === "PULL_REQUEST") {
                        text = `<strong>${event.author}</strong> opened a pull request from <strong>${event.from_branch}</strong> to <strong>${event.to_branch}</strong>.`;
                        badgeClass = "pull";
                        badgeText = "PULL REQUEST";
                    }
                    else if (event.action === "MERGE") {
                        text = `<strong>${event.author}</strong> successfully merged <strong>${event.from_branch}</strong> into <strong>${event.to_branch}</strong>.`;
                        badgeClass = "merge";
                        badgeText = "MERGE";
                    }

                    container.innerHTML += `
                        <div class="card">
                            <div>
                                <div class="event-text">${text}</div>
                                <div class="timestamp">${event.timestamp}</div>
                            </div>
                            <span class="badge ${badgeClass}">${badgeText}</span>
                        </div>
                    `;
                });
            }

            fetchEvents();
            setInterval(fetchEvents, 15000);
        </script>

    </body>
    </html>
    """)