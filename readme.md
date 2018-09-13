# Reminders
## Google Sheets + AWS Lambda

* Make sure aws credentials are stored somewhere accessible (preferably ~/.aws/credentials)
* Update dotenv with google service account credentials [[(get credentials)](https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html)

```bash
npm i -g serverless
npm i -D serverless-dotenv-plugin
sls plugin install -n serverless-python-requirements
sls deploy
sls invoke -f reminders
```

To run locally

```bash
pip install -r requirements.txt
pip install -r dev-requirements.txt
python reminders.py
```
