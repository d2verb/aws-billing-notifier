import json
import datetime
import os

import boto3
import requests
import pytz

SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]

def lambda_handler(event, context):
    billing = get_billing()
    notify(billing)

def get_billing():
    now = datetime.datetime.now()

    cloudwatch = boto3.resource("cloudwatch", region_name="us-east-1")
    metric = cloudwatch.Metric("AWS/Billing", "EstimatedCharges")

    response = metric.get_statistics(
        Dimensions = [
            {
                "Name": "Currency",
                "Value": "USD"
            },
        ],
        StartTime = now - datetime.timedelta(days=1),
        EndTime = now,
        Period = 3600 * 24, # 1 day
        Statistics = ["Maximum"]
    )

    datapoint = response["Datapoints"][0]
    billing = {
        "cost": datapoint["Maximum"],
        "timestamp": now
    }
    return billing

def build_message(billing):
    attachment_text = "${}".format(billing["cost"])
    atachements = {"text": attachment_text}

    endtime = billing["timestamp"].astimezone(pytz.timezone("Asia/Tokyo")).strftime("%Y-%m-%d %H:%M")
    message_text = "Total cost as of {}".format(endtime)

    message = {
        "text": message_text,
        "attachments": [atachements],
    }

    return message

def notify(billing):
    message = build_message(billing)
    response = requests.post(SLACK_WEBHOOK_URL, data=json.dumps(message))
    response.raise_for_status()