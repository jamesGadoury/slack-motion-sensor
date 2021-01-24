import os
from slack_sdk import WebClient

client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

response = client.chat_postMessage(
    channel=f"@{os.environ['SLACK_USER_ID']}",
    text="Hello world"
)
