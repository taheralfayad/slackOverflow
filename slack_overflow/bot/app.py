import os
import sqlite3
# Use the package we installed
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(directory, '.env'))

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Add functionality here
# @app.event("app_home_opened") etc
@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(f"Hey there <@{message['user']}>!")

@app.message("button")
def message_button(message, say):
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )

@app.action("button_click")
def action_button_click(body, ack, say):
    # Acknowledge the action
    ack()
    say(f"<@{body['user']['id']}> clicked the button")

# Command that adds an issue to the database
# I don't think this should be the name personally
# Format: "/summarize [project] [issue title] [description]"
@app.command("/issue")
def issue_command(ack, say, respond, command):
    # Acknowledge command request first:
    ack()

    projectId = command['text']

    if 'error' in command['text']:
        if projectId == "":
            projectId = "projectId"
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*ERROR*\n Project `{projectId}` does not exist.\n_Use `/list projects` to retrieve a list of all project ids."
                }
            }
        ]
        respond(blocks=blocks, text="Error, project does not exist.")
    else:
    # Then respond
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "User posted a new issue for Ableplayer\n*<localhost.com|Why is my Docker not working????>*"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Project:*\nAbleplayer"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*User*\n<@U024BE7LH>"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Date Posted*\n31 March 2023"
                    }
                ]
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "Answer"
                        },
                        "style": "primary",
                        "value": "click_me_123"
                    }
                ]
            }
        ]

        say(blocks=blocks, text=f"{command['text']}")

# Command that adds an answer to an issue on the database
# Temporary name for now
# Format: "/answer [project] [issue] [description]"
@app.command("/answer")
def answer_command(ack, say, command):
    # Acknowledge command request first:
    ack()
    # Then respond
    app.client.chat_update(f"{command['text']}")

# Command that lists all of the available projects/issues
# Could be problematic to code, I'm unsure
# Format: "/list [issues|projects] <project>"
@app.command("/list")
def list_command(ack, say, command):
    # Acknowledge command request first:
    ack()
    # Then respond
    say(f"{command['text']}")

@app.command("/taher")
def list_command(ack, say, command):
    # Acknowledge command request first:
    ack()
    # Then respond
    array = ['j', 'a', 'c', 'o', 'b', ':jacob:']
    for i in range(len(array)):
        say(f"{array[i]}")

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
