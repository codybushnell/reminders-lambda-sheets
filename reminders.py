import json
from utils import GoogleSheetsClient,  Reminder
from os import getenv


def handler(event, context):

    WORKBOOK = "pushups"
    WORKSHEET = "pushups"

    DATE_COL = "A"
    TEXT_COL = "D"


    gsc = GoogleSheetsClient(local=True) if event == "local" else GoogleSheetsClient()
    gsc.login()

    pushups_reminder = Reminder(
        "PUSHUPS",
        gsc._client,
        WORKBOOK,
        WORKSHEET,
        DATE_COL,
        TEXT_COL
    )

    pushups_reminder.send_reminder(
        twilio_account=getenv("twilio_account"),
        twilio_key=getenv("twilio_token"),
        to=getenv("to_number"),
        from_=getenv("twilio_number"),
    )

    response = {
        "statusCode": 200,
        "body": "success!"
    }

    return response

if __name__ == "__main__":
    print("testing")
    from dotenv import find_dotenv, load_dotenv
    load_dotenv(find_dotenv())
    handler("local", None)
