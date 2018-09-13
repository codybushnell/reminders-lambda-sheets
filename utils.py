import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime
import string
from twilio.rest import Client
from os import environ, getenv


class Reminder:

    def __init__(
        self,
        name,
        google_sheets_client,
        workbook,
        worksheet,
        date_col,
        text_col,
        max_rows=1000
    ):
        min_col, max_col = [
            string.ascii_uppercase.find(x)
            for x
            in [date_col, text_col]
        ]
        col_count = max_col - min_col + 1

        worksheet = google_sheets_client.open(
            workbook
        ).worksheet(
            worksheet
        )
        data = worksheet.range(
            "{}1:{}{}".format(
                date_col,
                text_col, max_rows
            )
        )

        df = pd.DataFrame(
            [
                [
                    y.value
                    for y in
                    data[x:x+col_count]
                ]
                for x in range(
                    0,
                    int(len(data)/col_count),
                    col_count
                )  # noqa
            ],
            columns=['Date'] + \
                ["temp{}".format(x) for x in range(col_count-2)] + \
                ["text"]
        ).iloc[:, [min_col, max_col]].dropna()

        df.Date = pd.DatetimeIndex(df.Date)

        now = datetime.now()

        text_to_send = df.loc[(1/(df.Date - now).dt.days).idxmin(), "text"]

        self.text_to_send = "{} REMINDER {}: {}".format(
            name,
            now.strftime("%B %d, %Y"),
            text_to_send
        )

    def send_reminder(
        self,
        twilio_account,
        twilio_key,
        to,
        from_,
    ):

        client = Client(
            twilio_account,
            twilio_key
        )

        client.messages.create(
            to=to,
            from_=from_,
            body=self.text_to_send
        )


class GoogleSheetsClient:

    def __init__(self):

        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]

        cred_var_prefix = "gc_"

        cred_keys = [
            x
            for x
            in list(environ.keys())
            if cred_var_prefix == x[:len(cred_var_prefix)]
        ]

        cred_dict = {
            ck[len(cred_var_prefix):]: getenv(ck).replace("\\\\n", "\n")
            for ck
            in cred_keys
        }

        self._credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            cred_dict,
            scope
        )

    def login(self):

        self._client = gspread.authorize(
            self._credentials
        )
