import date
import boto3

def get_billings():
    client = boto3.client('ce', region_name='us-east-1')

    starttime, endtime = get_datetime_range()
    response = client.get_cost_and_usage(
        TimePeriod = {
            "Start": starttime.strftime("%Y-%m-%d"),
            "End": endtime.strftime("%Y-%m-%d")
        },
        Granularity="MONTHLY",
        Metrics = [
            "AmortizedCost"
        ],
        GroupBy = [
            {
                "Type": "DIMENSION",
                "Key": "SERVICE"
            }
        ]
    )

    services, total = {}, 0.0
    for item in response["ResultsByTime"][0]["Groups"]:
        name = item["Keys"][0]
        billing = float(item["Metrics"]["AmortizedCost"]["Amount"])

        if billing < 0.001:
            continue

        services[name] = billing
        total += billing

    return {"total": total, "services": services}

def get_datetime_range():
    endtime = date.today()
    starttime = date.beginning_of_month(endtime)

    if starttime == endtime:
        starttime = date.prevday(starttime)
        starttime = date.beginning_of_month(starttime)
    
    return starttime, endtime