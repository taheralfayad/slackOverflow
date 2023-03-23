import logging
import os
import requests
import json
from dotenv import load_dotenv

from slack_bolt import App

directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(directory, '.env'))

logger = logging.getLogger(__name__)

app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"],
    token_verification_enabled=False,
)

@app.event("app_mention")
def handle_app_mentions(logger, event, say):
    logger.info(event)
    say(f"Hi there, <@{event['user']}>")

# Add functionality here
# @app.event("app_home_opened") etc
@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(f"Hey there <@{message['user']}>!")

@app.message()
def ignore(message, say):
    1 + 1

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

@app.command("/addproject")
def project_command(ack, say, respond, command):
    ack()

    error = False

    array = command['text'].replace(" ", "").lower()

    object = {
        'name': array
    }

    post = requests.post(os.environ['SITE_URL'] + "/projects", json=object)

    respond(f'Successfully created project `{array}`.')

# Command that adds an issue to the database
# I don't think this should be the name personally
# Format: "/issue [project] [issue title] [description]"
@app.command("/issue")
def issue_command(ack, say, respond, command):
    # Acknowledge command request first:
    ack()

    error = False

    # array: ["projectId ", "issue title", " ", "issue description"]
    array = command['text'].split('"')

    if len(array) >= 4:
        object = {
            'project': array[0].strip().lower(),
            'title': array[1].title(),
            'description': array[3],
            'author': command['user_id']
        }

        post = requests.post(os.environ['SITE_URL'] + f"/projects/{object['project']}/issues", json=object)
        response = json.loads(post.text)
    
    else:
        error = True

    if error == True:
        projectId = command['text']
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
                    "text": f"User posted a new issue for {response['project']}\n*<localhost.com|{response['title']}>*"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Project:*\n{response['project']}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Issue Id:*\n{response['id']}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*User*\n<@{command['user_id']}>"
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
# Format: "/answer [issue] [description]"
@app.command("/answer")
def answer_command(ack, say, respond, command):
    # Acknowledge command request first:
    ack()

    error = False
    # array: ["issueId ", "answer description", ""]
    array = command['text'].split('"')
    
    # Validate
    validObject = {
        "id": array[0].strip()
    }

    validGet = requests.get(os.environ['SITE_URL'] + f"/issues/{validObject['id']}", json=validObject)
    print(validGet.text)
    issue = json.loads(validGet.text)

    if issue['detail']:
        error = True
    if len(array) >= 2 and error == False:
        object = {
            "issue": array[0].strip(),
            "description": array[1],
            "author": command['user_id'],
        }
        post = requests.post(os.environ['SITE_URL'] + f"/issues/{object['issue']}/solutions", json=object)
        response = json.loads(post.text)
    else:
        error = True

    if error == True:
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
				    "text": f"*ERROR*\n Issue `{validObject['id']}` does not exist."
			    }
		    }
	    ]
        respond(blocks=blocks, text="Error, issue does not exist.")

    else: 
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"<@{issue['author']}>, <@{response['author']}> submitted an answer for your {issue['project']} issue\n*<https://localhost:5000|{issue['title']}>*"
                }
            }
        ]
        say(blocks=blocks, text=f"<@{issue['author']}>, <@{response['author']}> submitted an answer for your {issue['project']} issue\n*<https://localhost:5000|{issue['title']}")

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
