import json
import datetime
import os

from ce import get_billings

import requests

SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]

def lambda_handler(event, context):
    notify(get_billings())

def build_message(billings):
    total = billings["total"]

    # summary
    message_text = "Current total bill is *${:.2f}*".format(total)

    # details
    attachment_text = ["```"]
    for name, billing in billings["services"].items():
        line = f"{name:<40} : ${billing:.3f}"
        attachment_text.append(line)
    attachment_text.append("```")

    color = "good" if total < 50 else "danger"
    atachements = {
        "text": "\n".join(attachment_text),
        "mrkdwn_in": ["text"],
        "color": color
    }

    message = {
        "text": message_text,
        "attachments": [atachements],
    }

    return message

def notify(billings):
    message = build_message(billings)
    response = requests.post(SLACK_WEBHOOK_URL, data=json.dumps(message))
    response.raise_for_status()