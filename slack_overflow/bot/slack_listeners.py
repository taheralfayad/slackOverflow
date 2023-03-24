import logging
import os
import requests
import json
from dotenv import load_dotenv

from slack_bolt import App

directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(directory, '.env'))
logger = logging.getLogger(__name__)

API_URL = os.environ['SITE_URL'] + '/api'

app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"],
    token_verification_enabled=False,
)

@app.middleware
def log_request(logger, body, next):
    logger.debug(body)
    next()

@app.event("app_mention")
def handle_app_mentions(logger, event, say):
    logger.info(event)
    say(f"Hi there, <@{event['user']}>")

@app.message()
def ignore(message, say):
    ''

@app.action("answer_button")
def action_button_click(body, ack, client, action, logger):
    # Acknowledge the action
    ack()

    object = {
        'id': action['value'],
    }

    get = requests.get(API_URL + f"/issues/{object['id']}", json=object)
    issue = json.loads(get.text)

    print("ANSWER BUTTON\n", action, '\n')
    
    res = client.views_open(
        trigger_id=body["trigger_id"],
        view = {
            "type": "modal",
            "callback_id": "answer-modal",
            "title": {
                "type": "plain_text",
                "text": f"{issue['title']}",
                "emoji": True
            },
            "submit": {
                "type": "plain_text",
                "text": "Submit",
                "emoji": True
            },
            "close": {
                "type": "plain_text",
                "text": "Cancel",
                "emoji": True
            },
            "private_metadata": f"{issue['id']}",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"```{issue['description']}```"
                    }
                },
                {
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "multiline": True,
                        "action_id": "plain_text_input-action"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Answer",
                        "emoji": True
                    }
                },
                {
                    "block_id": "conversation",
                    "type": "input",
                    "label": {
                        "type": "plain_text",
                        "text": "Select a channel to post to"
                    },
                    "element": {
                        "action_id": "conversations_select",
                        "type": "conversations_select",
                        "response_url_enabled": True,
                        "default_to_current_conversation": True
                    }
                }
            ]
        }
    )
    logger.info(res)

@app.view("answer-modal")
def view_submission(ack, body, respond, view, action, logger, payload):
    ack()

    issue_id = view['private_metadata']
    validGet = requests.get(API_URL + f"/issues/{issue_id}", json={ 'id': issue_id })
    issue = json.loads(validGet.text)

    answer_input = next(iter(view['state']['values'].values()))['plain_text_input-action']['value']
    author = body["user"]["id"]

    object = {
            "issue": issue['id'],
            "description": answer_input,
            "author": author,
        }
    
    post = requests.post(API_URL + f"/issues/{object['issue']}/solutions", json=object)
    response = json.loads(post.text)

    object = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"<@{issue['author']}>, <@{response['author']}> submitted an answer for your {issue['project']} issue\n*<https://localhost:5000|{issue['title']}>*"
                },
            }
        ],
        "response_type": "in_channel"
    }

    requests.post(body['response_urls'][0]['response_url'], json=object)

@app.command("/addproject")
def project_command(ack, say, respond, command):
    ack()

    error = False

    array = command['text'].replace(" ", "").lower()

    object = {
        'name': array
    }

    requests.post(API_URL + "/projects", json=object)

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

        post = requests.post(API_URL + f"/projects/{object['project']}/issues", json=object)
        response = json.loads(post.text)

        if 'detail' in response:
            error = True
    else:
        error = True

    if error == True:
        projectId = object['project']
        if not projectId:
            projectId = 'projectId'
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*ERROR*\n Project `{projectId}` does not exist.\nUse `/list projects` to retrieve a list of all project ids."
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
                            "text": "Answer",
                            "emoji": True
                        },
                        "style": "primary",
                        "value": f"{response['id']}",
                        "action_id": "answer_button"
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

    validGet = requests.get(API_URL + f"/issues/{validObject['id']}", json=validObject)
    issue = json.loads(validGet.text)

    if issue['detail']:
        error = True
    if len(array) >= 2 and error == False:
        object = {
            "issue": array[0].strip(),
            "description": array[1],
            "author": command['user_id'],
        }
        post = requests.post(API_URL + f"/issues/{object['issue']}/solutions", json=object)
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

@app.command("/jacob")
def jacob_command(ack, say, command):
    # Acknowledge command request first:
    ack()
    # Then respond
    say(":jacob:")
