import urllib3
import json
import yaml

http = urllib3.PoolManager()


def lambda_handler(event, context):
    url = $SLACK_CHANNEL_URL
    changes = yaml.dump(remove_empty_dicts(event["detail"]["requestParameters"]))
    if event["detail"]["recipientAccountId"] == "111122223333":
        AccountName = "DEV"
    elif event["detail"]["recipientAccountId"] == "444455556666":
        AccountName = ":bangbang: PROD :bangbang:"
    elif event["detail"]["recipientAccountId"] == "777788889999":
        AccountName = "Stage"
    text = "\n".join(['<!channel>',
            f'*EventTime*: {event["detail"]["eventTime"]}',
            f'*EventName*: {event["detail"]["eventName"]}',
            f'*AwsRegion*: {event["detail"]["awsRegion"]}',
            f'*AccountId*: {event["detail"]["recipientAccountId"]}',
            f'*AccountName*: {AccountName}',
            f'*UserIdentity*: {event["detail"]["userIdentity"]["arn"]}',
            f'*UserAgent*: {event["detail"]["userAgent"]}',
            f'*Changes*: \n{str(changes)}'])
    msg = {
        "channel": "#CHANNEL_NAME",
        "username": "WEBHOOK_USERNAME",
        "text": text,
        "icon_emoji": ""
    }
    encoded_msg = json.dumps(msg).encode("utf-8")
    resp = http.request("POST", url, body=encoded_msg)
    print(
        {
            "message": event["detail"],
            "status_code": resp.status,
            "response": resp.data,
        }
    )
