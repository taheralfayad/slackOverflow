import os
# Use the package we installed
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
@app.command("/summarize")
def summarize_command(ack, say, command):
    # Acknowledge command request first:
    ack()
    # Then respond
    say(f"{command['text']}")

# Command that adds an answer to an issue on the database
# Temporary name for now
# Format: "/answer [project] [issue] [description]"
@app.command("/answer")
def answer_command(ack, say, command):
    # Acknowledge command request first:
    ack()
    # Then respond
    say(f"{command['text']}")

# Command that lists all of the available projects/issues
# Could be problematic to code, I'm unsure
# Format: "/list [issues|projects] <project>"
@app.command("/summarize")
def list_command(ack, say, command):
    # Acknowledge command request first:
    ack()
    # Then respond
    say(f"{command['text']}")

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
