from django.urls import path
from slack_bolt.adapter.django import SlackRequestHandler
from bot.slack_listeners import app

handler = SlackRequestHandler(app=app)

from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def slack_events_handler(request: HttpRequest):
    return handler.handle(request)

@csrf_exempt
def slack_commands_handler(request: HttpRequest):
    return handler.handle(request)

urlpatterns = [
    path("slack/events", slack_events_handler, name="slack_events"),
    path("slack/command/", slack_commands_handler, name="slack_command"),
    path("slack/interactive-endpoint", slack_events_handler, name="slack_endpoint")
]
