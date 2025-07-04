from flask import Blueprint, json, request

webhook = Blueprint("webhook", __name__, url_prefix="/webhook")

@webhook.route("", methods=["GET"])
def api_root():
    return "Welcome to my Web app"

@webhook.route("/receiver", methods=["POST"])
def receiver():
    return {}, 200
