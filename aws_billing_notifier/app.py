import json
import datetime
import os

import boto3
import requests
import pytz
from ce import get_billings

SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]

def lambda_handler(event, context):
    client = boto3.client('ce', region_name='us-east-1')
    billings = get_billings(client)
    notify(billings)

def build_message(billings):
    total = billings["total"]
    message_text = "Current total bill is *${:.2f}*".format(total)

    attachment_text = []
    for name, billing in billings["services"].items():
        line = f"{name:<40} : ${billing:.3f}"
        attachment_text.append(line)

    color = "good" if total < 50 else "danger"

    atachements = {
        "text": "```\n" + "\n".join(attachment_text) + "\n```",
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